import sys
from roku import roku
from h265verify import h265
from qxr import qxr
from x265web import x265WEB
from taoe import taoe
from ralphy import Ralphy
from av1 import AV1
from sev import sev
from upscale import Upscaled
# ... import other test functions

# ANSI escape codes for colors
BLUE = '\033[94m'
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
RESET = '\033[0m'

def run_tests():
    tests = [
        ("ROKU", roku),
        ("h265 Verified Groups", h265),
        ("QxR Groups", qxr),
        ("x265 (Web)", x265WEB),
        ("TAoE Groups", taoe),
        ("Ralphy", Ralphy),
        ("AV1", AV1),
        ("SEV", sev),
        ("Upscaled", Upscaled),


        # ... add other test functions
    ]

    for test_name, test_func in tests:
        print(f"{BLUE}=============================================={RESET}")
        print(f"{BLUE}Running test: {test_name}{RESET}")
        print(f"{BLUE}=============================================={RESET}\n")
        
        test_result = test_func(debug_level=1)

        if test_result:
            print()
            print(f"{GREEN}=============================================={RESET}")
            print(f"{GREEN}Passed Test: {test_name}{RESET}")
            print(f"{GREEN}=============================================={RESET}\n")
            continue
        else:
            print()
            print(f"{RED}=============================================={RESET}")
            print(f"{RED}Failed Test: {test_name}{RESET}")
            print(f"{RED}=============================================={RESET}\n")
            sys.exit(1)

if __name__ == "__main__":
    run_tests()
