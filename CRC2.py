POLY = 0x04C11DB7
INIT = 0x00000000#0xFFFFFFFF
XOR_OUT = 0x00000000

# Generate lookup table (no reflection)
def generate_crc_table():
    table = []
    for byte in range(256):
        crc = byte << 24  # Top-align byte in 32-bit word
        for _ in range(8):
            if (crc & 0x80000000):
                crc = ((crc << 1) ^ POLY) & 0xFFFFFFFF
            else:
                crc = (crc << 1) & 0xFFFFFFFF
        table.append(crc)
    return table

CRC_TABLE = generate_crc_table()

# Compute byte-wise CRC32 (no reflection)
def crc32_bytewise(data: bytes):
    crc = INIT
    for byte in data:
        index = ((crc >> 24) ^ byte) & 0xFF
        crc = ((crc << 8) ^ CRC_TABLE[index]) & 0xFFFFFFFF
    return crc ^ XOR_OUT

# Test example
data = bytes.fromhex("F5 47 00 00 00 00 00 00 00 00")
checksum = crc32_bytewise(data)
print(f"CRC32: {checksum:08X}")
