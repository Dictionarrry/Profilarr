from extract import get_custom_format, get_regex
import re
import sys

# ANSI escape codes for colors
GREEN = '\033[92m'
RED = '\033[91m'
ORANGE = '\033[93m'
RESET = '\033[0m'

good_matches = [
    "About Dry Grasses (2023) (1080p BluRay x265 HEVC 10bit AAC 5.1 Turkish Tigole) [QxR]",
    "1408 (2007) DC (1080p BluRay x265 10bit Tigole).mkv",
    "Desperado (1995) (1080p BluRay x265 10bit Tigole).mkv",
    "Nineteen Eighty-Four 1984 Criterion 1080p BluRay 10bit AAC 1.0 x265-Tigole",
    "2010.1984.1080p.BluRay.x265.10bit.Tigole",
    "Gran Turismo (2023) (2160p BluRay x265 10bit HDR Tigole).mkv",
    "Pirates of the Caribbean - The Curse of the Black Pearl 2003 REPACK 1080p BluRay x265 HEVC 10bit AAC 5.1-Tigole QxR",
    "Hot Tub Time Machine 2010 Unrated 1080p Bluray x265 HEVC 10bit AAC 5 1 Tigole",
    "Corsage 2022 1080p BluRay AAC 5.1 x265-Tigole QxR",
    "Everything Everywhere All at Once (2022) 2160p BluRay x265 HEVC 10bit HDR AAC 7 1 Tigole-QxR",
    "Argo (2012) Extended (1080p BluRay x265 SDR AAC 5.1 English - Tigole QxR)",
    "The Holdovers (2023) (1080p BluRay x265 SDR AAC 5.1 English - Tigole QxR)",
    "Mission - Impossible - Fallout (2018) IMAX (1080p BluRay x265 SDR AAC 7.1 English - Tigole QxR)",
    "Aguirre the Wrath of God (1972) WHC Edition 1080p BluRay x265 10bit AAC 1.0 ENG+GER Tigole QxR",
    "Y Tu Mam Tambi n (2001) Criterion (1080p x265 10bit Tigole)",
    "A Bug's Life (1998) (2160p UHD BluRay x265 HDR AAC 7.1 English - Tigole QxR)",
    "1408 (2007) Director's Cut (1080p BluRay x265 SDR AAC 5.1 English - Tigole QxR)",
    "A Fistful of Dollars (1964) (1080p BluRay x265 SDR AAC 5.1 English - Tigole QxR)",
    "A Taxi Driver (2017) (1080p BluRay x265 SDR AAC 5.1 Korean - Tigole QxR)",
    "A Ghost Story (2017) (1080p BluRay x265 SDR AAC 5.1 English - Tigole QxR)",
    "Around the World in 80 Days (2004) (1080p BluRay x265 SDR AAC 6.1 English - Tigole QxR)",
    "A Good Marriage (1982) (1080p BluRay x265 SDR AAC 1.0 French - Tigole QxR)",
    "A Prophet (2009) (1080p BluRay x265 SDR AAC 5.1 French - Tigole QxR)",
    "A Pigeon Sat on a Branch Reflecting on Existence (2014) (1080p BluRay x265 SDR AAC 5.1 Swedish - Tigole QxR)",
    "A Man for All Seasons (1966) (1080p BluRay x265 SDR AAC 5.1 English - Tigole QxR)",
    "Bill & Ted's Excellent Adventure (1989) (1080p RM4K  BluRay x265 SDR AAC 2.0 English - Tigole QxR)",
    "Nick and Norah's Infinite Playlist (2008) (1080p BluRay x265 SDR AAC 5.1 English - Tigole QxR)",
    "Iron Sky (2012) Director's Cut (1080p BluRay x265 SDR AAC 5.1 English - Tigole QxR)",

    "Aladdin 1992 Diamond Edition 1080p BluRay x265 HEVC 10bit AAC 7 1 English French Spanish FreetheFish-QxR",
    "Jersey Girl (1992) (1080p BluRay x265 HEVC 10bit AAC 5.1 FreetheFish) [QxR]",
    "American History X (1998) (1080p BluRay x265 FreetheFish).mkv",
    "That '70s Show S01-S08 COMPLETE + Extras 1080p BluRay AAC 5.1 x265-FreetheFish [QxR]",
    "Annie (1982) (1080p BluRay x265 FreetheFish)",
    "Apollo.13.1995.1080p.BluRay.x265.FreetheFish",
    "Game of Thrones (2010) S00E01 (1080p HDTV x265 SDR DD 2.0 English - FreetheFish QxR)",
    "Flubber (1997) (1080p WEBRip x265 SDR DDP 5.1 English - FreetheFish QxR)",
    "The Breakfast Club (1985) Criterion (1080p BluRay x265 SDR AAC 5.1 English - FreetheFish QxR)",
    "A Christmas Story (1983) (1080p BluRay x265 SDR AAC 1.0 English - FreetheFish QxR)",
    "How the Grinch Stole Christmas! (1966) (1080p BluRay x265 SDR AAC 2.0 English - FreetheFish QxR)",
    "The Nightmare Before Christmas (1993) (1080p BluRay x265 SDR AAC 7.1 English - FreetheFish QxR)",
    "American History X (1998) (1080p BluRay x265 SDR AAC 7.1 English - FreetheFish QxR)",
    "The Hunchback of Notre Dame (1996) (1080p BluRay x265 SDR AAC 5.1 English - FreetheFish QxR)",
    "Bodied (2018) (1080p DS4K RED WEB-DL x265 SDR AAC 5.1 English - FreetheFish QxR)",
    "Arthur and the Invisibles (2006) (1080p BluRay x265 SDR AAC 5.1 English - FreetheFish QxR)",

    "The Adventures of Tintin (2011) (1080p BluRay x265 HEVC 10bit EAC3 7.1 SAMPA) [QxR]",
    "Heat 1995 2160p BluRay HDR DTS 7.1 x265-SAMPA",
    "Dragon Ball Z Broly - The Legendary Super Saiyan 1993 1080p BluRay x265 HEVC 10bit MLPFBA 5.1-SAMPA",
    "The.Accountant.2016.1080p.BluRay.x265.SAMPA",
    "Casino Royale (2006) (2160p BluRay x265 HEVC 10bit HDR DTS 5.1 SAMPA).mkv",
    "Fast.X.2023.1080p.MA.WEB-DL.x265.HEVC.10bit.EAC3.5.1.SAMPA",
    "Captain America - Civil War (2016) IMAX (1080p BluRay x265 SDR DDP 7.1 English - SAMPA QxR)",
    "Ad Astra (2019) (2160p UHD BluRay x265 HDR TrueHD Atmos 7.1 English - SAMPA QxR)",
    "Alita - Battle Angel (2019) Open Matte (1080p WEB-DL Hybrid x265 SDR DDP 7.1 English - SAMPA QxR)",
    "The Adventures of Tintin (2011) (1080p BluRay x265 SDR DDP 7.1 English - SAMPA QxR)",
    "The Killer (1989) (1080p BluRay x265 SDR DDP 5.1 DUAL - SAMPA QxR)",
    "The Assassin (2015) (1080p BluRay x265 SDR DD 5.1 Mandarin - SAMPA QxR)",
    "The Incredible Hulk (2008) (1080p BluRay x265 SDR DDP 7.1 English - SAMPA QxR)",
    "The Living Daylights (1987) (1080p BluRay x265 SDR DTS 5.1 English - SAMPA QxR)",
    "Bumblebee (2018) (2160p UHD BluRay x265 HDR TrueHD Atmos 7.1 English - SAMPA QxR)",

    "The Edge of Heaven (2007) (1080p AMZN WEB-DL x265 afm72)",
    "The Big Shave (1967) Criterion (1080p BluRay x265 SDR AAC 1.0 English - afm72 QxR)",
    "Billy's Balloon (1998) 1080p BluRay x265 SDR AAC 2.0 English-afm72",
    "Broken Embraces AKA Los abrazos rotos 2009 1080p BluRay x265 HEVC 10bit AAC 5 1 Spanish-afm72",
    "The Borgias (2011) Season 2 S02 + Extras (1080p BluRay x265 HEVC 10bit AAC 5 1 afm72)",
    "Blade Runner 1982 The Final Cut + Extras (1080p BluRay HDR x265 HEVC 10bit AAC 7.1 afm72)",
    "TPB.AFK.The.Pirate.Bay.Away.from.Keyboard.2013.1080p.WEB-DL.x265.HEVC.10bit.AAC.2.0.afm72",
    "Submarine (2010) (1080p BluRay x265 HEVC 10bit AAC 5.1 afm72) [QxR].mkv",
    "World of Tomorrow The First Three Episodes 2015 1080p BluRay x265 HEVC 10bit AAC 2 0 afm72-QxR",
    "3:10 to Yuma (2007) (1080p BluRay x265 SDR AAC 7.1 English - afm72 QxR)",
    "Premium Rush (2012) (1080p BluRay x265 SDR AAC 5.1 English - afm72 QxR)",
    "Forrest Gump (1994) (1080p BluRay x265 SDR AAC 7.1 English - afm72 QxR)",
    "21 Grams (2003) (1080p BluRay x265 SDR AAC 5.1 English - afm72 QxR)",
    "Dog Day Afternoon (1975) (1080p BluRay x265 SDR AAC 1.0 English - afm72 QxR)",
    "Bicycle Thieves (1948) Arrow (1080p BluRay x265 SDR AAC 1.0 Italian - afm72 QxR)",
    "Bringing Up Baby (1938) Criterion (1080p BluRay x265 SDR AAC 1.0 English - afm72 QxR)",
    "Definitely, Maybe (2008) (1080p BluRay x265 SDR AAC 5.1 English - afm72 QxR)",
    "La Strada (1954) Criterion (1080p BluRay x265 SDR AAC 1.0 DUAL - afm72 QxR)",
    "Ikiru (1952) Criterion (1080p BluRay x265 SDR AAC 1.0 Japanese - afm72 QxR)",
    "Kes (1970) (1080p BluRay x265 SDR AAC 1.0 English - afm72 QxR)",
    "Where Is My Friend's House? (1987) Criterion (1080p BluRay x265 SDR AAC 1.0 Persian - afm72 QxR)",
    "Stalker (1979) (1080p BluRay x265 SDR AAC 2.0 Russian - afm72 QxR)",

    "This.Is.Us.2016-S04E05-Storybook.Love.1080p.AMZN.WEB-DL.x265.Silence",
    "Parks and Recreation (2009) S00E04 (1080p BluRay x265 SDR AAC 2.0 English - Silence QxR)",
    "Columbo S01-13 1080p BluRay AC3 2 0 x265-Silence",
    "A Discovery of Witches (2018) S02 (1080p x265 HEVC 10bit AAC 5 1 Silence)",
    "3 Body Problem (2024) Season 1 S01 (1080p NF WEB-DL x265 HEVC 10bit EAC3 5.1 Silence) [QxR]",
    "Loki (2023) S02 Season 2 COMPLETE 1080p 10bit DSNP WEBRip x265 HEVC Hindi DDP 5.1 English DDP 5.1 MSubs TheAvi Silence QxR",
    "Anatomy of a Fall (2023) (1080p BluRay x265 SDR DDP 5.1 French - Silence QxR)",
    "Brooklyn Nine-Nine (2013) S01-S08 (1080p BluRay x265 HEVC 10bit AAC 5 1 Silence) REPACK [QxR]",
    "Cosmos A Spacetime Odyssey (2014) Season 1 S01 + Extras (1080p BluRay x265 HEVC 10bit AAC 5 1 Silence) QxR",
    "You Can Count on Me 2000 1080p AMZN WEB-DL x265 HEVC 10bit AAC 5 1 Silence-QxR",
    "The World at War (1973) Season 1 S01 (1080p BluRay x265 HEVC 10bit AAC 2.0 Silence) (QxR)",
    "Stranger Things 2016 Season 2 S02 1080p BluRay x265 HEVC 10bit AAC 5.1 - Silence",
    "Superstore (2015) S06 (1080p AMZN WEB-DL x265 SDR DDP 5.1 English - Silence QxR)",
    "Sharp Objects (2018) S01 (1080p BluRay x265 SDR AAC 5.1 English - Silence QxR)",
    "21 Up (1977) 1080p BluRay x265 SDR AAC 2.0 English -Silence",
    "Parasite (2019) B&W Version (1080p BluRay x265 SDR AAC 5.1 Korean - Silence QxR)",
    "She Said (2022) (1080p MA WEB-DL x265 SDR DDP 5.1 English - Silence QxR)",
    "The Office (2005) S01 (1080p BluRay x265 SDR AAC 5.1 English - Silence QxR)",
    "The Office (2005) S02 (1080p BluRay x265 SDR AAC 5.1 English - Silence QxR)",
    "The Office (2005) S03 (1080p BluRay x265 SDR AAC 5.1 English - Silence QxR)",
    "The Office (2005) S04 (1080p BluRay x265 SDR AAC 5.1 English - Silence QxR)",
    "The Office (2005) S05 (1080p BluRay x265 SDR AAC 5.1 English - Silence QxR)",
    "The Office (2005) S06 (1080p BluRay x265 SDR AAC 5.1 English - Silence QxR)",
    "The Office (2005) S07 (1080p BluRay x265 SDR AAC 5.1 English - Silence QxR)",
    "The Office (2005) S08 (1080p BluRay x265 SDR AAC 5.1 English - Silence QxR)",

    "Badlands (1973) Criterion (1080p BluRay x265 r00t)",
    "13 Assassins (2010) 1080p BluRay x265 SDR AAC 5.1 Japanese-r00t",
    "The 400 Blows (1959) Criterion (1080p BluRay x265 SDR AAC 1.0 French - r00t QxR)",
    "Good Night, and Good Luck. (2005) 1080p BluRay x265 SDR AAC 5.1 English-r00t",
    "99 Homes (2014) + Extras (1080p BluRay x265 HEVC 10bit AAC 5 1 r00t)",
    "Channel Zero 2016 S02 1080p AMZN WEB-DL x265 HEVC 10bit EAC3 6 0 r00t-QxR",
    "Umbre (2014) Season 2 S02 (1080p HBO WEB-DL x265 HEVC 10bit AC3 5.1 Romanian r00t) [QxR]",
    "A Face in the Crowd (1957) (1080p BluRay x265 SDR AAC 1.0 English - r00t QxR)",
    "Anatomy of a Murder (1959) Criterion (1080p BluRay x265 SDR AAC 1.0 English - r00t QxR)",
    "BASEketball (1998) (1080p BluRay x265 SDR AAC 5.1 English - r00t QxR)",
    "Belle de Jour (1967) Criterion (1080p BluRay x265 SDR AAC 1.0 French - r00t QxR)",
    "Blow-Up (1966) Criterion (1080p BluRay x265 SDR AAC 1.0 English - r00t QxR)",
    "Chimes at Midnight (1965) Criterion (1080p BluRay x265 SDR AAC 1.0 English - r00t QxR)",
    "High and Low (1963) Criterion (1080p BluRay x265 SDR AAC 4.0 Japanese - r00t QxR)",
    "House (1977) Criterion (1080p BluRay x265 SDR AAC 1.0 Japanese - r00t QxR)",
    "The Lady from Shanghai (1947) (1080p BluRay x265 SDR AAC 1.0 English - r00t QxR)",
    "The 400 Blows (1959) Criterion (1080p BluRay x265 SDR AAC 1.0 French - r00t QxR)",

    "Crash Landing on You (2019) S01 (1080p NF WEB-DL x265 SDR DDP 2.0 Korean - MONOLITH QxR)",
    "3Below Tales of Arcadia (2018) Season 1-2 S01-S02 (1080p NF WEB-DL x265 HEVC 10bit AAC 5 1 MONOLITH)",
    "Mr D (2012) S01-S08 Complete Series (1080p NF WEB-DL x265 HEVC 10bit AAC 5 1 MONOLITH) [QxR]",
    "Sue.Thomas.F.B.Eye.2002-S03E13-False.Profit.480p.AMZN.WEB-DL.x265.MONOLITH",
    "ER 1994 S12 1080p AMZN WEB-DL H.265 H.265 10bit DD+ 2.0-MONOLITH",
    "3% (2011) Season 4 S04 (1080p NF WEBRip x265 HEVC 10bit EAC3 5.1 Portuguese MONOLITH) [QxR]",
    "Sue Thomas F B Eye 2002 Season 1 3 S01 S03 480p AMZN WEB-DL x265 HEVC 10bit EAC3 2.0 MONOLITH-QxR",
    "Last Week Tonight with John Oliver (2014) S01 (1080p AMZN WEB-DL x265 SDR DDP 2.0 English - MONOLITH QxR)",
    "Last Week Tonight with John Oliver (2014) S02 (1080p AMZN WEB-DL x265 SDR DDP 2.0 English - MONOLITH QxR)",
    "Last Week Tonight with John Oliver (2014) S03 (1080p AMZN WEB-DL x265 SDR DDP 2.0 English - MONOLITH QxR)",
    "Last Week Tonight with John Oliver (2014) S04 (1080p AMZN WEB-DL x265 SDR DDP 2.0 English - MONOLITH QxR)",
    "Last Week Tonight with John Oliver (2014) S05 (1080p AMZN WEB-DL x265 SDR DDP 2.0 English - MONOLITH QxR)",
    "Last Week Tonight with John Oliver (2014) S06 (1080p AMZN WEB-DL x265 SDR DDP 2.0 English - MONOLITH QxR)",
    "Last Week Tonight with John Oliver (2014) S07 (1080p AMZN WEB-DL x265 SDR DDP 2.0 English - MONOLITH QxR)",
    "Last Week Tonight with John Oliver (2014) S08 (1080p HMAX WEB-DL x265 SDR DD 2.0 English - MONOLITH QxR)",
    "How It's Made (2001) S24 (1080p WEB-DL x265 SDR AAC 2.0 English - MONOLITH QxR)",
    "How It's Made (2001) S28 (1080p WEB-DL x265 SDR AAC 2.0 English - MONOLITH QxR)",

    "The Birdcage (1996) 1080p BluRay x265 SDR AAC 5.1 English-Panda",
    "Black Mirror (2011) S03 (1080p BluRay x265 SDR AAC 5.1 English - Panda QxR)",
    "Dead Man's Shoes (2004) (1080p BluRay x265 HEVC 10bit AAC 5.1 Panda) [QxR]",
    "What We Do in the Shadows (2014) (1080p BluRay x265 SDR AAC 5.1 English - Silence QxR)",
    "Black Mirror (2011) S03 (1080p BluRay x265 SDR AAC 5.1 English - Panda QxR)",
    "Black Mirror (2011) S04 (1080p BluRay x265 SDR AAC 5.1 English - Panda QxR)",
    "Threads (1984) (1080p BluRay x265 SDR AAC 2.0 English - Panda QxR)",
    "Bicentennial Man (1999) (1080p AMZN WEB-DL x265 SDR AAC 5.1 English - Panda QxR)",
    "Blue Mountain State (2010) S01 (1080p BluRay x265 SDR AAC 5.1 English - Panda QxR)",
    "Blue Mountain State (2010) S02 (1080p WEB-DL x265 SDR AAC 2.0 English - Panda QxR)",
    "Blue Mountain State (2010) S03 (1080p WEB-DL x265 SDR AAC 2.0 English - Panda QxR)",
    "Blue Mountain State - The Rise of Thadland (2016) (1080p BluRay x265 SDR AAC 5.1 English - Panda QxR)",
    "Children of Men (2006) (1080p BluRay x265 SDR AAC 5.1 English - Panda QxR)",

    "El embarcadero (2019) - S02E03 - Episodio 3 (1080p BluRay x265 Kappa)",
    "Californication (2007) S01 (1080p BluRay x265 SDR AAC 5.1 English - Kappa QxR)",
    "Alias Grace (2017) S01 (1080p NF WEBRip x265 HEVC 10bit AC3 5 1 Kappa)",
    "Marvels Agents of S H I E L D (2013) S01-S07 (1080p BluRay x265 HEVC 10bit AAC 5 1 Ghost Kappa) [QxR]",
    "Bloodlands.2021-S01E01-Episode.1.1080p.BluRay.x265.Kappa",
    "Ballers 2015 S01 1080p BluRay x265 HEVC 10bit AAC 5.1-Kappa",
    "Eastbound & Down (2009) Season 1 S01 + Extras (1080p BluRay x265 HEVC 10bit AAC 5.1 Kappa) [QxR]",
    "ZeroZeroZero (2020) Season 1 S01 (1080p BluRay x265 HEVC 10bit AAC 5.1 Kappa)",
    "Californication (2007) S01 (1080p BluRay x265 SDR AAC 5.1 English - Kappa QxR)",
    "Californication (2007) S02 (1080p BluRay x265 SDR AAC 5.1 English - Kappa QxR)",
    "Californication (2007) S03 (1080p BluRay x265 SDR AAC 5.1 English - Kappa QxR)",
    "Californication (2007) S04 (1080p BluRay x265 SDR AAC 5.1 English - Kappa QxR)",
    "Californication (2007) S05 (1080p BluRay x265 SDR AAC 5.1 English - Kappa QxR)",
    "Californication (2007) S06 (1080p BluRay x265 SDR AAC 5.1 English - Kappa QxR)",
    "Californication (2007) S07 (1080p BluRay x265 SDR AAC 5.1 English - Kappa QxR)",
    "Chuck (2007) S01 (1080p BluRay x265 SDR AAC 5.1 English - Kappa QxR)",
    "Chuck (2007) S02 (1080p BluRay x265 SDR AAC 5.1 English - Kappa QxR)",
    "Chuck (2007) S03 (1080p BluRay x265 SDR AAC 5.1 English - Kappa QxR)",
    "Over the Garden Wall (2014) S01 (1080p BluRay x265 SDR AAC 2.0 English - QxR)"

    "His Dark Materials (2019) - S03E01 - The Enchanted Sleeper (1080p HMAX WEB-DL x265 t3nzin)",
    "Tulsa.King.2022.S01E01.1080p.BluRay.x265.t3nzin",
    "Acapulco (2021) S01 (1080p ATVP WEB-DL x265 SDR DDP Atmos 5.1 English - t3nzin QxR)",
    "Euphoria (2019) S01 + Extras (1080p AMZN WEB-DL x265 HEVC 10bit EAC3 5 1 t3nzin) [QxR]",
    "The Problem With Jon Stewart 2021 Season 2 S02 1080p ATVP WEB-DL x265 HEVC 10bit AC3 5.1 t3nzin REPACK-QxR",
    "Euphoria (2019) S00E01 (1080p AMZN WEB-DL x265 SDR DDP 5.1 English - t3nzin QxR)",
    "Euphoria (2019) S00E02 (1080p AMZN WEB-DL x265 SDR DDP 5.1 English - t3nzin QxR)",
    "Euphoria (2019) S01 (1080p AMZN WEB-DL x265 SDR DDP 5.1 English - t3nzin QxR)",
    "Euphoria (2019) S02 (1080p AMZN WEB-DL x265 SDR DDP 5.1 English - t3nzin QxR)",
    "House of the Dragon (2022) S01 (1080p BluRay x265 SDR DDP Atmos 5.1 English - t3nzin QxR)",
    "Only Murders in the Building (2021) S02 (1080p DSNP WEB-DL x265 SDR DDP 5.1 English - t3nzin QxR)",
    "Ted Lasso (2020) S02 (1080p ATVP WEB-DL x265 SDR DDP Atmos 5.1 English - t3nzin QxR)",
    "Ted Lasso (2020) S00E07 (1080p ATVP WEB-DL x265 SDR DDP Atmos 5.1 English - t3nzin QxR)",
    "Tiger King (2020) S01 (1080p NF WEB-DL x265 SDR DDP Atmos 5.1 English - t3nzin QxR)",
    "Tiger King (2020) S02 (1080p NF WEB-DL x265 SDR DDP 5.1 English - t3nzin QxR)",

    "Avatar.The.Last.Airbender.2005-S01E01-The.Boy.in.the.Iceberg.1080p.WEB-DL.x265.RCVR",
    "Desperate Housewives (2004) S01 (1080p WEB-DL x265 SDR AAC 5.1 English - RCVR QxR)",
    "Heartland S10 1080p NF WEB-DL DDP5 1 x264 1-RCVR",
    "1000.Ways.To.Die-S04e06-Crying.Over.Spilled.Blood-[Amzn.Webdl-1080P.8Bit.X264][Eac3.2.0]-Rcvr",
    "Mr Robot 2015 S01 + Extras 1080p BluRay x265 HEVC 10bit AAC 5.1 RCVR QxR",
    "The Widow (2019) Season 1 S01 (1080p BluRay x265 HEVC 10bit AAC 5.1 RCVR) [QxR]",
    "Gavin & Stacey (2007) S01 (1080p BluRay x265 SDR AAC 2.0 English - RCVR QxR)",
    "Gavin & Stacey (2007) S02 (1080p BluRay x265 SDR AAC 2.0 English - RCVR QxR)",
    "Gavin & Stacey (2007) S03 (1080p BluRay x265 SDR AAC 2.0 English - RCVR QxR)",
    "South Park (1997) S01 (1080p BluRay x265 SDR AAC 5.1 English - RCVR QxR)",
    "South Park (1997) S02 (1080p BluRay x265 SDR AAC 5.1 English - RCVR QxR)",
    "South Park (1997) S03 (1080p BluRay x265 SDR AAC 5.1 English - RCVR QxR)",
    "South Park (1997) S04 (1080p BluRay x265 SDR AAC 5.1 English - RCVR QxR)",
    "South Park (1997) S05 (1080p BluRay x265 SDR AAC 5.1 English - RCVR QxR)",
    "South Park (1997) S06 (1080p BluRay x265 SDR AAC 5.1 English - RCVR QxR)",
    "South Park (1997) S07 (1080p BluRay x265 SDR AAC 5.1 English - RCVR QxR)"

    "The Big Short (2015) (1080p BluRay x265 Natty)",
    "Apur Sansar - The World of Apu (1959) Criterion (1080p BluRay x265 SDR AAC 2.0 Bengali - Natty QxR)",
    "Gangs of Wasseypur 2012 Part 1 1080p BluRay x265 HEVC 10bit AAC 5.1 Hindi - Natty",
    "Pitch Black (2000) (1080p BluRay x265 SDR AAC 5.1 English - Natty QxR)",
    "Queen (2014) (1080p BluRay x265 SDR AAC 7.1 Hindi - Natty QxR)"
    "Swades (2004) (1080p BluRay x265 SDR AAC 5.1 Hindi - Natty QxR)",
    "You Dont Mess with the Zohan (2008) UNRATED (1080p BluRay x265 SDR AAC 5.1 English - Natty QxR)",
    "Khakee (2004) (1080p BluRay x265 SDR AAC 2.0 Hindi - Natty QxR)",
    "The Message (1976) (1080p BluRay x265 SDR AAC 5.1 English - Natty QxR)",

    "The.Blacklist.2013.S01E01.Pilot.1080p.BluRay.x265-RZeroX",
    "Tom.Clancys.Jack.Ryan.(2018)-S02E06-Persona.Non.Grata.(1080p.AMZN.WEB-DL.x265.RZeroX)",
    "Battlestar Galactica (2003) S00 (Mixed Mixed x265 SDR AAC 5.1 English - RZeroX QxR)",
    "Crazy.Ex-Girlfriend.2015-S01E01-Josh.Just.Happens.to.Live.Here.1080p.AMZN.WEB-DL.x265.RZeroX[Theft]",
    "The Boys (2019) Season 1 S01 (1080p AMZN WEB-DL x265 HEVC 10bit EAC3 5.1 RZeroX) [QxR]",
    "Brooklyn Nine Nine (2013) Season 1 S01 (1080p AMZN WEB-DL x265 HEVC 10bit EAC3 5.1 RZeroX)",
    "Young Justice (2010) Season 3 S03 (1080p DCU WEB-DL x265 HEVC 10bit Mixed Mixed RZeroX) [QxR]",
    "Monk (2002) S01 (1080p AMZN WEB-DL x265 SDR DDP 2.0 English - RZeroX QxR)",
    "Monk (2002) S02 (1080p AMZN WEB-DL x265 SDR DDP 2.0 English - RZeroX QxR)",
    "Monk (2002) S03 (1080p AMZN WEB-DL x265 SDR DDP 2.0 English - RZeroX QxR)",
    "Monk (2002) S08 (1080p AMZN WEB-DL x265 SDR DDP 5.1 English - RZeroX QxR)",
    "Monk (2002) S04 (1080p AMZN WEB-DL x265 SDR DDP 5.1 English - RZeroX QxR)",
    "Monk (2002) S05 (1080p AMZN WEB-DL x265 SDR DDP 2.0 English - RZeroX QxR)",
    "Monk (2002) S06 (1080p AMZN WEB-DL x265 SDR DDP 5.1 English - RZeroX QxR)",
    "Monk (2002) S07 (1080p AMZN WEB-DL x265 SDR DDP 5.1 English - RZeroX QxR)",
    "Wallace & Gromit - The Curse of the Were-Rabbit (2005) (1080p BluRay x265 SDR AAC 5.1 English - RZeroX QxR)",
    "Gifted (2017) (1080p BluRay x265 SDR AAC 5.1 English - RZeroX QxR)",

    "Before the Devil Knows You're Dead (2007) 1080p BluRay x265 SDR DDP 5.1 English-Bandi",
    "Blue Is the Warmest Color (2013) (1080p BluRay x265 SDR AAC 5.1 French - Bandi QxR)",
    "A Christmas Carol (2009) (1080p BluRay x265 SDR AAC 5.1 English - Bandi QxR)",
    "Ricky Gervais Live 4: Science (2010) (1080p BluRay x265 SDR AAC 2.0 English - Bandi QxR)",
    "City of God (2002) (1080p BluRay x265 SDR DDP 5.1 Portuguese - Bandi QxR)",
    "The Platform (2019) (1080p BluRay x265 SDR DDP 5.1 DUAL - Bandi QxR)",
    "Amores Perros (2000) (1080p BluRay x265 SDR DDP 5.1 Spanish - Bandi QxR)",
    "Day of the Woman (1978) Uncut (1080p BluRay x265 SDR AAC 2.0 English - Bandi QxR)",
    "Frida (2002) (1080p BluRay x265 SDR AAC 5.1 English - Bandi QxR)",
    "Blue Is the Warmest Color (2013) (1080p BluRay x265 SDR AAC 5.1 French - Bandi QxR)",
    "CODA (2021) (1080p DS4K ATVP WEB-DL x265 SDR DDP Atmos 5.1 English - Bandi QxR)",
    "Liz and the Blue Bird (2018) (1080p BluRay x265 SDR AAC 5.1 DUAL - Bandi QxR)",

    "Anne with an E (2017) - S01E01 - Your Will Shall Decide Your Destiny (1080p BluRay x265 Garshasp)",
    "Grand Designs (1999) S04 576p DVD x265 SDR AAC 2.0 English-Garshasp",
    "Planet of the Apes (1968) (1080p BluRay x265 SDR DDP 5.1 English - Garshasp QxR)",
    "Grave of the Fireflies (1988) (1080p BluRay x265 HEVC 10bit EAC3 2 0 Japanese Garshasp) QxR",
    "How It's Made (2001) S01-S32 (Mixed AMZN WEB-DL x265 HEVC 10bit EAC3 2 0 Garshasp) [QxR]",
    "Louie (2010) S03 (1080p AMZN WEB-DL x265 HEVC 10bit EAC3 5 1 Garshasp)",
    "Bluey.2018-S02E02-Hammerbarn.1080p.DSNP.WEB-DL.x265.Garshasp",
    "Titanic (1997) (1080p BluRay x265 SDR AAC 5.1 English - Garshasp QxR)",
    "The Red Turtle (2016) (1080p BluRay x265 SDR DDP 5.1 English - Garshasp QxR)",
    "Howl's Moving Castle (2004) (1080p BluRay x265 SDR DDP 5.1 DUAL - Garshasp QxR)",
    "While You Were Sleeping (1995) (1080p BluRay x265 SDR DDP 5.1 English - Garshasp QxR)",
    "From Up on Poppy Hill (2011) (1080p BluRay x265 SDR DDP 5.1 DUAL - Garshasp QxR)",
    "The Wind Rises (2013) (1080p BluRay x265 SDR DDP 2.0 DUAL - Garshasp QxR)",
    "Adventures of Tintin (1991) S01 (1080p BluRay x265 SDR DDP 5.1 DUAL - Garshasp QxR)",
    "Adventures of Tintin (1991) S02 (1080p BluRay x265 SDR DDP 5.1 DUAL - Garshasp QxR)",
    "Adventures of Tintin (1991) S03 (1080p BluRay x265 SDR DDP 5.1 DUAL - Garshasp QxR)",
    "Planet of the Apes (1968) (1080p BluRay x265 SDR DDP 5.1 English - Garshasp QxR)",

    "Gentleman Jack (2019) S01 (1080p AMZN WEB-DL x265 SDR DDP 5.1 English - Ghost QxR)",
    "Gentleman Jack (2019) S02 (1080p AMZN WEB-DL x265 SDR DDP 5.1 English - Ghost QxR)",
    "Tuca & Bertie (2019) S01 (1080p NF WEB-DL x265 SDR DDP 5.1 English - Ghost QxR)",
    "Tuca & Bertie (2019) S02 (1080p HULU WEB-DL x265 SDR AAC 2.0 English - Ghost QxR)",
    "Barry (2018) S01 (1080p AMZN WEB-DL x265 SDR DDP 5.1 English - Ghost QxR)",
    "Barry (2018) S02 (1080p AMZN WEB-DL x265 SDR DDP 5.1 English - Ghost QxR)",
    "Barry (2018) S03 (1080p HMAX WEB-DL x265 SDR DD 5.1 English - Ghost QxR)",
    "Scooby-Doo, Where Are You! (1969) S01-S02 (1080p BluRay x265 SDR DD 2.0 English - Ghost QxR)",
    "The Scooby-Doo Show (1976) S01-S03 (1080p Mixed x265 SDR Mixed 2.0 English - Ghost QxR)",
    "What's New, Scooby-Doo? (2002) S01-S03 + Specials (1080p HMAX WEB-DL x265 SDR DD 2.0 English - Ghost QxR)",
    "Peep Show (2003) S06 1080p AMZN WEB-DL x265 SDR AAC 2.0 English-Ghost",
    "Godzilla x Kong The New Empire 2024 1080p AMZN WEB-DL x265 HEVC 10bit EAC3 Atmos 5 1 Ghost-QxR",
    "X Men '97 (2024) Season 1 S01 (1080p DSNP WEB-DL x265 HEVC 10bit EAC3 Atmos 5.1 Ghost) [QxR]",

    "The Twilight Zone (1959) S01 (1080p BluRay x265 SDR AAC 2.0 English - ImE QxR)",
    "The Twilight Zone (1959) S02 (1080p BluRay x265 SDR AAC 2.0 English - ImE QxR)",
    "The Twilight Zone (1959) S03 (1080p BluRay x265 SDR AAC 2.0 English - ImE QxR)",
    "The Twilight Zone (1959) S04 (1080p BluRay x265 SDR AAC 2.0 English - ImE QxR)",
    "The Twilight Zone (1959) S05 (1080p BluRay x265 SDR AAC 2.0 English - ImE QxR)",
    "The West Wing (1999) S00 (1080p AMZN WEB-DL x265 SDR DDP 2.0 English - ImE QxR)",
    "The West Wing (1999) S01 (1080p AMZN WEB-DL x265 SDR DDP 2.0 English - ImE QxR)",
    "The West Wing (1999) S02 (1080p AMZN WEB-DL x265 SDR DDP 2.0 English - ImE QxR)",
    "The West Wing (1999) S03 (1080p AMZN WEB-DL x265 SDR DDP 2.0 English - ImE QxR)",
    "The West Wing (1999) S04 (1080p AMZN WEB-DL x265 SDR DDP 2.0 English - ImE QxR)",
    "Static Shock (2000) Season 1 S01 (1080p HMAX WEB-DL x265 HEVC 10bit AC3 2.0 ImE) [QxR]",
    "The.Sopranos.1999.S02E02.Do.Not.Resuscitate.1080p.BluRay.x265.ImE",
    "Lilo & Stitch The Series (2003) - S02E17 - Morpholomew (1080p DSNP WEB-DL x265 ImE)",
    "Law & Order Criminal Intent (2001) Season 5 S05 (1080p AMZN WEB-DL x265 HEVC 10bit EAC3 5.1 ImE)",
    "Law and Order Special Victims Unit (1999) - S20E19 - Dearly Beloved (1080p AMZN WEB-DL x265 ImE)"

    "The Boondocks (2005) S01 (1080p HMAX WEB-DL x265 SDR DD 2.0 English - YOGI QxR)",
    "The Boondocks (2005) S02 (1080p HMAX WEB-DL x265 SDR DD 2.0 English - YOGI QxR)",
    "The Boondocks (2005) S03 (1080p HMAX WEB-DL x265 SDR DD 5.1 English - YOGI QxR)",
    "The Boondocks (2005) S04 (1080p HMAX WEB-DL x265 SDR DD 5.1 English - YOGI QxR)",
    "Star Wars - The Clone Wars (2008) S07 (1080p DSNP WEB-DL x265 SDR DDP 5.1 English - YOGI QxR)",
    "A Goofy Movie (1995) (1080p BluRay x265 SDR DD 2.0 English - YOGI QxR)",
    "Rush Hour (1998) (1080p BluRay x265 SDR DDP 7.1 English - YOGI QxR)",
    "Rush Hour 3 (2007) (1080p BluRay x265 SDR DDP 7.1 English - YOGI QxR)",
    "Rush Hour 2 (2001) (1080p BluRay x265 SDR DDP 5.1 English - YOGI QxR)",
    "Rush Hour (2016) S01 (1080p AMZN WEB-DL x265 SDR DDP 5.1 English - YOGI QxR)",
    "The VelociPastor (2018) (1080p AMZN WEB-DL x265 SDR DDP 2.0 English - YOGI QxR)",

    "Millennium (2010) S01 (1080p BluRay x265 SDR AAC 5.1 Swedish - LION QxR)",
    "Constantine (2014) S01 (1080p BluRay x265 SDR AAC 5.1 English - Langbard QxR)"
]

