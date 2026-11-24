from dataclasses import dataclass

@dataclass (frozen=True)
class TestCaseRequest:
    __test__ = False
    title : str
    description : str
    expected_result : str    