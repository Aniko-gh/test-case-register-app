from dataclasses import dataclass, field
from models.test_case import TestCase

@dataclass(frozen = True)
class TestCaseResult:
    succeeded : bool
    message : str | None = None
    result : list[TestCase] = field(default_factory=list)