import sys
import bwt_impl

def main():
    bwt_impl.bwt_stream(sys.stdin.buffer, sys.stdout.buffer)

if __name__ == '__main__':
    main()
