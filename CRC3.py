def crc32_bitwise(data, initial_crc=0xFFFFFFFF, polynomial=0x04C11DB7):
    """
    Calculates the bit-wise CRC32 checksum of data.

    Args:
        data: The data to calculate the CRC32 for (bytes or bytearray).
        initial_crc: The initial CRC value (default is 0xFFFFFFFF for standard CRC32).
        polynomial: The CRC32 generator polynomial (default is 0xEDB88320 for reversed representation).

    Returns:
        The calculated CRC32 checksum as a 32-bit integer.
    """
    crc = initial_crc
    for byte in data:
        crc ^= byte
        for _ in range(8):
            if crc & 1:  # Check the least significant bit
                crc = (crc >> 1) ^ polynomial
            else:
                crc >>= 1
    return crc ^ 0x00000000  # Final XOR with 0xFFFFFFFF (for standard CRC32)

# Example usage:
#data_to_send = b'\xF5\x47\x00\x00\x00\x00\x00\x00\x00\x00'   #\x8C\x7B\x6E\xC5'
data_to_send = b'\xF5\x4A\x00\x00\x00\x00\x00\x00\x00\x00' #\x1F\xF8\x6E\x87'
#data_to_send = b"Hello, Microcontroller!"
checksum = crc32_bitwise(data_to_send)
print(f"CRC32 Checksum: {hex(checksum)}")
