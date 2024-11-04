import unittest
import compress
import decompress
import io

class TestCompress(unittest.TestCase):
    def _run_and_assert(self, fn, a, b):
        c = io.BytesIO()
        fn(io.BytesIO(a), c)
        c.seek(0)
        self.assertEqual(b, c.read())

    def test_basic_compress(self):
        a = "This is          a test string AHHHHH!".encode('utf8')
        b = b'\x01T\x01h\x01i\x01s\x01 \x01i\x01s\x0a \x01a\x01 \x01t\x01e\x01s\x01t\x01 \x01s\x01t\x01r\x01i\x01n\x01g\x01 \x01A\x05H\x01!'
        self._run_and_assert(compress.compress, a, b)

    def test_basic_decompress(self):
        a = b'\x01T\x01h\x01i\x01s\x01 \x01i\x01s\x0a \x01a\x01 \x01t\x01e\x01s\x01t\x01 \x01s\x01t\x01r\x01i\x01n\x01g\x01 \x01A\x05H\x01!'
        b = "This is          a test string AHHHHH!".encode('utf8')
        self._run_and_assert(decompress.decompress, a, b)

    def test_compress_large_runlength(self):
        a = "A" + "B" * 255 + "C"
        a = a.encode('utf8')
        b = b'\x01A\xFFB\x01C'
        self._run_and_assert(compress.compress, a, b)

    def test_decompress_large_runlength(self):
        a = b'\x01A\xFFB\x01C'
        b = "A" + "B" * 255 + "C"
        b = b.encode('utf8')
        self._run_and_assert(decompress.decompress, a, b)

    def test_compress_max_runlength(self):
        a = "A" + "B" * 256 + "C"
        a = a.encode('utf8')
        b = b'\x01A\xFFB\x01B\x01C'
        self._run_and_assert(compress.compress, a, b)

    def test_decompress_max_runlength(self):
        a = b'\x01A\xFFB\x01B\x01C'
        b = "A" + "B" * 256 + "C"
        b = b.encode('utf8')
        self._run_and_assert(decompress.decompress, a, b)

    def test_compress_empty(self):
        a = b''
        b = b''
        self._run_and_assert(compress.compress, a, b)

    def test_decompress_empty(self):
        a = b''
        b = b''
        self._run_and_assert(decompress.decompress, a, b)
