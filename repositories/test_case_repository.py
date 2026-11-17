from models.test_case import TestCase

class TestCaseRepository:
    def __init__(self):
        self.__test_cases : list[TestCase] = []
        self._next_id: int = 1
      
    def try_add(self, test_case : TestCase) -> bool:
        if any(tc.title == test_case.title for tc in self.__test_cases):
            return False
        test_case.id = (f"TC-{self._next_id:03d}")
        self._next_id += 1
        
        self.__test_cases.append(test_case)
        return True
    
    def get_all(self) -> list[TestCase]:
        return self.__test_cases.copy()