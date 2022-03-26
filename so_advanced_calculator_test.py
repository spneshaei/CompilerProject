import unittest

from so_advanced_calculator import *
  
class SoAdvancedCalculatorTest(unittest.TestCase):

    def setUp(self):
        pass
  
    def test_add_one_to_number(self):        
        self.assertEquals(add_one_to_number(1), 2)
        self.assertEquals(add_one_to_number(2), 3)
        self.assertEquals(add_one_to_number(3), 4)
        self.assertEquals(add_one_to_number(0), 1)
        self.assertEquals(add_one_to_number(-5), -4)
        self.assertEquals(add_one_to_number(-1), 0)
        self.assertEquals(add_one_to_number(len("Taha")), len("Parsa"))

    def test_subtract_one_from_number(self):        
        self.assertEquals(subtract_one_from_number(2), 1)
        self.assertEquals(subtract_one_from_number(3), 2)
  
if __name__ == '__main__':
    unittest.main()