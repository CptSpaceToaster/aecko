import unittest
import numpy

from aecko import blend


class ExampleTestClass(unittest.TestCase):
    def setUp(self):
        pass

    def test_compare(self):
        a = numpy.array([[[127, 127, 127],
                          [127, 127, 127]],
                         [[127, 127, 127],
                          [127, 127, 127]]],
                        dtype=numpy.int16)

        b = numpy.array([[[127, 127, 127],
                          [255, 0,   0]],
                         [[0,   255, 0],
                          [0,   0,   255]]],
                        dtype=numpy.int16)

        c = numpy.array([[[127, 127, 127],
                          [191, 64,  64]],
                         [[64,  191, 64],
                          [64,  64,  191]]])

        d = numpy.array([[[127, 127, 127],
                          [63,  191, 191]],
                         [[191, 63,  191],
                          [191, 191, 63]]])

        e = blend.do_compare(a, b)
        f = blend.do_compare(b, a)

        numpy.testing.assert_equal(e, c)
        self.assertEqual(e.dtype, numpy.uint8)
        numpy.testing.assert_equal(f, d)
        self.assertEqual(f.dtype, numpy.uint8)

    def test_compare_with_alpha(self):
        a = numpy.array([[[127, 127, 127, 255],
                          [127, 127, 127, 255]],
                         [[127, 127, 127, 255],
                          [127, 127, 127, 255]]],
                        dtype=numpy.int16)

        b = numpy.array([[[127, 127, 127, 255],
                          [255, 0,   0,   255]],
                         [[0,   255, 0,   255],
                          [0,   0,   255, 255]]],
                        dtype=numpy.int16)

        c = numpy.array([[[127, 127, 127, 255],
                          [191, 64,  64,  255]],
                         [[64,  191, 64,  255],
                          [64,  64,  191, 255]]])

        d = numpy.array([[[127, 127, 127, 255],
                          [63,  191, 191, 255]],
                         [[191, 63,  191, 255],
                          [191, 191, 63,  255]]])

        e = blend.do_compare(a, b)
        f = blend.do_compare(b, a)

        numpy.testing.assert_equal(e, c)
        self.assertEqual(e.dtype, numpy.uint8)
        numpy.testing.assert_equal(f, d)
        self.assertEqual(f.dtype, numpy.uint8)

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
