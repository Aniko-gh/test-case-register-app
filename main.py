from repositories.testcase_repository import TestCaseRepository
from services.testcase_service import TestCaseService
from dialogs.testcase_dialog import TestCaseDialog

class App:
    def __init__(self) -> None:
        self._repository = TestCaseRepository()
        self._service = TestCaseService(self._repository)
        self._dialog = TestCaseDialog(self._service)

    def main(self) -> None:
        self._dialog.start()

if __name__ == "__main__":
    app = App()
    app.main()