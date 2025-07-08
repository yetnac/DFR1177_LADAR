def crc32_bitwise_le(data: bytes, poly: int = 0x04C11DB7, initial_value: int = 0xFFFFFFFF) -> int:
    """
    Calculates the CRC-32 checksum for a byte string, bit-wise,
    considering little-endian byte order.

    Args:
        data: The input byte string.
        poly: The CRC-32 polynomial (default: 0x04C11DB7).
        initial_value: The initial value of the CRC register (default: 0xFFFFFFFF).

    Returns:
        The calculated CRC-32 checksum (32-bit unsigned integer).
    """

    crc = initial_value
    bitmask = 0xFFFFFFFF  # To keep the CRC within 32 bits

    # Process data byte by byte (little-endian: process bytes in their order)
    for byte in data:
        # Process each bit of the byte
        for i in range(8):
            # Check the most significant bit (MSB) of the current CRC
            msb_is_set = (crc & (1 << 31)) != 0

            # Shift CRC left and add the current data bit
            # For little-endian, process the least significant bit first
            current_bit = (byte >> i) & 1  # Get the i-th bit
            crc = (crc << 1) | current_bit
            crc &= bitmask  # Keep it at 32 bits

            # If MSB was set, XOR with polynomial
            if msb_is_set:
                crc ^= poly

    return crc

# Example usage:
#data_to_send = b'hello world!'
#data_to_send = b'\xF5\x47\x00\x00\x00\x00\x00\x00\x00\x00'   #\x8C\x7B\x6E\xC5'
data_to_send = b'\xF5\x4A\x00\x00\x00\x00\x00\x00\x00\x00' #\x1F\xF8\x6E\x87'
calculated_crc = crc32_bitwise_le(data_to_send)
print(f"CRC32 (little-endian): {hex(calculated_crc)}")
