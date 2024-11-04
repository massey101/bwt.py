import sys
import typing

RUNLENGTH_BYTES = 1

def get_max_runlength(runlength_bytes: int) -> int:
    return 1 << (7 + (8 * (runlength_bytes-1)))


def encode_run(runlength: int, runcharacter: bytes, runlength_bytes: int) -> bytes:
    max_runlength = get_max_runlength(runlength_bytes)
    assert runlength < max_runlength

    if runlength <= runlength_bytes:
        return runcharacter * runlength

    runlength += max_runlength
    return runlength.to_bytes(runlength_bytes, 'big') + runcharacter


def compress(inputdata: typing.BinaryIO, output: typing.BinaryIO, runlength_bytes=RUNLENGTH_BYTES):
    max_runlength = get_max_runlength(runlength_bytes)

    runcharacter = None
    runlength = 0
    while True:
        character = inputdata.read(1)
        if character == b'':
            break

        if character != runcharacter or runlength >= max_runlength - 1:
            if runcharacter != None:
                output.write(encode_run(runlength, runcharacter, runlength_bytes))
            runlength = 0
            runcharacter = character

        runlength += 1

    if runcharacter != None:
        output.write(encode_run(runlength, runcharacter, runlength_bytes))

def main():
    compress(sys.stdin.buffer, sys.stdout.buffer)

if __name__ == '__main__':
    main()
