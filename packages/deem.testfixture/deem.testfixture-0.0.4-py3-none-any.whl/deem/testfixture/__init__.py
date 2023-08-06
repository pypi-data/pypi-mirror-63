import atexit
import json
import unittest
import errno
import os
import os.path
from datetime import datetime
from enum import Enum


class TestResultCollector:
    def __init__(self):
        self.test_results = []

    def add_test_result(self, test_result):
        self.test_results.append(test_result)

    def write_report(self):
        file_name = '0{}-deem-test.json'.format(str(int(datetime.utcnow().timestamp() * 1e3)))
        file_path = os.path.abspath(os.path.join(__file__, '../../.test_results/', file_name))

        if not os.path.exists(os.path.dirname(file_path)):
            try:
                os.makedirs(os.path.dirname(file_path))
            except OSError as exc:
                if exc.errno != errno.EEXIST:
                    raise

        test_results_file = open(file_path, "w")
        test_results_file.write(json.dumps(self.test_results))
        test_results_file.close()


class BaseTest(unittest.TestCase):

    def setUp(self):
        if not hasattr(unittest.TestCase, 'test_result_collector'):
            test_result_collector = TestResultCollector()
            unittest.TestCase.test_result_collector = test_result_collector

            def shutdown_func():
                test_result_collector.write_report()

            atexit.register(shutdown_func)

        self.test_result_collector = unittest.TestCase.test_result_collector

    def __init__(self, method_name='runTest'):
        super().__init__(method_name)

    def _get_status(self):
        status = 'Passed' if self._outcome.success else 'Failed'
        for method, error in self._outcome.errors:
            if error:
                (error_class, error, trace_back) = error
                if error_class is not AssertionError:
                    status = 'Error'
                    break
        return status

    def _produce_test_result(self):
        return {
            'className': type(self).__name__,
            'methodName': self._testMethodName,
            'status': self._get_status(),
            'timestamp': str(int(datetime.utcnow().timestamp() * 1e3)),
            'score': None
        }

    def doCleanups(self):
        clean_up_result = super().doCleanups()
        self.test_result_collector.add_test_result(self._produce_test_result())
        return clean_up_result


class TestType(Enum):
    PUBLIC = 'Public'
    FUNCTIONAL = 'Functional'
    SIGNAL = 'Signal'


class ScoredTest(BaseTest):

    def __init__(self, method_name='runTest'):
        super().__init__(method_name)
        self.test_type = TestType.PUBLIC
        self.test_weight = 0
        self.test_signal = None

    def _produce_test_result(self):
        test_result = super()._produce_test_result()
        test_result['score'] = {
            'testType': self.test_type.value,
            'testWeight': self.test_weight,
            'testSignal': self.test_signal
        }
        return test_result
