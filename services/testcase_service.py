from repositories.testcase_repository import TestCaseRepository
from models.testcase_request import TestCaseRequest
from models.testcase_result import TestCaseResult
from models.testcase import TestCase

class TestCaseService:
    __test__ = False
    def __init__(self, testcase_repository : TestCaseRepository):
        self.__repository : TestCaseRepository = testcase_repository

    def create_test_case(self, testcase_request : TestCaseRequest) -> TestCaseResult:
        title = testcase_request.title.strip()
        description = testcase_request.description.strip()
        expected_result = testcase_request.expected_result.strip()

        if not title or not description or not expected_result:
            return TestCaseResult(succeeded=False, message="Fill in all mandatory fields.")
      
        test_case = TestCase(title, description, expected_result)

        if not self.__repository.try_add(test_case):
            return TestCaseResult(succeeded=False, message="Test case has already been registered.")

        return TestCaseResult(succeeded=True, result=[test_case])
        
    def get_test_cases(self) -> TestCaseResult:
        test_cases = self.__repository.get_all()
        if not test_cases:
            return TestCaseResult(succeeded=False, message="No test case found.")

        return TestCaseResult(succeeded=True, result=test_cases)