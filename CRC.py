import crcmod

# Define CRC-32/MPEG-2 (no reflection, no XOR, init=0x00000000)
crc32_mpeg2 = crcmod.mkCrcFun(poly=0x104C11DB7, rev=False, initCrc=0x00000000, xorOut=0x00000000)

# Input data: f5 47 00 00 00 00 00 00 00 00
data = bytes([0xF5, 0x47, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
checksum = crc32_mpeg2(data)

print(f"CRC32 (MPEG-2): {checksum:08X}")

data2 = bytes([0xF5, 0x47])
checksum2 = crc32_mpeg2(data2)

print(f"CRC32 (MPEG-2): {checksum2:08X}")