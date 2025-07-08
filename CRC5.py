import struct

def calculate_crc32_little_endian(data):
    """
    Calculates the CRC32 checksum of data for a little-endian system.

    Args:
        data: The data (bytes) to calculate the checksum for.

    Returns:
        The CRC32 checksum as an integer.
    """
    crc = 0xFFFFFFFF  # Initial CRC value (common for CRC32)
    polynomial = 0x04C11DB7  # Standard CRC32 polynomial

    for byte in data:
        crc ^= byte << 24  # XOR the current byte with the highest byte of CRC

        for _ in range(8):
            if crc & 0x80000000:
                crc = (crc << 1) ^ polynomial
            else:
                crc <<= 1

    return crc & 0xFFFFFFFF  # Return the 32-bit checksum

# http://www.zorc.breitbandkatze.de/crc.html    %12%34%56%78  DF8A8A2B (hex), 4 data bytes
# Example usage:
#message = b"Hello, STM32 UART!"
# data F5470000000000000000  CRC 8C 7B 6E C5
#data_to_send = b'\xF5\x47\x00\x00\x00\x00\x00\x00\x00\x00'   #\x8C\x7B\x6E\xC5'
data_to_send = b'\xF5\x4A\x00\x00\x00\x00\x00\x00\x00\x00' #\x1F\xF8\x6E\x87'
crc_checksum = calculate_crc32_little_endian(data_to_send)
print(f"CRC32 Checksum (Little-Endian): {hex(crc_checksum)}")

# To send the CRC over UART, you'd need to convert it to bytes in little-endian format
crc_bytes = struct.pack('<I', crc_checksum) # '<' for little-endian, 'I' for unsigned int
print(f"CRC32 Checksum (Little-Endian bytes): {crc_bytes}")

# You would then append crc_bytes to your data before sending it over UART.
