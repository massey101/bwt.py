import sys
import typing

RUNLENGTH_BYTES = 1

def compress(inputdata: typing.BinaryIO, output: typing.BinaryIO, runlength_bytes=RUNLENGTH_BYTES):
    max_runlength = 2 ** (8 * runlength_bytes)

    runcharacter = None
    runlength = 0
    while True:
        character = inputdata.read(1)
        if character == b'':
            break

        if character != runcharacter or runlength >= max_runlength - 1:
            if runcharacter != None:
                output.write(runlength.to_bytes(runlength_bytes, 'little'))
                output.write(runcharacter)
            runlength = 0
            runcharacter = character

        runlength += 1

    if runcharacter != None:
        output.write(runlength.to_bytes(runlength_bytes, 'little'))
        output.write(runcharacter)

def main():
    compress(sys.stdin.buffer, sys.stdout.buffer)

if __name__ == '__main__':
    main()
