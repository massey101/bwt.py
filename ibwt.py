import sys
import bwt_impl

def main():
    bwt_impl.ibwt_stream(sys.stdin.buffer, sys.stdout.buffer)

if __name__ == '__main__':
    main()
