from extract import get_custom_format, get_regex
import re
import sys

# ANSI escape codes for colors
GREEN = '\033[92m'
RED = '\033[91m'
RESET = '\033[0m'

def h265(debug_level=0):
    # Get the custom formats for "h265" from both Radarr and Sonarr
    h265_radarr = get_custom_format("h265", "radarr", debug_level)
    h265_sonarr = get_custom_format("h265", "sonarr", debug_level)

    # Extract the regex values for verified groups
    h265_value_radarr = get_regex(h265_radarr, "verified groups", debug_level)
    h265_value_sonarr = get_regex(h265_sonarr, "verified groups", debug_level)

    # Replace the negative lookbehind with a negative lookahead
    h265_value_radarr = h265_value_radarr.replace("(?<=^|[\\s.-])", "(?:^|[\\s.-])")
    h265_value_sonarr = h265_value_sonarr.replace("(?<=^|[\\s.-])", "(?:^|[\\s.-])")

    if debug_level > 0:
        print(f"Testing with regex: {h265_value_radarr}")

    # Compare Radarr and Sonarr h265 regex values
    if h265_value_radarr != h265_value_sonarr:
        print("Test Failed: regex value not same.")
        print(f"Radarr regex: {h265_value_radarr}")
        print(f"Sonarr regex: {h265_value_sonarr}")
        sys.exit(1)

    radarr_good_matches = [
        "The Batman (2022) (1080p HMAX WEB-DL H265 SDR DDP Atmos 5.1 English - HONE)",
        "King Richard (2021) (1080p HMAX WEB-DL H265 SDR DDP Atmos 5.1 English - HONE)",
        "The Survivor (2021) (1080p HMAX WEB-DL H265 SDR DD 5.1 English - HONE)",
        "Transformers (2007) (1080p HMAX WEB-DL H265 SDR DD 5.1 English - BLAZE)",
        "Significant Other (2022) (1080p AMZN WEB-DL H265 SDR DDP 5.1 English - Yoyo)",
        "The NeverEnding Story (1984) (1080p HMAX WEB-DL H265 SDR DD 5.1 English - SiGLA)",
        "Monster-in-Law (2005) (1080p HMAX WEB-DL H265 SDR DD 5.1 English - SiGLA)",
        "Rocky III (1982) (1080p AMZN WEB-DL H265 SDR DDP 5.1 English - AnoZu)",
        "Samaritan (2022) (1080p AMZN WEB-DL H265 SDR DDP 5.1 English - GRiMM)",
        "The Old Guard (2020) (1080p NF WEB-DL H265 SDR DDP Atmos 5.1 English - GRiMM)"
    ]
    radarr_bad_matches = [
        "The Tinder Swindler (2022) (1080p NF WEB-DL H265 SDR DDP Atmos 5.1 English - TEPES)",
        "The Greatest Lie Ever Sold: George Floyd and the Rise of BLM (2022) (1080p WEB-DL H265 SDR AAC 2.0 English - NOGROUP)",
        "Baccano! (2007) S01 (1080p BluRay H265 SDR OPUS 2.0 English - NOGROUP)",
        "Bhool Bhulaiyaa 2 (2022) (1080p NF WEB-DL H265 SDR DDP 5.1 Hindi - ElecTr0n)",
        "Ek Villain Returns (2022) (1080p NF WEB-DL H265 SDR DDP 5.1 Hindi - SKUI)"
    ]
    sonarr_good_matches = [
        "Minx (2022) S01 (1080p HMAX WEB-DL H265 SDR DD 5.1 English - HONE)",
        "We Own This City (2022) S01E01 (1080p HMAX WEB-DL H265 SDR DD 5.1 English - HONE)",
        "My Brilliant Friend (2018) S01 (1080p HMAX WEB-DL H265 SDR DD 5.1 Italian - HONE)",
        "The Goldbergs (2013) S09 (1080p HULU WEB-DL H265 SDR DDP 5.1 English - BLAZE)",
        "Atlanta (2016) S01 (1080p HULU WEB-DL H265 SDR DDP 5.1 English - Yoyo)",
        "Friday Night Lights (2006) S01 (1080p AMZN WEB-DL H265 SDR DDP 5.1 English - SiGMA)",
        "Defiance (2013) S03 (1080p AMZN WEB-DL H265 SDR DDP 5.1 English - SiGMA)",
        "Happy Valley (2014) S01 (1080p iP WEB-DL H265 SDR AAC 2.0 English - HECATE)",
        "Shaun the Sheep (2007) S05 (1080p iP WEB-DL H265 SDR AAC 2.0 English - HECATE)",
        "Skins (2007) S01 (1080p AMZN WEB-DL H265 SDR DDP 2.0 English - DarQ)",
        "Wheeler Dealers (2003) S17 (1080p AMZN WEB-DL H265 SDR DDP 2.0 English - DarQ)",
        "Supernatural (2005) S04 (1080p AMZN WEB-DL H265 SDR DDP 5.1 English - AnoZu)",
        "DC's Stargirl (2020) S01 (1080p AMZN WEB-DL H265 SDR DDP 5.1 English - YELLO)",
        "American Horror Story (2011) S12E01 (1080p HULU WEB-DL H265 SDR DDP 5.1 English - YELLO)"
    ]
    sonarr_bad_matches = [
        "House of the Dragon (2022) S00E24 (1080p HMAX WEB-DL H265 SDR DD 2.0 English - PbP)",
        "Daybreak (2019) S01 (1080p NF WEB-DL x265 SDR H265 DDP Atmos 5.1 English - t3nzin)",
        "Superjail! (2008) S03 (1080p AMZN WEB-DL H265 SDR DD 5.1 English - DiNGUS)"
    ]


    failed_good_matches = []
    failed_bad_matches = []

    # Print Radarr Good Matches
    print("\nRadarr Releases:")
    print("----------------")
    print("Should Match:")
    for term in radarr_good_matches:
        if re.search(h265_value_radarr, term, re.IGNORECASE):
            print(f"  - {term}: {GREEN}Passed{RESET}")
        else:
            failed_good_matches.append(("Radarr", term))
            print(f"  - {term}: {RED}Failed{RESET}")

    # Print Radarr Bad Matches
    print("\nShould NOT Match:")
    for term in radarr_bad_matches:
        if not re.search(h265_value_radarr, term, re.IGNORECASE):
            print(f"  - {term}: {GREEN}Passed{RESET}")
        else:
            failed_bad_matches.append(("Radarr", term))
            print(f"  - {term}: {RED}Failed{RESET}")

    # Print Sonarr Good Matches
    print("\nSonarr Releases:")
    print("----------------")
    print("Should Match:")
    for term in sonarr_good_matches:
        if re.search(h265_value_sonarr, term, re.IGNORECASE):
            print(f"  - {term}: {GREEN}Passed{RESET}")
        else:
            failed_good_matches.append(("Sonarr", term))
            print(f"  - {term}: {RED}Failed{RESET}")

    # Print Sonarr Bad Matches
    print("\nShould NOT Match:")
    for term in sonarr_bad_matches:
        if not re.search(h265_value_sonarr, term, re.IGNORECASE):
            print(f"  - {term}: {GREEN}Passed{RESET}")
        else:
            failed_bad_matches.append(("Sonarr", term))
            print(f"  - {term}: {RED}Failed{RESET}")

    # Determine and print overall test result
    if not failed_good_matches and not failed_bad_matches:
        return True
    else:
        return False
