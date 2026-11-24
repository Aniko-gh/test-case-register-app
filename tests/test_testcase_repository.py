import pytest

from models.testcase import TestCase
from repositories.testcase_repository import TestCaseRepository

def test_try_add__should_add_test_case_to_list__return_true_and_assign_id():
    
    repository = TestCaseRepository()
    test_case = TestCase(
        "Kontaktuppgifter på hemsidan",
        "Kontrollera att alla kontaktuppgifter finns på hemsidans sidfot och att de är de som bestämts av företaget.",
        "Kontaktuppgifterna visas på hemsidans sidfot och stämmer överens med dem som företaget har angett."
        )

    result = repository.try_add(test_case)

    assert result is True
    assert test_case.id == "TC-001"
    assert repository.get_all() == [test_case]

def test_try_add__should_increment_id__when_multiple_test_cases_added():
    
    repository = TestCaseRepository()
    test_case_1 = TestCase(
        title="Kontaktuppgifter på hemsidan",
        description="Kontrollera att alla kontaktuppgifter finns på hemsidans sidfot och att de är de som bestämts av företaget.",
        expected_result="Kontaktuppgifterna visas på hemsidans sidfot och stämmer överens med dem som företaget har angett.")
    test_case_2 = TestCase(
        title="Kontaktuppgifter på produktsidan",
        description="Kontrollera att alla kontaktuppgifter finns på produktsidans sidfot och att de är de som bestämts av företaget.",
        expected_result="Kontaktuppgifterna visas på produktsidans sidfot och stämmer överens med dem som företaget har angett.")
    
    repository.try_add(test_case_1)
    repository.try_add(test_case_2)

    assert test_case_1.id == "TC-001"
    assert test_case_2.id == "TC-002"
    assert len(repository.get_all()) == 2

def test_try_add__should_reject_duplicate_title__return_false():

    repository = TestCaseRepository()
    test_case_1 = TestCase(
            title="Kontaktuppgifter på hemsidan",
            description="Kontrollera att alla kontaktuppgifter finns på hemsidans sidfot och att de är de som bestämts av företaget.",
            expected_result="Kontaktuppgifterna visas på hemsidans sidfot och stämmer överens med dem som företaget har angett.")
    test_case_2 = TestCase(
            title="Kontaktuppgifter på hemsidan",
            description="Kontrollera att alla kontaktuppgifter finns på hemsidans sidfot och att de är de som bestämts av företaget.",
            expected_result="Kontaktuppgifterna visas på hemsidans sidfot och stämmer överens med dem som företaget har angett.")
    repository.try_add(test_case_1)

    result = repository.try_add(test_case_2)

    assert result == False
    assert len(repository.get_all()) == 1

def test_try_add__should_not_increment_id__when_duplicate_rejected():

    repository = TestCaseRepository()
    test_case_1 = TestCase(
            title="Kontaktuppgifter på hemsidan",
            description="Kontrollera att alla kontaktuppgifter finns på hemsidans sidfot och att de är de som bestämts av företaget.",
            expected_result="Kontaktuppgifterna visas på hemsidans sidfot och stämmer överens med dem som företaget har angett.")
    test_case_2 = TestCase(
            title="Kontaktuppgifter på hemsidan",
            description="Kontrollera att alla kontaktuppgifter finns på hemsidans sidfot och att de är de som bestämts av företaget.",
            expected_result="Kontaktuppgifterna visas på hemsidans sidfot och stämmer överens med dem som företaget har angett.")
    test_case_3 = TestCase(
            title="Kontaktuppgifter på produktsidan",
            description="Kontrollera att alla kontaktuppgifter finns på produktsidans sidfot och att de är de som bestämts av företaget.",
            expected_result="Kontaktuppgifterna visas på produktsidans sidfot och stämmer överens med dem som företaget har angett.")
        
    repository.try_add(test_case_1)
    repository.try_add(test_case_2)
    repository.try_add(test_case_3)

    assert test_case_1.id == "TC-001"
    assert test_case_3.id == "TC-002"


def test_get_all__should_return_empty_list__when_initialized():

    repository = TestCaseRepository()

    result = repository.get_all()

    assert result == []


def test_get_all__should_return_all_test_cases():

    repository = TestCaseRepository()
    test_case = TestCase(
        "Kontaktuppgifter på hemsidan",
        "Kontrollera att alla kontaktuppgifter finns på hemsidans sidfot och att de är de som bestämts av företaget.",
        "Kontaktuppgifterna visas på hemsidans sidfot och stämmer överens med dem som företaget har angett."
        )
    repository.try_add(test_case)

    result = repository.get_all()

    assert result == [test_case]