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
    "HobyBuchanon.Rebecca.Vanguard.Sailor.Luna.Extreme.Sloppy.Gagging.Throat.Fuck.and.Throat.Pie.2019.12.20.1080p.AV1",
    "TushyRaw.Emma.Rosie.Petite.Tight.Emma.Gets.Her.Tiny.Ass.Stretched.Out.TushyRaw.Emma.Rosie.Petite.Tight.Emma.Gets.Her.Tiny.Ass.Stretched.Out.2023.12.06.2160p.AV1.mp4",
    "MILFY 24 05 15 Nikki Benz Ultimate MILF Nikki Cums Hard while Riding His Cock XXX 720p AV1 XLeech.mkv",
    "MILFY 24 05 08 Medusa Fit Yoga MILF Medusa Rides Young Studs Cock All Day XXX 720p AV1 XLeech.mkv",
    "Vixen 24 05 17 Blake Blossom Giselle Blanco Double Take XXX 720p AV1 XLeech.mkv",
    "TouchMyWife 24 05 17 Addison Vodka Wife Wants the Younger Version XXX 720p AV1 XLeech.mkv",
    "LoveHerAss 24 05 08 Clea Gaultier Big Tits Hot Ass Absolute Babe XXX 720p AV1 XLeech.mkv",
    "Deeper 24 05 09 Lulu Chu Cop Shop XXX 720p AV1 XLeech.mkv",
    "BreedMe 24 05 14 Payton Preslee Busty Brunette Payton Preslee XXX 720p AV1 XLeech.mkv",
    "Freeze 24 05 03 Lia Lin When Shaman Calls XXX 720p AV1 XLeech.mkv",
    "Oppenheimer 2023 BluRay 2160p UHD AV1 HDR10 DTS-HD MA 5.1 - PRL Waldek",
    "Casino.Royale.2006.1080p.Bluray.OPUS.5.1.AV1-WhiskeyJack.mkv",
    "Interstellar 2014 BluRay 2160p DTS HDMA5 1 AV1 10bit-CHD",
    "Dune.Part.Two.2024.REPACK.1080p.BluRay.AV1.Opus.7.1.MULTi4-dAV1nci",
    "Oppenheimer 2023 BluRay 2160p UHD AV1 HDR10 DTS-HD MA 5.1 - PRL Waldek",
    "Guardians of the Galaxy Vol 3 2023 BluRay 2160p UHD AV1 HDR10 TrueHD 7.1 Atmos - PRL Waldek",
    "Dune.Part.Two.2024.2160p.DV.HDR.BluRay.AV1.Opus.7.1.MULTi4-dAV1nci",
    "AVATAR: THE WAY OF WATER [2022]1080p WEB DL[AV1][10 BIT][Atmos/E-AC3][RoB]",
    "Godzilla.X.Kong.The.New.Empire.2024.Web-Dl.2160P.AV1",
    "GREEN LANTERN EXTENDED CUT [2011]1080p BDRRip[10 BIT AV1][DTS-HD MA][RoB]",
    "Resident Evil Death Island 2023 1080p English AAC AV1",
    "Bird Box (2018) 1080p DS4K NF WEBRip AV1 Opus 5.1 [Retr0]",
    "The Banshees of Inisherin (2022) 1080p DS4K MA WEBRip AV1 Opus 5.1 [Retr0]",
    "Once Upon a Studio (2023) DS4K 1080p DSNP WEBRip AV1 Opus 5.1 [RAV1NE]",
    "24 Jam Bersama Gaspar (2024) INDONESIAN DS4K 1080p NF WEBRip AV1 Opus 5.1 [RAV1NE]",
    "THE HUNGER GAMES QUADRILOGY [4K UHD BDRip][10 BIT AV1][HDR][ATMOS/TrueHD][RoB]",
    "AVATAR: THE WAY OF WATER [2022]1080p WEB DL[AV1][10 BIT][Atmos/E-AC3][RoB]",
    "Rebel Moon Part One-A Child of Fire 2023 720p AV1-Zero00",
    "[Copernicus] Chainsaw Man - S01E02 [BDRip][1080p][AV1-10bit]",
    "Scavengers.Reign.S01e05.The.Demeter.Opus.AV1"
]


bad_matches = [
]

def AV1(debug_level=0):
    # Get the custom formats for "AV1" from both Radarr and Sonarr
    AV1_radarr = get_custom_format("AV1", "radarr", debug_level)
    AV1_sonarr = get_custom_format("AV1", "sonarr", debug_level)

    # Extract the regex values for both Radarr and Sonarr using get_regex
    AV1_value_radarr = get_regex(AV1_radarr, "AV1", debug_level)
    AV1_value_sonarr = get_regex(AV1_sonarr, "AV1", debug_level)

    # Replace the negative lookbehind with a negative lookahead
    AV1_value_radarr = AV1_value_radarr.replace(r"(?<=^|[\s.-])", r"(?:^|[\s.-])")
    AV1_value_sonarr = AV1_value_sonarr.replace(r"(?<=^|[\s.-])", r"(?:^|[\s.-])")

    if debug_level > 0:
        print(f"Testing with regex: {ORANGE}{AV1_value_radarr}{RESET}\n")

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
        if re.search(AV1_value_radarr, release, re.IGNORECASE):
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