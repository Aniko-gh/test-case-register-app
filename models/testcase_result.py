from dataclasses import dataclass, field
from models.testcase import TestCase

@dataclass(frozen = True)
class TestCaseResult:
    __test__ = False
    succeeded : bool
    message : str | None = None
    result : list[TestCase] = field(default_factory=list)