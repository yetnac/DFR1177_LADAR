# -*- coding: utf-8 -*-
"""
Notes
"""
import serial 
import struct 
import binascii 

# CRC32 parameters 
CRC_POLYNOMIAL = 0x04C11DB7 
CRC_INIT = 0xFFFFFFFF 
CRC_XOR_OUT = 0x00000000 

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
    crc = calculate_crc32(header) 
    crc_bytes = struct.pack('>I', crc)  # Big-endian CRC 
    packet = header + crc_bytes 
    return packet 

 
def parse_response_packet(packet: bytes): 
    """Parses a variable-length response packet.""" 
    if len(packet) < 8:  # Start + type + len (2) + CRC (4) + end 
        raise ValueError("Packet too short.") 

    if packet[0] != END_CMD: 
        raise ValueError("Invalid start byte.") 
 
    pkt_type = packet[1] 
    data_len = struct.unpack('>H', packet[2:4])[0] 
    expected_len = 1 + 1 + 2 + data_len + 4  # start + type + len + data + CRC 

    if len(packet) != expected_len: 
        raise ValueError("Incorrect packet length.") 
 
    data = packet[4:4+data_len] 
    crc_received = struct.unpack('>I', packet[4+data_len:])[0] 
    crc_calculated = calculate_crc32(packet[:4+data_len]) 

    if crc_received != crc_calculated: 
        raise ValueError("CRC check failed.") 

    return pkt_type, data 
 

def send_command(ser, cmd_id: int, params: bytes): 
    """Send a command packet and receive a response.""" 
    packet = build_command_packet(cmd_id, params) 
    ser.write(packet) 

    # Read start byte 
    while True: 
        start_byte = ser.read(1) 
        if start_byte == bytes([END_CMD]): 
            break 

    header = start_byte + ser.read(3)  # type + 2-byte length 
    pkt_type = header[1] 
    data_len = struct.unpack('>H', header[2:4])[0] 
    data = ser.read(data_len) 
    crc_bytes = ser.read(4) 

    full_packet = header + data + crc_bytes 
    return parse_response_packet(full_packet) 

if __name__ == "__main__": 
    # Example usage 
    try: 
        ser = serial.Serial('COM3', 115200, timeout=1)  # Adjust port as needed 

        # Example: send command ID 0x01 with dummy 8-byte parameters 
        params = b'\x01\x02\x03\x04\x05\x06\x07\x08' 
        pkt_type, data = send_command(ser, 0x01, params) 

        print(f"Received response type: {pkt_type}") 
        print(f"Data: {data.hex()}") 

    except Exception as e: 
        print(f"Error: {e}") 

 

 
