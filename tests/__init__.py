import os
import sys
import unittest

import coverage

#from .tests import FlackTests
from .twitter import TestTwitterStream

def run():
    os.environ['FLACK_CONFIG'] = 'testing'

    # start coverage engine
    cov = coverage.Coverage(branch=True)
    cov.start()

    # run tests
    tests = unittest.TestLoader().discover('.')
    ok = unittest.TextTestRunner(verbosity=2).run(tests).wasSuccessful()

    # print coverage report
    cov.stop()
    print('')
    cov.report(omit=['manage.py', 'tests/*', 'venv*/*'])

    sys.exit(0 if ok else 1)

if __name__ == "__main__":
    unittest.main()