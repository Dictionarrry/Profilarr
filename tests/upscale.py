from extract import get_custom_format, get_regex
import re
import sys

# ANSI escape codes for colors
GREEN = '\033[92m'
RED = '\033[91m'
ORANGE = '\033[38;5;208m'
RESET = '\033[0m'

good_matches = [
    "The.Dukes.Of.Hazzard.Unrated.2005.2160p.Ai-Upscaled.10Bit.H265.DDP.5.1.RIFE.4.15-60fps-DirtyHippie",
    "Scrubs.S05E09.My.Half-Acre.Upscale.Hybrid.1080p.WEBRip.DD5.1.H.264-DEADBADUGLY",
    "[EG]Mobile Suit Gundam SEED 21 BD[HEVC DualAudio AI-Upscale]",
    "Death.Proof.2007.2160p.Ai-Upscaled.10Bit.H265.TrueHD.5.1-DirtyHippie RIFE.4.14v2-60fps.mkv",
    "Oi.Aparadektoi.S02E03.[FullHDAIUpscaled][Upload-Ft4U]",
    "Cash.Out-I.maghi.del.furto.2024.UpScaled.2160p.H265.10.bit.DV.HDR10+.ita.eng.AC3.5.1.sub.ita.eng.Licdom",
    "2012 (2009) UHD 4K Upscaled x264 AC3 Soup mkv",
    "The Martian 2015 4K UHD UPSCALED-ETRG",
    "WWE Smackdown 1999 S04 1080p (Upscaled) PEACOCK WEB-DL H 264 AAC 2 0",
    "Venom 023 (2023) (Digital) (Li'l-Empire) (HD-Upscaled)",
    "Natashas.Bondage.Sex.Vol.2.Upscaled",
    "Star Trek: Deep Space Nine S01 AI Upscale 2160p DVD AAC 2.0 H.263",
    "Star.Trek.Raumschiff.Voyager.S05E13.Schwere.German.AC3D.DL.1080p.DVD.AI.REGRADED.x264-HQC",
    "The.Marvels.(2023).[HDR.ReGrade].1080p.4K-WEBRip.[Hin-Eng].DDP.5.1.Atmos.—.PeruGuy",
    "Terminator 3 Rise of the Machines 2003 2160p HDR UpsUHD x265 REGRADED REPACK-QfG",
    "The Departed (2006) Regrade (2160p x265 HEVC 10bit HDR BluRay DTS-HD MA 6.1 Prof).mkv",
    "The Matrix (1999) 1080p BluRay Regraded x264 TrueHD Atmos 7.1 [lvl99]",
    "The.Last.Samurai.2003.2160p.x265.10bit.TrueHD.DTS.5.1[TheUpscaler].mkv",
    "New.Jack.City.1991.2160p.x265.10bit.DTS HD.MA.5.1[TheUpscaler]",
    "Bank Chor (2017) 720p UP SCALED DVDRip x264 AC3 ESub [DDR]",
    "Transformers.2007.2160p.DV.HDR10Plus.Ai-Enhanced.H265.TrueHD.7.1.Atmos.MULTI.RIFE.4.15-60fps-DirtyHippie",
    "Karakter (1997) - AI enhanced 4K",
    "The.Farm-Angola,.USA.1998.480p.DVDRip.AI.Enhanced",
    "Ugramm.2014.[Kannada+Hindi].1080p.Ai.Enhanced.[1",
    "Soldiers Sortie 2006 AIEnhanced 1080p 50fps x265 10bit MP2-Enichi",
    "No.Country.For.Old.Men.2007.2160P.Ai-Upscaled.10Bit.H265.DTS-HD.MA.5.1.RIFE.4.15-60fps-DirtyHippie",
    "Oi.Aparadektoi.S01E10.91.[FullHDAIUpscaled][Upload-Ft4U]",
    "Avatar.2009.Extended.UHD.Re-Grade.4000nit.2160p.HEVC.HDR.IVACHS.ENG.ExKinoRay",
    "It's Always Sunny in Philadelphia (2005) S05 (1080p AIUS DVD Hybrid x265 SDR DD 5.1 English - JBENT TAoE) [REPACK] ",
    "It's Always Sunny in Philadelphia (2005) S05E01 The Gang Exploits the Mortgage Crisis REPACK (1080p DVDRip AI Upscale x265 10bit AC3 5.1 - JBENT)[TAoE].mkv"
]

bad_matches = [
    "The Scales of Providence [2008] KO Complete eng subs",
    "Scales Mermaids Are Real 2017 WEBRip X264",
    "Barrie Cassidys One Plus One S01E03 Sally Scales 720p HDTV x264-CBFM",
    "The Aggression Scale 2012 10bit hevc-d3g",
    "Family.by.the.Ton.S01E02.Stepping.on.the.Scale.HDTV.x264-CRiMSON",
    "Upgrade.2018.1080p.Bluray.DD5.1.x264-playHD",
    "The Brave S01E05 Enhanced Protection 720p AMZN WEBRip DDP5 1 X264-NTb",
    "Star.Trek.The.Original.Series.Remastered.And.Enhanced.DVDRip.XviD.ROSub.FL",
    "Guns N' Roses - 2016-04-08 Las Vegas, NV 1st NIGHT ENHANCED BLU RAY 1080i+LPCM AUDIO [fanfzero]",
    "Enhanced.2020.1080p.Bluray.DTS-HD.MA.5.1.X264-EVO"
]


def Upscaled(debug_level=0):
    # Get the custom formats for "Upscaled" from both Radarr and Sonarr
    Upscaled_radarr = get_custom_format("Upscaled", "radarr", debug_level)
    Upscaled_sonarr = get_custom_format("Upscaled", "sonarr", debug_level)


    # Extract the regex values for both Radarr and Sonarr using get_regex
    Upscaled_value_radarr = get_regex(Upscaled_radarr, "Upscaled", debug_level)
    Upscaled_value_sonarr = get_regex(Upscaled_sonarr, "Upscaled", debug_level)

    if debug_level > 0:
        print(f"Testing with regex: {ORANGE}{Upscaled_value_radarr}{RESET}\n")
    # Compare Radarr and Sonarr Upscaled regex values
    if Upscaled_value_radarr != Upscaled_value_sonarr:
        print("Test Failed: regex value not same.")
        print(f"Radarr regex: {Upscaled_value_radarr}")
        print(f"Sonarr regex: {Upscaled_value_sonarr}")


    good_matches_passed = []
    good_matches_failed = []
    bad_matches_passed = []
    bad_matches_failed = []

    print("Checking good matches:")
    # Test good matches
    for release in good_matches:
        if re.search(Upscaled_value_radarr, release, re.IGNORECASE):
            good_matches_passed.append(release)
            print(f"  - {release}: {GREEN}Passed{RESET}")
        else:
            good_matches_failed.append(release)
            print(f"  - {release}: {RED}Failed{RESET}")

    print("\nChecking bad matches:")
    # Test bad matches
    for release in bad_matches:
        if re.search(Upscaled_value_radarr, release, re.IGNORECASE):
            bad_matches_failed.append(release)
            print(f"  - {release}: {RED}Failed{RESET}")
        else:
            bad_matches_passed.append(release)
            print(f"  - {release}: {GREEN}Passed{RESET}")

    # Reporting failed matches
    print("\nFailed matches:")
    if good_matches_failed or bad_matches_passed:
        for release in good_matches_failed + bad_matches_failed:
            print(f"  - {release}")
    else:
        print(f"{GREEN}None, Great Job! :){RESET}")

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
