import unittest
if __name__ == "__main__":
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover("tests", pattern="*.py")
    
    test_runner = unittest.TextTestRunner(verbosity=2)
    test_runner.run(test_suite)