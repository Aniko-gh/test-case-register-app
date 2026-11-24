from unittest.mock import Mock

import pytest

from services.testcase_service import TestCaseService
from repositories.testcase_repository import TestCaseRepository
from models.testcase_request import TestCaseRequest
from models.testcase_result import TestCaseResult
from models.testcase import TestCase

@pytest.fixture
def repository() -> Mock:
    return Mock(spec=TestCaseRepository)

@pytest.fixture
def service(repository : Mock) -> TestCaseService:
    return TestCaseService(repository)

def test_create_test_case__should_succeeded__when_valid_request():
    repository = TestCaseRepository()
    service = TestCaseService(repository)
    request = TestCaseRequest(
        title="  Kontaktuppgifter på hemsidan  ",
        description="  Kontrollera att alla kontaktuppgifter finns på hemsidans sidfot och att de är de som bestämts av företaget.  ",
        expected_result="  Kontaktuppgifterna visas på hemsidans sidfot och stämmer överens med dem som företaget har angett.  "
    )

    result = service.create_test_case(request)

    assert result.succeeded is True
    assert len(result.result) == 1
    assert result.result[0].title == "Kontaktuppgifter på hemsidan"
    assert result.result[0].description == "Kontrollera att alla kontaktuppgifter finns på hemsidans sidfot och att de är de som bestämts av företaget."
    assert result.result[0].expected_result == "Kontaktuppgifterna visas på hemsidans sidfot och stämmer överens med dem som företaget har angett."
    assert result.result[0].id == "TC-001"

@pytest.mark.parametrize(
    "title, description, expected_result",
    [
        ("",
        "Kontrollera att alla kontaktuppgifter finns på hemsidans sidfot och att de är de som bestämts av företaget.",
        "Kontaktuppgifterna visas på hemsidans sidfot och stämmer överens med dem som företaget har angett."),
        ("   ",
        "Kontrollera att alla kontaktuppgifter finns på hemsidans sidfot och att de är de som bestämts av företaget.",
        "Kontaktuppgifterna visas på hemsidans sidfot och stämmer överens med dem som företaget har angett."),
        ("Kontaktuppgifter på hemsidan",
        "",
        "Kontaktuppgifterna visas på hemsidans sidfot och stämmer överens med dem som företaget har angett."),
        ("Kontaktuppgifter på hemsidan",
        "   ",
        "Kontaktuppgifterna visas på hemsidans sidfot och stämmer överens med dem som företaget har angett."),
        ("Kontaktuppgifter på hemsidan",
        "Kontrollera att alla kontaktuppgifter finns på hemsidans sidfot och att de är de som bestämts av företaget.",
        ""),
        ("Kontaktuppgifter på hemsidan",
        "Kontrollera att alla kontaktuppgifter finns på hemsidans sidfot och att de är de som bestämts av företaget.",
        "   "),
    ],
)
def test_create_test_case__should_fail__when_mandatory_field_empty(title, description, expected_result):
    repository = TestCaseRepository()
    service = TestCaseService(repository)
    request = TestCaseRequest(
        title=title,
        description=description,
        expected_result=expected_result,
    )

    result = service.create_test_case(request)

    assert result.succeeded is False
    assert result.message == "Fill in all mandatory fields."
    assert len(repository.get_all()) == 0

def test_create_test_case__should_fail__if_test_case_already_exists():
    repository = TestCaseRepository()
    service =TestCaseService(repository)
    request = TestCaseRequest(
        title="Kontaktuppgifter på hemsidan",
        description="Kontrollera att alla kontaktuppgifter finns på hemsidans sidfot och att de är de som bestämts av företaget.",
        expected_result="Kontaktuppgifterna visas på hemsidans sidfot och stämmer överens med dem som företaget har angett.",
    )
    service.create_test_case(request)

    result = service.create_test_case(request)

    assert result.succeeded is False
    assert result.message == "Test case has already been registered."
    assert len(repository.get_all()) == 1
    

def test_get_test_cases__should_return_empty_list__when_no_test_case_has_been_added():
    repository = TestCaseRepository()
    service = TestCaseService(repository)
    
    result = service.get_test_cases()

    assert result.succeeded is False
    assert result.message == "No test case found."


def test_get_test_cases__should_return_list_of_test_cases__when_test_cases_exist():
    repository = TestCaseRepository()
    service = TestCaseService(repository)
    service.create_test_case(TestCaseRequest(
        "Kontaktuppgifter på hemsidan",
        "Kontrollera att alla kontaktuppgifter finns på hemsidans sidfot och att de är de som bestämts av företaget.",
        "Kontaktuppgifterna visas på hemsidans sidfot och stämmer överens med dem som företaget har angett.")
    )
    service.create_test_case(TestCaseRequest(
        "Kontaktuppgifter på produktsidan",
        "Kontrollera att alla kontaktuppgifter finns på hemsidans sidfot och att de är de som bestämts av företaget.",
        "Kontaktuppgifterna visas på hemsidans sidfot och stämmer överens med dem som företaget har angett.")
        )

    result = service.get_test_cases()

    assert result.succeeded is True
    assert len(result.result) == 2
    assert result.result[0].title == "Kontaktuppgifter på hemsidan"
    assert result.result[1].title == "Kontaktuppgifter på produktsidan"
