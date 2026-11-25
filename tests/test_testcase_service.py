from unittest.mock import Mock

import pytest

from services.testcase_service import TestCaseService
from repositories.testcase_repository import TestCaseRepository
from models.testcase_request import TestCaseRequest
from models.testcase import TestCase

@pytest.fixture
def repository() -> Mock:
    return Mock(spec=TestCaseRepository)

@pytest.fixture
def service(repository : Mock) -> TestCaseService:
    return TestCaseService(repository)

def test_create_test_case__should_succeeded__when_valid_request(service : TestCaseService, repository : Mock) -> None:
    repository.try_add.return_value = True
    request = TestCaseRequest(
        title="  Kontaktuppgifter på hemsidan  ",
        description="  Alla kontaktuppgifter finns på hemsidans sidfot och att de är de som bestämts av företaget.  ",
        expected_result="  Kontaktuppgifterna visas på hemsidans sidfot och stämmer överens med dem som företaget har angett.  "
    )

    result = service.create_test_case(request)

    assert result.succeeded is True
    assert result.message is None
    assert len(result.result) == 1

    test_case = result.result[0]

    assert test_case.title == "Kontaktuppgifter på hemsidan"
    assert test_case.description == "Alla kontaktuppgifter finns på hemsidans sidfot och att de är de som bestämts av företaget."
    assert test_case.expected_result == "Kontaktuppgifterna visas på hemsidans sidfot och stämmer överens med dem som företaget har angett."
        
    repository.try_add.assert_called_once()


@pytest.mark.parametrize(
    "title, description, expected_result",
    [
        ("",
        "Alla kontaktuppgifter finns på hemsidans sidfot och att de är de som bestämts av företaget.",
        "Kontaktuppgifterna visas på hemsidans sidfot och stämmer överens med dem som företaget har angett."),
        ("   ",
        "Alla kontaktuppgifter finns på hemsidans sidfot och att de är de som bestämts av företaget.",
        "Kontaktuppgifterna visas på hemsidans sidfot och stämmer överens med dem som företaget har angett."),
        ("Kontaktuppgifter på hemsidan",
        "",
        "Kontaktuppgifterna visas på hemsidans sidfot och stämmer överens med dem som företaget har angett."),
        ("Kontaktuppgifter på hemsidan",
        "   ",
        "Kontaktuppgifterna visas på hemsidans sidfot och stämmer överens med dem som företaget har angett."),
        ("Kontaktuppgifter på hemsidan",
        "Alla kontaktuppgifter finns på hemsidans sidfot och att de är de som bestämts av företaget.",
        ""),
        ("Kontaktuppgifter på hemsidan",
        "Alla kontaktuppgifter finns på hemsidans sidfot och att de är de som bestämts av företaget.",
        "   "),
    ],
)

def test_create_test_case__should_fail__when_mandatory_field_empty(service : TestCaseService, repository : Mock, title : str, description : str, expected_result : str) -> None:
    request = TestCaseRequest(
        title=title,
        description=description,
        expected_result=expected_result,
    )

    result = service.create_test_case(request)

    assert result.succeeded is False
    assert result.message == "Fill in all mandatory fields."
    
    repository.try_add.assert_not_called()


def test_create_test_case__should_fail__if_test_case_already_exists(service : TestCaseService, repository : Mock) -> None:
    repository.try_add.return_value = False
    request = TestCaseRequest(
        title="Kontaktuppgifter på hemsidan",
        description="Alla kontaktuppgifter finns på hemsidans sidfot och att de är de som bestämts av företaget.",
        expected_result="Kontaktuppgifterna visas på hemsidans sidfot och stämmer överens med dem som företaget har angett.",
    )
    
    result = service.create_test_case(request)

    assert result.succeeded is False
    assert result.message == "Test case has already been registered."
    
    repository.try_add.assert_called_once()

    
def test_get_test_cases__should_return_empty_list__when_no_test_case_added(service : TestCaseService, repository : Mock) -> None:
    repository.get_all.return_value = []
    
    result = service.get_test_cases()

    assert result.succeeded is False
    assert result.message == "No test case found."
    
    repository.get_all.assert_called_once()


def test_get_test_cases__should_return_list_of_test_cases__when_test_cases_exist(service : TestCaseService, repository : Mock) -> None:
    repository.get_all.return_value = [
        TestCase(
            title = "Kontaktuppgifter på hemsidan",
            description = "Alla kontaktuppgifter finns på hemsidans sidfot och att de är de som bestämts av företaget.",
            expected_result = "Kontaktuppgifterna visas på hemsidans sidfot och stämmer överens med dem som företaget har angett.",
        ),
        TestCase(
            title = "Kontaktuppgifter på produktsidan",
            description = "Alla kontaktuppgifter finns på produktsidans sidfot och att de är de som bestämts av företaget.",
            expected_result = "Kontaktuppgifterna visas på produktsidans sidfot och stämmer överens med dem som företaget har angett.",
        ),
    ]    
    
    result = service.get_test_cases()

    assert result.succeeded is True
    assert result.result[0].title == "Kontaktuppgifter på hemsidan"
    assert result.result[1].title == "Kontaktuppgifter på produktsidan"
    
    repository.get_all.assert_called_once()