import binascii

# Constants
START_CMD = 0xF5
cmd_id = 0x47
params = b'\x00\x00\x00\x00\x00\x00\x00\x00'
header = bytes([START_CMD, cmd_id]) + params
print(' '.join(f'{x:02x}' for x in header))
# CRC32 parameters
CRC_POLYNOMIAL = 0x04C11DB7
CRC_INIT = 0xFFFFFFFF
CRC_XOR_OUT = 0x00000000
crc = CRC_INIT
crc = binascii.crc32(header, crc) & 0xFFFFFFFF
#output = crc ^ CRC_XOR_OUT
#print(' '.join(f'{x:02x}' for x in crc))

print(crc.hex())