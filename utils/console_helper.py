import os
import subprocess
from models.testcase import TestCase

def clear_screen():
    if os.name == "nt":
        subprocess.run(["cmd", "/c", "cls"], check=False)
    else:
        subprocess.run(["clear"], check=False)

def pause() -> None:
    input("\nPress ENTER to continue...")

def display_test_case(tc: TestCase) -> None:
    print(f"ID: {tc.id}\n"
        f"Title: {tc.title}\n"
        f"Description: {tc.description}\n"
        f"Expected result: {tc.expected_result}\n"
        f""
        )