import sys
import typing

RUNLENGTH_BYTES = 1
def get_max_run_length(runlength_bytes: int) -> int:
    return 1 << (7 + (8 * (runlength_bytes-1)))

def decode_runlength(encoded_runlength: bytes, runlength_bytes: int) -> int:
    runlength = int.from_bytes(encoded_runlength, 'little')
    runlength -= get_max_run_length(runlength_bytes)
    return runlength

def decompress(inputdata: typing.BinaryIO, output: typing.BinaryIO, runlength_bytes=RUNLENGTH_BYTES):
    while True:
        character = inputdata.read(1)
        if character == b'':
            break

        if not character[0] & 1 << 7:
            output.write(character)
            continue

        if runlength_bytes - 1 > 0:
            character += inputdata.read(runlength_bytes - 1)

        runlength = decode_runlength(character, runlength_bytes)
        character = inputdata.read(1)
        if character == b'':
            raise Exception('Unexpected EOF')
        output.write(character * runlength)

def main():
    decompress(sys.stdin.buffer, sys.stdout.buffer)

if __name__ == '__main__':
    main()
