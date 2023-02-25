from django.test import TestCase
# test_ is a must for test methods names
from store.logic import operations
 
class LogicTestCase(TestCase):
    def test_plus(self):
        result = operations(6, 13, "+")
        self.assertEqual(result, 19) 

    def test_minus(self):
        result = operations(6, 13, "-")
        self.assertEqual(result, -7)

    def test_multiply(self):
        result = operations(6, 13, "*")
        self.assertEqual(result, 78)