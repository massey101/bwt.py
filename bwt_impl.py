import typing
import string

BLOCK_SIZE_BYTES = 4
DEFAULT_BLOCK_SIZE = 1 * 1024

def encode_blocksize(blocksize: int) -> bytes:
    return blocksize.to_bytes(BLOCK_SIZE_BYTES, 'little')

def decode_blocksize(encoded: bytes) -> int:
    if len(encoded) != BLOCK_SIZE_BYTES:
        raise ValueError('Blocksize must be {} bytes'.format(BLOCK_SIZE_BYTES))
    return int.from_bytes(encoded, 'little')

def bwt_stream(inputdata: typing.BinaryIO, output: typing.BinaryIO, blocksize=DEFAULT_BLOCK_SIZE):
    while True:
        block = inputdata.read(blocksize)
        if block == b'':
            return
        encoded = bwt(block)
        output.write(encode_blocksize(len(encoded)))
        output.write(encoded)

def ibwt_stream(inputdata: typing.BinaryIO, output: typing.BinaryIO):
    while True:
        encoded_blocksize = inputdata.read(BLOCK_SIZE_BYTES)
        if encoded_blocksize == b'':
            return
        blocksize = decode_blocksize(encoded_blocksize)
        block = inputdata.read(blocksize)
        if len(block) != blocksize:
            raise ValueError('Block malformed. Expected size {}'.format(blocksize))
        output.write(ibwt(block))

ALPHABET = (
    string.whitespace
    + string.punctuation
    + string.digits
    + string.ascii_uppercase
    + string.ascii_lowercase
)
ALPHABET += ''.join([chr(i) for i in range(0, 127) if chr(i) not in ALPHABET])
ALPHABET = ALPHABET.encode('utf8')

class FastAlphabet:
    def __init__(self, alphabet):
        self.alphabet = {}
        for i in range(len(alphabet)):
            self.alphabet[alphabet[i]] = i

    def __contains__(self, letter):
        return letter in self.alphabet

    def index(self, letter):
        return self.alphabet[letter]

FAST_ALPHABET = FastAlphabet(ALPHABET)

def sorter(table: list[bytes]) -> list[bytes]:
    # return sorted(table, key=lambda x: [ALPHABET.index(c) if c in ALPHABET else c for c in x])
    return sorted(table)

def bwt(inputdata: bytes) -> bytes:
    return bwt_fast(inputdata)
    assert b'\02' not in inputdata and b'\03' not in inputdata

    inputdata = b'\02' + inputdata + b'\03'
    table = [inputdata[i:] + inputdata[:i] for i in range(len(inputdata))]
    sorted_table = sorted(table)
    return bytes([line[-1] for line in sorted_table])

def calc_value(inputdata: bytes) -> bytes:
    total = 0
    for i in range(len(inputdata)):
        total += inputdata[i] * (127 ** (len(inputdata) - i))
    return total

def bwt_fast(inputdata: bytes) -> bytes:
    inputdata = b'\02' + inputdata + b'\03'
    table = [(inputdata[i-1], calc_value(inputdata[i:] + inputdata[:i])) for i in range(len(inputdata))]
    sorted_table = sorted(table, key=lambda x: x[1])
    return bytes([x[0] for x in sorted_table])

def ibwt(inputdata: bytes) -> bytes:
    assert b'\02' in inputdata and b'\03' in inputdata

    table = [b'' for b in range(len(inputdata))]
    for i in range(len(inputdata)):
        for j in range(len(inputdata)):
            table[j] = bytes([inputdata[j]]) + table[j]
        table = sorted(table)

    for line in table:
        if line[0] == 0x02 and line[-1] == 0x03:
            return line.strip(b'\02').strip(b'\03')

    return None
