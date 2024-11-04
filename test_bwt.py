import unittest
import bwt_impl as bwt
import io

class TestBWT(unittest.TestCase):
    def _run_and_assert(self, fn, a, b, *args):
        c = io.BytesIO()
        fn(io.BytesIO(a), c, *args)
        c.seek(0)
        self.assertEqual(b, c.read())

    def test_bwt_basic(self):
        a = b'BANANA'
        b = b'\03ANNB\02AA'
        c = bwt.bwt(a)
        self.assertEqual(b, c)

    def test_ibwt_basic(self):
        a = b'\03ANNB\02AA'
        b = b'BANANA'
        c = bwt.ibwt(a)
        self.assertEqual(b, c)

    def test_bwt_longer(self):
        a = b'SIX.MIXED.PIXIES.SIFT.SIXTY.PIXIE.DUST.BOXES'
        b = b'\03STEXYDST.E.IXXIIXXSSMPPS.B..EE.\02.USFXDIIOIIIT'
        c = bwt.bwt(a)
        self.assertEqual(b, c)

    def test_ibwt_longer(self):
        a = b'\03STEXYDST.E.IXXIIXXSSMPPS.B..EE.\02.USFXDIIOIIIT'
        b = b'SIX.MIXED.PIXIES.SIFT.SIXTY.PIXIE.DUST.BOXES'
        c = bwt.ibwt(a)
        self.assertEqual(b, c)

    def test_bwt_empty(self):
        a = b''
        b = b'\03\02'
        c = bwt.bwt(a)
        self.assertEqual(b, c)

    def test_ibwt_empty(self):
        a = b'\03\02'
        b = b''
        c = bwt.ibwt(a)
        self.assertEqual(b, c)

    def test_bwt_stream_basic(self):
        a = b'BANANA'
        b = b'\x08\x00\x00\x00\03ANNB\02AA'
        self._run_and_assert(bwt.bwt_stream, a, b)

    def test_ibwt_stream_basic(self):
        a = b'\x08\x00\x00\x00\03ANNB\02AA'
        b = b'BANANA'
        self._run_and_assert(bwt.ibwt_stream, a, b)

    def test_bwt_stream_empty(self):
        a = b''
        b = b''
        self._run_and_assert(bwt.bwt_stream, a, b)

    def test_ibwt_stream_empty(self):
        a = b''
        b = b''
        self._run_and_assert(bwt.ibwt_stream, a, b)

    def test_bwt_stream_block_size(self):
        a = b'A' + b'B' * (256-2) + b'C'
        b = b'\x02\x01\x00\x00\03C\02A' + b'B' * (256-2)
        self._run_and_assert(bwt.bwt_stream, a, b, 256)

    def test_ibwt_stream_block_size(self):
        a = b'\x02\x01\x00\x00\03C\02A' + b'B' * (256-2)
        b = b'A' + b'B' * (256-2) + b'C'
        self._run_and_assert(bwt.ibwt_stream, a, b)

    def test_bwt_stream_two_blocks(self):
        a = b'A' + b'B' * (256-1) + b'C'
        b = b'\x02\x01\x00\x00\03B\02B' + b'B' * (256-3) + b'A' + b'\x03\x00\x00\x00\03C\02'
        self._run_and_assert(bwt.bwt_stream, a, b, 256)

    def test_ibwt_stream_two_blocks(self):
        a = b'\x02\x01\x00\x00\03B\02B' + b'B' * (256-3) + b'A' + b'\x03\x00\x00\x00\03C\02'
        b = b'A' + b'B' * (256-1) + b'C'
        self._run_and_assert(bwt.ibwt_stream, a, b)


