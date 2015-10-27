import unittest


class ExampleTestClass(unittest.TestCase):
    def setUp(self):
        pass

    def test_example(self):
        """
        This function name MUST begin with 'test'
        """
        self.assertEqual(1 + 2, 3)

    def test_example_another(self):
        self.assertNotEqual(1, '1')

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
