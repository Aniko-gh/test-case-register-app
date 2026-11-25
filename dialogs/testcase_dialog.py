from services.testcase_service import TestCaseService
from models.testcase_request import TestCaseRequest

from utils.console_helper import pause, display_test_case, clear_screen

class TestCaseDialog:
    __test__ = False
    def __init__(self, testcase_service : TestCaseService):
        self.__service : TestCaseService = testcase_service

    def start(self) -> None:
        while True:
            self.show_menu()
            option = input("Choose an option: ").strip()

            if option == "1":
                self.create_test_case()
            elif option == "2":
                self.list_test_cases()
            elif option == "0":
                print("Exiting programme...")
                break
            else:
                print("Invalid option. Try again.")
                pause()

    def show_menu(self) -> None:
        clear_screen()
        print("")
        print("   TEST CASE MANAGEMENT   ")
        print("1. Create Test Case")
        print("2. List Test Cases")
        print("0. Exit")
        print("")

    def _prompt_mandatory(self, prompt_text: str) -> str:
        while True:
            value = input(prompt_text).strip()
            if value:
                return value
            print("Fill in all mandatory fields. Please try again.")
            print("")

    def create_test_case(self) -> None:
        clear_screen()
        print("")
        print(f"   CREATE TEST CASE   ")
        print("")

        title = self._prompt_mandatory("Enter title: ")
        
        description = self._prompt_mandatory("Enter description: ")
        
        expected_result = self._prompt_mandatory("Enter expected result: ")
        
        test_case_request = TestCaseRequest(title=title, description=description, expected_result=expected_result)

        result = self.__service.create_test_case(test_case_request)

        if not result.succeeded:
            print("")
            print(result.message)
        else:
            for tc in result.result:
                print("")
                print(f"Test case has been added.")
                print("")
                display_test_case(tc)
        pause()

    def list_test_cases(self) -> None:
        clear_screen()
        print("")
        print(f"   LIST TEST CASES   ")
        print("")
        
        result = self.__service.get_test_cases()

        if not result.succeeded:
            print(result.message)
        else:    
            for test_case in result.result:
                display_test_case(test_case)
        pause()