from dataclasses import dataclass

@dataclass (frozen=True)
class TestCaseRequest:
    title : str
    description : str
    expected_result : str    