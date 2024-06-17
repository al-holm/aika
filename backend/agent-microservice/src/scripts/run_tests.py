import unittest
import xmlrunner
import coverage
import logging
import os
import sys
import webbrowser

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_tests():
    # Start coverage
    cov = coverage.Coverage()
    cov.start()

    # Add the root directory to the sys.path to ensure importability
    root_dir = os.path.abspath(os.path.dirname(__file__))
    if root_dir not in sys.path:
        sys.path.insert(0, root_dir)

    # Discover tests
    loader = unittest.TestLoader()

    # Define the directories to search for tests
    test_directories = [
        '/home/ali/Documents/aika/backend/agent-microservice/src/agent_service/agent/tests',
        '/home/ali/Documents/aika/backend/agent-microservice/src/agent_service/prompts/tests',
        '/home/ali/Documents/aika/backend/agent-microservice/src/agent_service/parsers/tests',
        '/home/ali/Documents/aika/backend/agent-microservice/src/agent_service/tools/tests',
        '/home/ali/Documents/aika/backend/agent-microservice/src/agent_service/rag/tests'
    ]
    
    # Create a test suite combining all discovered tests
    suite = unittest.TestSuite()
    for test_dir in test_directories:
        test_dir_path = os.path.join(root_dir, test_dir)
        logger.info(f"Discovering tests in {test_dir_path}")
        try:
            discovered_suite = loader.discover(start_dir=test_dir_path, pattern="test_*.py")
            suite.addTests(discovered_suite)
        except ImportError as e:
            logger.error(f"Error importing tests from {test_dir_path}: {e}")
        except Exception as e:
            logger.error(f"Unexpected error occurred while discovering tests in {test_dir_path}: {e}")

    if suite.countTestCases() == 0:
        logger.warning("No tests found! Check your test directories and patterns.")
    else:
        logger.info(f"Discovered {suite.countTestCases()} test cases.")

    # Run tests with XML reporting
    runner = xmlrunner.XMLTestRunner(output='test-reports')
    result = runner.run(suite)

    # Save coverage report
    cov.stop()
    cov.save()
    cov.report()
    
    with open('test_coverage.txt', 'w') as f:
        cov.report(file=f)
    cov.html_report(directory='coverage_html_report')

    logger.info(f"Coverage report generated in 'coverage_html_report' directory.")

    report_path = os.path.abspath('coverage_html_report/index.html')
    webbrowser.open(f'file://{report_path}')

    return result.wasSuccessful()

if __name__ == '__main__':
    successful = run_tests()
    if not successful:
        logger.error("Some tests failed.")
        os._exit(1)
    logger.info("All tests passed successfully.")