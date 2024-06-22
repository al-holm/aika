import coverage
import unittest

cov = coverage.Coverage(branch=True, omit=['*/__init__.py', '*/tests/*'])
cov.start()

loader = unittest.TestLoader()
suite = loader.discover('agent_service/')

runner = unittest.TextTestRunner()
runner.run(suite)


cov.stop()
cov.save()

cov.report()
with open('test_coverage.txt', 'w') as f:
        cov.report(file=f)
#cov.html_report(directory='htmlcov')