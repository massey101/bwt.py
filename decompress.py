import sys
import typing

RUNLENGTH_BYTES = 1

def read_run_length(inputdata: typing.BinaryIO, runlength_bytes):
    runlength = bytearray()
    for j in range(runlength_bytes):
        buffer = inputdata.read(1)
        if buffer == b'':
            return 0
        runlength.extend(buffer)
    runlength = int.from_bytes(runlength, 'little')

    return runlength

def decompress(inputdata: typing.BinaryIO, output: typing.BinaryIO, runlength_bytes=RUNLENGTH_BYTES):
    while True:
        runlength = read_run_length(inputdata, runlength_bytes)
        if runlength == 0:
            break
        character = inputdata.read(1)
        if character == b'':
            raise Exception('Unexpected EOF')
        output.write(character * runlength)

def main():
    decompress(sys.stdin.buffer, sys.stdout.buffer)

if __name__ == '__main__':
    main()