bad_matches = [
    "Futurama (1999) S06E18 The Silence of the Clamps (1080p BDRip x265 10bit AC3 5.1 - Goki)[TAoE]",
    "Futurama (1999) S06E16 Ghost in the Machines (1080p BDRip x265 10bit AC3 5.1 - Goki)[TAoE]",
    "Foundation (2021) S01E03 The Mathematician’s Ghost (1080p ATVP Webrip x265 10bit EAC3 5 1 Atmos - Goki)[TAoE]",
    "The.Silence.of.the.Lambs.1991.2160p.UHD.BluRay.DTS-HD.MA.5.1.DV.x265-W4NK3R",
    "Blast of Silence (1961) 1080p CRIT WEB-DL H264 SDR AAC 1.0 English-KUCHU",

    "Anal Brasil 19 (Fernando Marques, Sampasex) 2017 WEB-DL 720p",
    
    "Silence.2016.720p.BluRay.x264.DD5.1-playHD",
    "Total.War.WARHAMMER.II.The.Silence.and.The.Fury-EMPRESS",
    "Dead.Silence.2007.BDRip.DD5.1.x264.RoSubbed-playSD",
    "Quiet.on.Set.The.Dark.Side.of.Kids.TV.S01E05.Breaking.the.Silence.1080p.AMZN.WEB-DL.DDP2.0.H.264-FLUX",
    "When.Calls.the.Heart.S01E03.A.Telling.Silence.1080p.AMZN.WEBRip.DDP.5.1.H.265.-iVy",
    "Cone of Silence 1960 1080p BluRay REMUX AVC FLAC 2 0-EPSiLON",

    "r00t-Frakmend-(KR006)-SiNGLE-WEB-FLAC-2022-HRDT",
    "Ruthless (2023) 1080p AMZN WEB-DL H264 SDR DDP 5.1 English-chr00t",
    "he Yogi Bear Show (1958) S01 (1080p HMAX Webrip x265 10bit AC3 2 0 - Goki)[TAoE]",
    "Hey.There.It's.Yogi.Bear.1964.1080p.BluRay.FLAC2.0.x264-ShAnKs.mkv",
    "The Yogi Bear Show S03 1080p HMAX WEB-DL DD2.0 H.264-PHOENiX",
    "Yogi the Easter Bear (1994) DVD Rip",

    "Acen-Monolith_Volume_One-(KF170PT1)-WEB-2023-BABAS",
    "Cleora_Shephard-Swim-(HR161)-SINGLE-16BIT-WEB-FLAC-2020-MonolithsNitid",
    "Monolith.2022.1080p.BluRay.Remux.AVC.DTS-HD.MA.5.1-CiNEPHiLES",

    "Albatross.1996.1080p.AMZN.WEB-DL.DDP2.0.H.264-PandaMoon",
    "Mister.Rogers.Neighborhood.S12E10.Pets.A.Visit.with.Real.Pandas.and.a.Birthday.Parade.AAC2.0.1080p.x264-PoF",
    "Here.Is.Your.Life.1966.1080p.BluRay.FLAC1.0.x264-SADPANDA.mkv",

    "Achile-Kappa-(G0100042797863)-SINGLE-16BIT-WEB-FLAC-2020-PacificatedLittleness",
    "Kappa no ku to natsu yasumi [2007] 720p x264 Blu-Ray -CtrlHD",

    "Big_Youth-Natty_Cultural_Dread-(TRLS123)-LP-1976-Gully",
    "Der.Fluch.der.Natty.Knocks.2023.German.AC3.WEBRip.x264-ZeroTwo",
    "natty.knocks.2023.1080p.bluray.x264-pignus.mkv",
    "Black.Death.2010.1080p.Blu-ray.AVC.DTS-HD.MA.5.1-taterzero",

    "Baby Bandito S01 WEBRip EAC3 5 1 1080p x265-iVy",

    "Chronicles.of.The.Ghostly.tribe.2015.1080p.BluRay.x265.10bit.DTS-ADE",
    "The.Ghost.And.Molly.McGee.S01E07.Mamas.Gotta.Hustle.AAC5.1.1080p.WEBRip.x265-PoF",
    "Ghosts (2021) S03E10 1080p AMZN WEB-DL x265 SDR DDP 5.1 English-YELLO",
    "PervCity Krissy Lynn Mariah Madisynn Krissy Lynn and Mariah Madisynn In A Thick Ass Threesome XXX 2013 1080p HEVC-GhostFreakXX",

    "Time.2021.S01.DVDRip.AAC2.0.H.264-TABULARiA",
    "Eden.Log.2007.1080p.BluRay.REMUX.AVC.DTS-HD.MA.5.1-ImenSane"
]

