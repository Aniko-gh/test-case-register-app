from dataclasses import dataclass, field

@dataclass
class TestCase:
    __test__ = False
    title : str
    description : str
    expected_result : str
    id: str | None = field(default=None, init=False)
    