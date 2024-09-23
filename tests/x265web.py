from extract import get_custom_format, get_regex
import re
import sys

# ANSI escape codes for colors
GREEN = '\033[92m'
RED = '\033[91m'
RESET = '\033[0m'

good_matches = [
    "Silo (2023) S01 1080p DS4K ATVP WEB-DL DDP 5 1 Atmos English - YELLO",
    "Yuva (2024) Kannada (1080p DS4K WEBRip AMZN x265 HEVC 10bit DDP5.1 ESub M3GAN) [MCX]",
    "Mrs. Davis 2023 S01 1080p DS4K PCOK WEB-DL DDP 5.1 x265 - YELLO",
    "The New Look (2024) S01E01 Just You Wait and See (1080p DS4K ATVP WEBRip x265 10-bit SDR DDP Atmos 5 1 English - DarQ)",
    "Baghead (2024) 1080p DS4K WEB-DL x265 DV HDR10+ DDP 5.1 English-SM737",
    "Bosch.Legacy.2022.S02E03.1080p.DS4K.AMZN.WEB-DL.10bit.DDP5.1.x265-YELLO"
]

bad_matches = [
    "Bird Box (2018) 1080p DS4K NF WEBRip AV1 Opus 5.1 [Retr0]",
    "The Banshees of Inisherin (2022) 1080p DS4K MA WEBRip AV1 Opus 5.1 [Retr0]",
    "Once Upon a Studio (2023) DS4K 1080p DSNP WEBRip AV1 Opus 5.1 [RAV1NE]",
    "24 Jam Bersama Gaspar (2024) INDONESIAN DS4K 1080p NF WEBRip AV1 Opus 5.1 [RAV1NE]",
]

def x265WEB(debug_level=0):
    # Get the custom formats for "x265WEB" from both Radarr and Sonarr
    x265WEB_radarr = get_custom_format("x265 (Web)", "radarr", debug_level)
    x265WEB_sonarr = get_custom_format("x265 (Web)", "sonarr", debug_level)

    # Get the custom formats for "AV1" from both Radarr and Sonarr
    AV1_radarr = get_custom_format("AV1", "radarr", debug_level)
    AV1_sonarr = get_custom_format("AV1", "sonarr", debug_level)

    # Extract the regex values for both Radarr and Sonarr using get_regex
    x265WEB_value_radarr = get_regex(x265WEB_radarr, "x265", debug_level)
    x265WEB_value_sonarr = get_regex(x265WEB_sonarr, "x265", debug_level)

    # Extract the regex values for both Radarr and Sonarr using get_regex
    AV1_value_radarr = get_regex(AV1_radarr, "AV1", debug_level)
    AV1_value_sonarr = get_regex(AV1_sonarr, "AV1", debug_level)

    # Replace the negative lookbehind with a negative lookahead
    x265WEB_value_radarr = x265WEB_value_radarr.replace(r"(?<=^|[\s.-])", r"(?:^|[\s.-])")
    x265WEB_value_sonarr = x265WEB_value_sonarr.replace(r"(?<=^|[\s.-])", r"(?:^|[\s.-])")

    if debug_level > 0:
        print(f"Testing with x265 regex: {x265WEB_value_radarr}")
        print(f"Testing with AV1 regex: {AV1_value_radarr}")

    # Compare Radarr and Sonarr x265WEB regex values
    if x265WEB_value_radarr != x265WEB_value_sonarr:
        print("Test Failed: regex value not same.")
        print(f"Radarr regex: {x265WEB_value_radarr}")
        print(f"Sonarr regex: {x265WEB_value_sonarr}")

    # Compare Radarr and Sonarr AV1 regex values
    if AV1_value_radarr != AV1_value_sonarr:
        print("Test Failed: regex value not same.")
        print(f"Radarr regex: {AV1_value_radarr}")
        print(f"Sonarr regex: {AV1_value_sonarr}")

    good_matches_passed = []
    good_matches_failed = []
    bad_matches_passed = []
    bad_matches_failed = []

    print("Checking good matches:")
    # Test good matches
    for release in good_matches:
        if re.search(x265WEB_value_radarr, release, re.IGNORECASE):
            good_matches_passed.append(release)
            print(f"  - {release}: {GREEN}Passed{RESET}")
        else:
            good_matches_failed.append(release)
            print(f"  - {release}: {RED}Failed{RESET}")

    print("\nChecking bad matches:")
    # Test bad matches
    for release in bad_matches:
        if re.search(AV1_value_radarr, release, re.IGNORECASE):
            bad_matches_passed.append(release)
            print(f"  - {release}: {GREEN}Passed{RESET}")
        else:
            bad_matches_failed.append(release)
            print(f"  - {release}: {RED}Failed{RESET}")

    # Reporting failed matches
    print("\nFailed matches:")
    for release in good_matches_failed + bad_matches_failed:
        print(f"  - {release}")

    total_matches = len(good_matches) + len(bad_matches)
    passed_matches = len(good_matches_passed) + len(bad_matches_passed)
    success_rate = (passed_matches / total_matches) * 100

    print("\nStats:")
    print(f"Total: {total_matches}")
    print(f"Bad: {len(bad_matches_failed) + len(good_matches_failed)}")
    print(f"Rate: {success_rate:.2f}%")

    if success_rate >= 99.8:
        print("Test Passed")
        return True
    else:
        print("Test Failed")
        return False
