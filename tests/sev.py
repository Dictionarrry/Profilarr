from extract import get_custom_format, get_regex
import re
import sys

# ANSI escape codes for colors
GREEN = '\033[92m'
RED = '\033[91m'
BLUE = '\033[94m'
ORANGE = '\033[38;5;208m'
RESET = '\033[0m'


good_matches = [
    "Narcos - S03.E02 - The Cali KGB 1080p BDRip x265 DTS-HD MA 5.1 Kira [SEV]",
    "Invincible - Season - 02 [2023-2024] 1080p AMZN WebRip x265 DD+ 5.1 Kira [SEV]",
    "The Hangover Part III 2013 1080p BluRay DTS-HD MA 5.1 x265-Kira",
    "Aliens (1986) Special Edition Open Matte (1080p BluRay x265 SDR DTS-HD MA 5.1 English - Kira SEV)",
    "Convicting A Murderer [2023] S01 1080p DW+ WebRip x265 AAC 2.0 Kira [SEV]",
    "Titans S04 1080p BluRay AAC 5.1 x265-Kira SEV",
    "Captain America : The First Avenger 2011 1080p BluRay TrueHD 7.1 Atmos x265-D0ct0rLew",
    "Moon Knight S01 1080p UHD BluRay x265 10bit TrueHD Atmos 7.1 - D0ct0rLew SEV"
]

bad_matches = [
    "Asp-Heavens_Seven-(AVCD-61385)-JP-CD-2024-DARKAUDiO",
    "Sevana-Keep Going Chosen-Single-WEB-2024-PaB",
    "Spencer.Ellsworth-Starfire.Shadow.Sun.Seven.The.Starfire.Trilogy.2.2017.RETAIL.EPUB.eBook-CTO"
]

def sev(debug_level=0):
    # Get the custom formats for "sev" from both Radarr and Sonarr
    sev_radarr = get_custom_format("sev", "radarr", debug_level)
    sev_sonarr = get_custom_format("sev", "sonarr", debug_level)

    # Extract the regex values for both Radarr and Sonarr using get_regex
    sev_value_radarr = get_regex(sev_radarr, "sev", debug_level)
    sev_value_sonarr = get_regex(sev_sonarr, "sev", debug_level)

    # Extract the regex values for both Radarr and Sonarr using get_regex
    UTR_value_radarr = get_regex(sev_radarr, "UTR", debug_level)
    UTR_value_sonarr = get_regex(sev_sonarr, "UTR", debug_level)

    # Replace the negative lookbehind with a negative lookahead
    sev_value_radarr = sev_value_radarr.replace(r"(?<=^|[\s.-])", r"(?:^|[\s.-])")
    sev_value_sonarr = sev_value_sonarr.replace(r"(?<=^|[\s.-])", r"(?:^|[\s.-])")


    if debug_level > 0:
        print(f"Testing with SEV regex: {ORANGE}{sev_value_radarr}{RESET}\n")
        print(f"Testing with UTR regex: {ORANGE}{UTR_value_radarr}{RESET}\n")

    # Compare Radarr and Sonarr sev regex values
    if sev_value_radarr != sev_value_sonarr:
        print("Test Failed: regex value not same.")
        print(f"Radarr regex: {sev_value_radarr}")
        print(f"Sonarr regex: {sev_value_sonarr}")

    # Compare Radarr and Sonarr UTR regex values
    if UTR_value_radarr != UTR_value_sonarr:
        print("Test Failed: regex value not same.")
        print(f"Radarr regex: {UTR_value_radarr}")
        print(f"Sonarr regex: {UTR_value_sonarr}")

    good_matches_passed = []
    good_matches_failed = []
    bad_matches_passed = []
    bad_matches_failed = []

    print("Checking good matches:")
    # Test good matches
    for release in good_matches:
        if re.search(sev_value_radarr, release, re.IGNORECASE):
            good_matches_passed.append(release)
            print(f"  - {release}: {GREEN}Passed{RESET}")
        else:
            good_matches_failed.append(release)
            print(f"  - {release}: {RED}Failed{RESET}")

    print("\nChecking bad matches:")
    # Test bad matches
    for release in bad_matches:
        if re.search(sev_value_radarr, release, re.IGNORECASE):
            bad_matches_passed.append(release)
            print(f"  - {release}: {RED}Failed{RESET}")
        else:
            bad_matches_failed.append(release)
            print(f"  - {release}: {GREEN}Passed{RESET}")

    print("\nFailed matches:")
    if good_matches_failed or bad_matches_passed:
        for release in good_matches_failed + bad_matches_passed:
            print(f"  - {release}")
    else:
        print(f"{GREEN}None, Great Job! :){RESET}")

    total_matches = len(good_matches) + len(bad_matches)
    passed_matches = len(good_matches_passed) + len(bad_matches_failed)
    success_rate = (passed_matches / total_matches) * 100

    print("\nStats:")
    print(f"Total: {total_matches}")
    print(f"Bad: {len(bad_matches_passed) + len(good_matches_failed)}")
    print(f"Rate: {success_rate:.2f}%")

    if success_rate >= 99.8:
        return True
    else:
        return False