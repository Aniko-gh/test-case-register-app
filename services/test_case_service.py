from repositories.test_case_repository import TestCaseRepository
from models.test_case_request import TestCaseRequest
from models.test_case_result import TestCaseResult
from models.test_case import TestCase

class TestCaseService:
    def __init__(self, test_case_repository : TestCaseRepository):
        self.__repository : TestCaseRepository = test_case_repository

    def create_test_case(self, test_case_request : TestCaseRequest) -> TestCaseResult:
        title = test_case_request.title.strip()
        description = test_case_request.description.strip()
        expected_result = test_case_request.expected_result.strip()

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