utr_good_matches = [
    "The Spectacular Spider-Man - S01E06 - The Invisible Hand (1080p BDRip x265 HEVC 10bit AAC 5.1 RCVR) UTR",
    "The.Spectacular.Spider-Man-S01E09-The.Uncertainty.Principle.1080p.BDRip.x265.HEVC.10bit.AAC.5.1.RCVR.[UTR]",
    "Brigsby Bear (2017) (1080p BluRay x265 SDR AAC 5.1 English - Tigole UTR)",
    "Risky Business (1983) (1080p BluRay x265 SDR AAC 5.1 English - FreetheFish UTR)",
    "Labyrinth (1986) 30th Anniversary (1080p BluRay x265 SDR AAC 7.1 English - Tigole UTR)",
    "Love Actually (2003) (1080p BluRay x265 SDR AAC 5.1 English - Tigole UTR)",
    "The Simpsons (1989) S07 (480p DVD x265 SDR AAC 5.1 English - ImE UTR)",
    "The Simpsons (1989) S14 (1080p BluRay x265 SDR AAC 5.1 English - ImE UTR)"
]

utr_bad_matches = [
    "The.Outreau.Case.A.French.Nightmare.S01E01.The.Renard.Block.1080p.NF.WEB-DL.DDP5.1.H.264-NTb.mkv",
    "The.Outreau.Case.A.French.Nightmare.S01.1080p.NF.WEB-DL.DDP5.1.H.264-NTb",
    "Eva.Soda.Utroskab.med.den.første.kvinde.i.bilen.Sex.i.bilen.6462a7a8a5d9e.",
    "Outrage.1950.1080p.BluRay.Flac.2.0.x265.HEVC-Nb8.mkv",
    "Utro 1966 DANiSH 720p WEB-DL H 264 AAC2 0-TWA"
]

