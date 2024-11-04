import unittest
import compress_smart as compress
import decompress_smart as decompress
import io

class TestCompress(unittest.TestCase):
    def _run_and_assert(self, fn, a, b):
        c = io.BytesIO()
        fn(io.BytesIO(a), c)
        c.seek(0)
        self.assertEqual(b, c.read())

    def test_basic_compress(self):
        a = "This is          a test string AHHHHH!".encode('utf8')
        b = b'This is\x8a a test string A\x85H!'
        self._run_and_assert(compress.compress, a, b)

    def test_basic_decompress(self):
        a = b'This is\x8a a test string A\x85H!'
        b = "This is          a test string AHHHHH!".encode('utf8')
        self._run_and_assert(decompress.decompress, a, b)

    def test_compress_large_runlength(self):
        a = "A" + "B" * 127 + "C"
        a = a.encode('utf8')
        b = b'A\xFFBC'
        self._run_and_assert(compress.compress, a, b)

    def test_decompress_large_runlength(self):
        a = b'A\xFFBC'
        b = "A" + "B" * 127 + "C"
        b = b.encode('utf8')
        self._run_and_assert(decompress.decompress, a, b)

    def test_compress_max_runlength(self):
        a = "A" + "B" * 128 + "C"
        a = a.encode('utf8')
        b = b'A\xFFBBC'
        self._run_and_assert(compress.compress, a, b)

    def test_decompress_max_runlength(self):
        a = b'A\xFFBBC'
        b = "A" + "B" * 128 + "C"
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
