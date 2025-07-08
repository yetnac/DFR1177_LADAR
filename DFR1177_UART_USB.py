import serial
import struct
import binascii

# CRC32 parameters
CRC_POLYNOMIAL = 0x04C11DB7
CRC_INIT = 0xFFFFFFFF
CRC_XOR_OUT = 0x00000000

# Miscellaneous Commands
GET_TEMPERATURE = 0x4A   # Returns the chip temperature
GET_TEMPERATURE_R = 0xFC
IDENTIFY = 0x47          # Returns the device ID and the operating mode
IDENTIFY_R = 0x02

# Constants
START_CMD = 0xF5
END_CMD = 0xFA
CMD_PACKET_LENGTH = 14

def calculate_crc32(data: bytes) -> int:
    """Calculates CRC32 with specified parameters."""
    crc = CRC_INIT
    crc = binascii.crc32(data, crc) & 0xFFFFFFFF
    return crc ^ CRC_XOR_OUT

def build_command_packet(cmd_id: int, params: bytes) -> bytes:
    """Builds a 14-byte command packet."""
    if len(params) != 8:
        raise ValueError("Parameters must be exactly 8 bytes.")

    header = bytes([START_CMD, cmd_id]) + params
    #print(' '.join(f'{x:02x}' for x in header))
    crc = calculate_crc32(header)
    crc_bytes = struct.pack('<I', crc)  # little-endian CRC
    packet = header + crc_bytes
    return packet

def parse_response_packet(packet: bytes):
    """Parses a variable-length response packet."""
    if len(packet) < 8:  # Start + type + len (2) + CRC (4) + end
        raise ValueError("Packet too short.")

    if packet[0] != END_CMD:
        raise ValueError("Invalid start byte.")

    pkt_type = packet[1]
    data_len = struct.unpack('<H', packet[2:4])[0]
    expected_len = 1 + 1 + 2 + data_len + 4  # start + type + len + data + CRC

    if len(packet) != expected_len:
        raise ValueError("Incorrect packet length.")

    data = packet[4:4+data_len]
    crc_received = struct.unpack('<I', packet[4+data_len:])[0]
    crc_calculated = calculate_crc32(packet[:4+data_len])
    #print(f'crc_received = {crc_received} and crc_calculated = {crc_calculated}')

    #if crc_received != crc_calculated:
    #    raise ValueError("CRC check failed.")

    return pkt_type, data

def send_command(ser, cmd_id: int, params: bytes):
    """Send a command packet and receive a response."""
    packet = build_command_packet(cmd_id, params)
    #print(' '.join(f'{x:02x}' for x in packet))
    #ser.write(packet)
    # Identify
    #IDcmd = b'\xF5\x47\x00\x00\x00\x00\x00\x00\x00\x00\x8C\x7B\x6E\xC5'
    # Get Temperature
    #IDcmd = b'\xF5\x4A\x00\x00\x00\x00\x00\x00\x00\x00\x1F\xF8\x6E\x87'
    # Set Integration Time
    #IDcmd = b'\xF5\x00\x00\x1E\x00\x00\x00\x00\x00\x00\x47\x07\xEC\xC0'
    # Get Distance
    IDcmd = b'\xF5\x20\x00\x00\x00\x00\x00\x00\x00\x00\x62\xAC\xA8\xCC'
    print(' '.join(f'{x:02x}' for x in IDcmd))
    ser.write(IDcmd)
    print("packets sent")

    # Read start byte (i.e., find start byte)
    while True:
        start_byte = ser.read(1)
        if start_byte == bytes([END_CMD]):
            break

    header = start_byte + ser.read(3)  # header = start_byte + type + 2 bytes(length)
    pkt_type = header[1]               # response type
    data_len = struct.unpack('<H', header[2:4])[0]   # length of data bytes to read
    data = ser.read(data_len)          # data bytes
    crc_bytes = ser.read(4)            # checksum

    full_packet = header + data + crc_bytes
    print(' '.join(f'{x:02x}' for x in full_packet))
    print("packets read")
    return parse_response_packet(full_packet)

print("Running Main")
if __name__ == "__main__":
    # Example usage
    try:
        ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1)  # Adjust port as needed
        print("Open Serial port")

        # Example: send IDENTIFY command ID 0x47 with dummy 8-byte parameters
        params = b'\x00\x00\x00\x00\x00\x00\x00\x00'
        pkt_type, data = send_command(ser, 0x47, params)

        print(f"Received response type: {pkt_type}")
        print(f"Data: {data.hex()}")

        if pkt_type == IDENTIFY_R: 
            print(f'Hardware version: {data[0]}, mode: {data[3]:02x}')

        if pkt_type == GET_TEMPERATURE_R:
            print(f'Temperature: {data} deg C')

    except Exception as e:
        print(f"Error: {e}")
    
# data_to_send = b'\xF5\x47\x00\x00\x00\x00\x00\x00\x00\x00\x8C\x7B\x6E\xC5'
#    data_read = b'\xFA\x02\x04\x00\x01\x00\x04\x00\xE0\x1E\x86\xB5'
# test in calc %FA%02%04%00%01%00%04%00

