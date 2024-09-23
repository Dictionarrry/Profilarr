from extract import get_custom_format, get_regex
import re
import sys

# ANSI escape codes for colors
GREEN = '\033[92m'
RED = '\033[91m'
RESET = '\033[0m'

good_matches = [
    "Click.and.Collect.2018.1080p.AMZN.WEB-DL.DD+.2.0.H.264-Ralphy.mkv",
    "While.We.Watched.2023.1080p.AMZN.WEB-DL.DD+.5.1.H.265-Ralphy.mkv",
    "The.Office.US.S04E01E02.1080P.BluRay.DD.5.1.X265-RalphyP.mkv",
    "Spotlight.2015.1080P.BluRay.DD.5.1.X265-Ralphy",
    "The.Bourne.Supremacy.2004.1080p.BluRay.DD+.5.1.X265-Ralphy.mkv"
]

bad_matches = [
    "None :)"
]

def Ralphy(debug_level=0):
    # Get the custom formats for "Ralphy" from both Radarr and Sonarr
    Ralphy_radarr = get_custom_format("Ralphy", "radarr", debug_level)
    Ralphy_sonarr = get_custom_format("Ralphy", "sonarr", debug_level)

    # Extract the regex values for both Radarr and Sonarr using get_regex
    Ralphy_value_radarr = get_regex(Ralphy_radarr, "Ralphy", debug_level)
    Ralphy_value_sonarr = get_regex(Ralphy_sonarr, "Ralphy", debug_level)

    # Replace the negative lookbehind with a negative lookahead
    Ralphy_value_radarr = Ralphy_value_radarr.replace(r"(?<=^|[\s.-])", r"(?:^|[\s.-])")
    Ralphy_value_sonarr = Ralphy_value_sonarr.replace(r"(?<=^|[\s.-])", r"(?:^|[\s.-])")

    if debug_level > 0:
        print(f"Testing with regex: {Ralphy_value_radarr}")

    # Compare Radarr and Sonarr Ralphy regex values
    if Ralphy_value_radarr != Ralphy_value_sonarr:
        print("Test Failed: regex value not same.")
        print(f"Radarr regex: {Ralphy_value_radarr}")
        print(f"Sonarr regex: {Ralphy_value_sonarr}")
        sys.exit(1)

    good_matches_passed = []
    good_matches_failed = []
    bad_matches_passed = []
    bad_matches_failed = []

    print("Checking good matches:")
    # Test good matches
    for release in good_matches:
        if re.search(Ralphy_value_radarr, release, re.IGNORECASE):
            good_matches_passed.append(release)
            print(f"  - {release}: {GREEN}Passed{RESET}")
        else:
            good_matches_failed.append(release)
            print(f"  - {release}: {RED}Failed{RESET}")

    print("\nChecking bad matches:")
    # Test bad matches
    for release in bad_matches:
        if re.search(Ralphy_value_radarr, release, re.IGNORECASE):
            bad_matches_passed.append(release)
            print(f"  - {release}: {RED}Failed{RESET}")
        else:
            bad_matches_failed.append(release)
            print(f"  - {release}: {GREEN}Passed{RESET}")

    print("\nFailed matches:")
    for release in good_matches_failed + bad_matches_passed:
        print(f"  - {release}")

    total_matches = len(good_matches) + len(bad_matches)
    passed_matches = len(good_matches_passed) + len(bad_matches_failed)
    success_rate = (passed_matches / total_matches) * 100

    print("\nStats:")
    print(f"Total: {total_matches}")
    print(f"Bad: {len(bad_matches_passed) + len(good_matches_failed)}")
    print(f"Rate: {success_rate:.2f}%")

    if success_rate >= 99.8:
        print("Test Passed")
        return True
    else:
        print("Test Failed")
        return False 