hone_good_matches = [
    "Criminal.Minds-Suspect.Behavior.2011.S01E01.1080p.AMZN.WEB-DL.x265.SDR.DDP5.1.English-Yogi.HONE",
    "The Bourne Supremacy (2004) Open Matte (1080p AMZN WEB-DL x265 SDR DDP 5.1 English - Yogi HONE)",
    "American Wedding (2003) Unrated (1080p BluRay x265 SDR DDP 5.1 English - Yogi HONE)"
]

hone_bad_matches = [
    "ASIAN KUNG-FU GENERATION - BEST HIT AKG Official Bootleg “HONE” (2018) [Anthology] [FLAC 24bit Lossless / WEB]"
]

def qxr(debug_level=0):
    # Get the custom formats for "QxR" from both Radarr and Sonarr
    QxR_radarr = get_custom_format("QxR", "radarr", debug_level)
    QxR_sonarr = get_custom_format("QxR", "sonarr", debug_level)

    # Extract the regex values for both Radarr and Sonarr using get_regex
    QxR_value_radarr = get_regex(QxR_radarr, "QxR", debug_level)
    QxR_value_sonarr = get_regex(QxR_sonarr, "QxR", debug_level)
    UTR_value_radarr = get_regex(QxR_radarr, "UTR (Title)", debug_level)
    UTR_value_sonarr = get_regex(QxR_sonarr, "UTR (Title)", debug_level)
    HONE_value_radarr = get_regex(QxR_radarr, "HONE", debug_level)
    HONE_value_sonarr = get_regex(QxR_sonarr, "HONE", debug_level)

    # Compare Radarr and Sonarr QxR regex values
    if QxR_value_radarr != QxR_value_sonarr:
        print("Test Failed: regex value not same.")
        print(f"Radarr regex: {QxR_value_radarr}")
        print(f"Sonarr regex: {QxR_value_sonarr}")
        sys.exit(1)

    if UTR_value_radarr != UTR_value_sonarr:
        print("Test Failed: regex value not same.")
        print(f"Radarr regex: {UTR_value_radarr}")
        print(f"Sonarr regex: {UTR_value_sonarr}")
        sys.exit(1)

    if HONE_value_radarr != HONE_value_sonarr:
        print("Test Failed: regex value not same.")
        print(f"Radarr regex: {HONE_value_radarr}")
        print(f"Sonarr regex: {HONE_value_sonarr}")
        sys.exit(1)

    if debug_level > 0:
        print(f"\n{ORANGE}Testing with regex: {QxR_value_radarr}{RESET}")
        print(f"{ORANGE}Testing with regex: {UTR_value_radarr}{RESET}")
        print(f"{ORANGE}Testing with regex: {HONE_value_radarr}{RESET}\n")

    # Replace the negative lookbehind with a negative lookahead
    QxR_value_radarr = QxR_value_radarr.replace(r"(?<=^|[\s.-])", r"(?:^|[\s.-])")
    QxR_value_sonarr = QxR_value_sonarr.replace(r"(?<=^|[\s.-])", r"(?:^|[\s.-])")
    UTR_value_radarr = UTR_value_radarr.replace(r"(?<=^|[\s.-])", r"(?:^|[\s.-])")
    UTR_value_sonarr = UTR_value_sonarr.replace(r"(?<=^|[\s.-])", r"(?:^|[\s.-])")
    HONE_value_radarr = HONE_value_radarr.replace(r"(?<=^|[\s.-])", r"(?:^|[\s.-])")
    HONE_value_sonarr = HONE_value_sonarr.replace(r"(?<=^|[\s.-])", r"(?:^|[\s.-])")

    good_matches_passed = []
    good_matches_failed = []
    bad_matches_passed = []
    bad_matches_failed = []

    print("Checking good matches for release groups:")
    # Test good matches
    for release in good_matches:
        if re.search(QxR_value_radarr, release, re.IGNORECASE):
            good_matches_passed.append(release)
            print(f"  - {release}: {GREEN}Passed{RESET}")
        else:
            good_matches_failed.append(release)
            print(f"  - {release}: {RED}Failed{RESET}")

    print("\nChecking bad matches for release groups:")
    # Test bad matches
    for release in bad_matches:
        if re.search(QxR_value_radarr, release, re.IGNORECASE):
            bad_matches_passed.append(release)
            print(f"  - {release}: {RED}Failed{RESET}")
        else:
            bad_matches_failed.append(release)
            print(f"  - {release}: {GREEN}Passed{RESET}")

    print("\nChecking good matches for UTR release groups:")
    # Test good matches
    for release in utr_good_matches:
        if re.search(UTR_value_radarr, release, re.IGNORECASE):
            good_matches_passed.append(release)
            print(f"  - {release}: {GREEN}Passed{RESET}")
        else:
            good_matches_failed.append(release)
            print(f"  - {release}: {RED}Failed{RESET}")

    print("\nChecking bad matches for UTR release groups:")
    # Test bad matches
    for release in utr_bad_matches:
        if re.search(UTR_value_radarr, release, re.IGNORECASE):
            bad_matches_passed.append(release)
            print(f"  - {release}: {RED}Failed{RESET}")
        else:
            bad_matches_failed.append(release)
            print(f"  - {release}: {GREEN}Passed{RESET}")

    print("\nChecking good matches for HONE release groups:")
    # Test good matches
    for release in hone_good_matches:
        if re.search(HONE_value_radarr, release, re.IGNORECASE):
            good_matches_passed.append(release)
            print(f"  - {release}: {GREEN}Passed{RESET}")
        else:
            good_matches_failed.append(release)
            print(f"  - {release}: {RED}Failed{RESET}")

    print("\nChecking bad matches for HONE release groups:")
    # Test bad matches
    for release in hone_bad_matches:
        if re.search(HONE_value_radarr, release, re.IGNORECASE):
            bad_matches_passed.append(release)
            print(f"  - {release}: {RED}Failed{RESET}")
        else:
            bad_matches_failed.append(release)
            print(f"  - {release}: {GREEN}Passed{RESET}")

    print("\nFailed matches:")
    for release in good_matches_failed + bad_matches_passed:
        print(f"  - {release}")

    # Calculate stats
    total_releases = len(good_matches) + len(bad_matches) + len(utr_good_matches) + len(utr_bad_matches) + len(hone_good_matches) + len(hone_bad_matches)
    total_fails = len(good_matches_failed) + len(bad_matches_passed)
    required_pass_rate = 99.8
    actual_pass_rate = ((total_releases - total_fails) / total_releases) * 100

    print("\nStats:")
    print(f"Total releases: {total_releases}")
    print(f"Total fails: {total_fails}")
    print(f"Required pass rate: {required_pass_rate}%")
    print(f"Actual pass rate: {actual_pass_rate:.2f}%")

    if actual_pass_rate >= required_pass_rate:
        return True
    else:
        return False