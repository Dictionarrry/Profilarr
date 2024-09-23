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
    "Black Sails 2014 S02 1080p BluRay x265 10bit DTS-HD MA 5.1 + DD 5.1-Goki TAoE",
    "The.Orville.2017.S03E04.Gently.Falling.Rain.1080p.HULU.Webrip.x265.10bit.EAC3.5.1-Goki[TAoE]",
    "Futurama S08E01 The Impossible Stream 1080p HULU WEBRip 10bit EAC3 5 1 x265 - Goki",
    "Star Trek-Strange New Worlds-2022-S02-1080p BDRip x265 10bit DTS-HD MA 5.1-Goki-T",
    "X-Men.97.2024.S01E03.Fire.Made.Flesh.REPACK.1080p.DSNP.Webrip.x265.10bit.EAC3.5.1.Atmos.GokiTAoE",
    "Primal (2019) S02E03 (1080p HMAX WEB-DL x265 SDR DD 5.1 English - Goki TAoE)",
    "Passengers.2016.2160p.HDR.BDRip.x265.10bit.AC3.5.1.Goki.TAoE",
    "Rick and Morty S04 Extras 1080p BluRay DD2.0 x265-Goki",
    "Gladiator.2000.Extended.2160p.HDR.BDRip.x265.10bit.AC3.5.1.Goki.TAoE",
    "Monsters.at.Work.2021.S02E04.Opening.Doors.1080p.HULU.Webrip.x265.10bit.EAC3.5.1.GokiTAoE",
    "American Dad (2005) S20E12 (1080p AMZN WEB-DL x265 SDR DDP 5.1 English - Goki TAoE)",
    "The Big Bang Theory S12E01 The Conjugal Configuration 1080p Webrip x265 EAC3 5.1 Goki [SEV]",
    "Star.Trek.Discovery.2017.S05E08.Labyrinths.1080p.AMZN.Webrip.x265.10bit.EAC3.5.1.GokiTAoE",
    "The.Great.North.2021.S02E01.Brace.Off.Adventure.1080p.HULU.Webrip.x265.10bit.EAC3.5.1-Goki[TAoE]",
    "Kung.Fu.Panda.4.2024.2160p.HDR10.DV.Hybrid.AMZN.Webrip.x265.10bit.EAC3.5.1.Atmos.Goki.TAoE",
    "Family.Guy.S19E13.PeTerminator.1080p.HULU.Webrip.x265.10bit.EAC3.5.1-Goki",
    "Koyaanisqatsi (1983) (1080p BDRip x265 10bit AC3 5 1 - Goki)[TAoE]",
    "The Simpsons (1989) S35E17 The Tipping Point (1080p HULU Webrip x265 10bit EAC3 5 1 - Goki)[TAoE]",
    "Bobs.Burgers.S03E01.Ear-Sy.Rider.1080p.AMZN.Webrip.x265.10bit.AC3.5.1.-.Goki",

    "SpongeBob.SquarePants.1999.S14E01.Single.Celled.Defense.1080p.AMZN.Webrip.x265.10bit.EAC3.2.0.Frys.TAoE",
    "SpongeBob.SquarePants.1999.S02E35-E36.Procrastination.and.Im.With.Stupid.1080p.AMZN.Webrip.x265.10bit.EAC3.2.0-Frys.[TAoE]",
    "The New Scooby-Doo Movies S01-S02 1080p BluRay AAC x265 10bit-Frys",
    "The Secret Squirrel Show (1966) S01-02+Specials (1080p DVDRip AI Upscale x265 10bit AC3 2 0 - Frys) [TAoE]",
    "SpongeBob.SquarePants.1999.S00E04.Ugh.1080p.AMZN.Webrip.x265.10bit.EAC3.2.0-Frys.[TAoE]",
    "Are You Afraid of the Dark (2019) S02 (1080p AMZN Webrip x265 10bit EAC3 2 0 - Frys) [TAoE]",
    "The Grinch Grinches the Cat in the Hat (1982) (1080p AMZN Webrip x265 10bit EAC3 2 0 - Frys) [TAoE] mkv",
    "SpongeBob SquarePants (1999) S14E06 (1080p AMZN WEB-DL x265 SDR DDP 2.0 English - Frys TAoE)",
    "Atom.Ant.(1965).S01.(1080p.AMZN.Webrip.x265.10bit.EAC3.2.0.-.Frys).[TAoE]",
    "The Dogfather (1974) S01 (1080p BluRay x265 SDR DD 2.0 English - Frys TAoE)",
    "Scooby-Doo.Shaggys.Showdown.2017.1080p.AMZN.WEBRip.x265.10bit.EAC3.5.1-Frys.TAoE",
    "Atom Ant (1965) S01E17 Bully For Atom Ant (1080p AMZN Webrip X265 10bit EAC3 2.0 - Frys) [TAoE]",
    "Misterjaw (1976) S01 (1080p BluRay x265 SDR DTS-HD MA 2.0 English - Frys TAoE)",
    "Roland and Rattfink (1968) S01 (1080p BluRay x265 SDR DTS-HD MA 2.0 English - Frys TAoE)",

    "Curb.Your.Enthusiasm.2000.S06E05.The.Freak.Book.1080p.AMZN.Webrip.x265.10bit.EAC3.2.0-JBENT[TAoE]",
    "For.All.Mankind.2019.S04E06.Leningrad.1080p.ATVP.Webrip.x265.10bit.EAC3.5.1.Atmos.English.JBENTTAoE",
    "For.All.Mankind.2019.S04E07.Crossing.the.Line.1080p.ATVP.Webrip.x265.10bit.EAC3.5.1.Atmos.English.JBENTTAoE",
    "Guardians.of.the.Galaxy.Vol.3.2023.1080p.BDRip.x265.10bit.TrueHD.7.1.Atmos.English.JBENT.TAoE",
    "Mayans.M.C..(2018).S05.(1080p.AMZN.Webrip.x265.10bit.EAC3.5.1.English.-.JBENT)[TAoE]",
    "Meg.2.The.Trench.2023.1080p.MA.Webrip.x265.10bit.EAC3.5.1.Atmos.English.JBENT.TAoE",
    "God.Is.a.Bullet.2023.Uncut.1080p.Webrip.x265.10bit.EAC3.5.1.English.JBENT.TAoE",
    "Young.Sheldon.2017.S07E03.A.Strudel.and.a.Hot.American.Boy.Toy.1080p.AMZN.Webrip.x265.10bit.EAC3.5.1.English.JBENTTAoE",
    "Young Sheldon (2017) S07E07 A Proper Wedding and Skeletons in the Closet (1080p AMZN Webrip x265 10bit EAC3 5 1 English - JBENT)[TAoE]",
    "Sound.of.Freedom.2023.1080p.AMZN.Webrip.x265.10bit.EAC3.5.1.English.JBENT.TAoE",
    "Young Sheldon-2017-S07E06 Baptists, Catholics and an Attempted Drowning-1080p AMZN Webrip x265 10bit EAC3 5.1 English-JBENT-TAoE",
    "Scrubs (2001) S06 (1080p AIUS DVDRip x265 10bit AC3 5 1 English - JBENT)[TAoE]",
    "Love.2016.S01E08.Closing.Title.Song.1080p.NF.Webrip.x265.10bit.AC3.5.1-JBENT[TAoE]",
    "M3GAN.2022.Unrated.1080p.BDRip.x265.10bit.EAC3.7.1.English.JBENT.TAoE",
    "For.All.Mankind.(2019).S02.(1080p.BDRip.x265.10bit.DTS-HD.MA.5.1.English.-.JBENT)[TAoE]",
    "Curb Your Enthusiasm (2000) S06 (1080p AMZN WEB-DL x265 SDR DDP 2.0 English - JBENT TAoE)",
    "Reno.911!.(2003).S03.REPACK.(1080p.AIUS.DVDRip.x265.10bit.AC3.2.0.English.-.JBENT)[TAoE]",
    "Mayans.M.C.(2018).S03E01.Pap.Struggles.with.the.Death.Angel.REPACK.(1080p.AMZN.Webrip.x265.10bit.EAC3.5.1-JBENT) TAoE",
    "Highlander (1986) Director's Cut REPACK (1080p BDRip x265 10bit AC3 5.1 - JBENT)[TAoE].mkv",
    "Workaholics 2011 S03 1080p BluRay x265 10bit AC3 5.1 - JBENT TAoE",
    "Younger 2015 S06 1080p AMZN Webrip x265 10bit EAC3 5.1 - JBENT TAoE",

    "Shogun (2024) S01E03 Tomorrow is Tomorrow (1080p DSNP Webrip x265 10bit EAC3 5 1 - DNU)[TAoE]",
    "Wonka.2023.1080p.DS4K.Webrip.x265.10bit.EAC3.5.1.Atmos.DNU.TAoE",
    "Sexy.Beast.2024.S01E04.Always.Wanted.to.See.That.Place....1080p.DS4K.AMZN.Webrip.x265.10bit.EAC3.5.1.DNUTAoE",
    "Halo.2022.S02E07.Thermopylae.1080p.AMZN.Webrip.x265.10bit.EAC3.5.1.DNUTAoE",
    "Masters.of.the.Air.2024.S01E02.Part.Two.1080p.DS4K.ATVP.Webrip.x265.10bit.EAC3.5.1.Atmos.DNUTAoE",
    "The Completely Made-Up Adventures of Dick Turpin (2024) S01 (1080p ATVP Webrip x265 10bit EAC3 5 1 Atmos - DNU)[TAoE]",
    "Wish.2023.1080p.DS4K.Webrip.x265.10bit.EAC3.5.1.Atmos.DNU.TAoE",
    "MotoGP S2024E94 Round 04 Gran Premio de España MotoGP Sprint Race 1080p Webrip x265 10bit AAC 2 0 - DNU",
    "MotoGP S2024E111 Round 05 Grand Prix de France MotoGP Qualifying Nr. 2 1080p Webrip x265 10bit AAC 2 0 - DNU",
    "The.Crown.2016.S06E03.Dis-Moi.Oui.1080p.NF.WEBRip.x265.10bit.EAC3.5.1-DNU.TAoE",
    "Rebel Moon - Part Two The Scargiver (2024) (1080p NF Webrip x265 10bit EAC3 5.1 Atmos - DNU)[TAoE].mkv",
    "Red.Eye.(2024).S01.(1080p.ITV.Webrip.x265.10bit.AAC.2.0.-.DNU)[TAoE]",
    "MotoGP.S01E01.Grand.Prix.of.Qatar.Qualifying.1.1080p.Webrip.x265.10bit.AAC.2.0.DNU",
    "The Completely Made-Up Adventures of Dick Turpin (2024) S01 (1080p ATVP WEB-DL x265 SDR DDP Atmos 5.1 English - DNU TAoE)",
    "Aquaman.and.the.Lost.Kingdom.2023.1080p.DS4K.AMZN.Webrip.x265.10bit.EAC3.5.1.Atmos-DNU[TAoE].mkv",
    "BMF (2021) S03E08 Code Red (1080p AMZN Webrip x265 10bit EAC3 5.1 - DNU)[TAoE].mkv",
    "Trigger Point 2022 S02 1080p STAN WEBRip DD+ 5.1 x265-DNU TAoE",

    "Fast X (2023) (1080p AMZN Webrip x265 10bit EAC3 5 1 English - Ainz)[TAoE]",
    "Silo (2023) S01E02 (1080p Webrip x265 EAC3 5 1 English - Ainz)[TAoE]",
    "Silo (2023) S01E05 (1080p Webrip x265 EAC3 5 1 English - Ainz)[TAoE]",
    "Silo.2023.S01E07.1080p.ATVP.Webrip.x265.10bit.EAC3.5.1.English.AinzTAoE",
    "Silo.2023.S01E08.1080p.ATVP.Webrip.x265.10bit.EAC3.5.1.English.AinzTAoE",
    "Doctor.Strange.in.the.Multiverse.of.Madness.(2022).(1080p.Webrip.x265.10.bit.EAC3.5.1.-.Ainz)[TAoE]",
    "The Outsider (2020) S01E02 Roanoke 1080p AMZN Webrip x265 10bit EAC3 5.1 - Ainz",
    "Invasion.2021.S01E07.Hope.1080p.Webrip.x265.10bit.EAC3.5.1.Ainz.TAoE",
    "Westworld (2016) S04E07 Metanoia (1080p HMAX Webrip x265 10 bit AC3 5 1 - Ainz)[TAoE]",
    "The Outsider (2020) S01E04 A Wide Place in the Road 1080p AMZN Webrip x265 10bit EAC3 5.1 - Ainz",
    "Invasion.2021.S01E08.Contact.1080p.Webrip.x265.10bit.EAC3.5.1.Ainz.TAoE",
    "Clarksons.Farm.2021.S02E02.1080p.AMZN.Webrip.x265.10.bit.EAC3.5.1.English.AinzTAoE",
    "The Winchesters (2022) S01E08 Hang on to Your Life (1080p AMZN Webrip x265 10bit EAC3 5 1 - Ainz) [TAoE]",
    "The Legend of Vox Machina (2022) S02E04 Those Who Walk Away (1080p AMZN Webrip x265 10bit EAC3 5 1 - Ainz)[TAoE]",
    "The.Legend.of.Vox.Machina.2019.S02E02.The.Trials.of.Vasselheim.1080p.Webrip.x265.10bit.EAC3.5.1.Ainz.TAoE",

    "Reacher (2022) S01 (1080p ANZM Webrip x265 10bit EAC3 5 1 - TheSickle)[TAoE]",
    "Encanto.2021.1080p.BDRip.x265.10bit.AC3.5.1.TheSickle.TAoE",
    "The Hobbit - The Battle of the Five Armies (2014) EE (1080p BDRip x265 10bit AC3 5 1 - TheSickle)[TAoE] mkv",
    "Vikings.2013.S03E01.Mercenary.1080p.BDRip.x265.10bit.AC3.5.1.TheSickleTAoE",
    "Luca.2021.1080p.BDRip.x265.10bit.AC3.5.1.TheSickle.TAoE",
    "Truth Seekers (2020) S01 (1080p AMZN WEB-DL x265 SDR DDP 5.1 English - TheSickle TAoE)",
    "Lara Croft - Tomb Raider (2001) (1080p BluRay x265 SDR DD 5.1 English - TheSickle TAoE)",
    "Lost in Space (2018) S03 (1080p NF WEB-DL x265 SDR DDP 5.1 English - TheSickle TAoE)",
    "Lost in Space (2018) S02 (1080p NF WEB-DL x265 SDR DDP 5.1 English - TheSickle TAoE)",
    "Tomb Raider (2018) (1080p BluRay x265 SDR DD 5.0 English - TheSickle TAoE)",

    "The Flash (2023) (1080p DS4K MA Webrip x265 10bit EAC3 5 1 Atmos English - ANONAZ)[TAoE]",
    "The.Boogeyman.2023.1080p.DS4K.MA.Webrip.x265.10bit.EAC3.5.1.Atmos.English.ANONAZ.TAoE",
    "Ant-Man.and.the.Wasp.Quantumania.2023.4Kto1080p.MA.Webrip.x265.10bit.EAC3.5.1.Atmos.ANONAZ.TAoE",
    "Jawan (2023) (1080p DS4K NF Webrip x265 10bit EAC3 5 1 Hindi - ANONAZ)[TAoE]",
    "Retribution (2023) (1080p DS4K AMZN WEB-DL x265 SDR DDP Atmos 5.1 English - ANONAZ TAoE)",
    "Aar Ya Paar (2022) S01E04 1080p WEB-DL x265 SDR DDP Atmos 5.1 Hindi-ANONAZ",
    "Kohrra.2023.S01E02.Episode.2.1080p.NF.Webrip.x265.10bit.EAC3.5.1.Atmos.Multi.ANONAZTAoE",
    "Jehanabad - Of Love & War (2023) S01E04 1080p DS4K WEB-DL x265 SDR DDP Atmos 5.1 Hindi-ANONAZ",
    "The Night Manager (2023) S01 (1080p DS4K DSNP WEB-DL x265 SDR DDP Atmos 5.1 Multi - ANONAZ TAoE)",
    "The Abyss (1989) Special Edition (1080p DS4K AMZN Webrip x265 10bit EAC3 5.1 Atmos English - ANONAZ)[TAoE].mkv",
    "Police Academy The Complete Collection (1984) (1080p BDRip x265 10bit EAC3 1 0 - Species180) [TAoE]",

    "Lexx (1997) S01 (1080p DVDRip x265 10bit AIUS PCM 2 0 - Species180) [TAoE]",
    "X-Men Collection (1080p BDRip x265 10bit DTS 7 1 - Species180) [TAoE]",
    "Superman - The Animated Series (1996) S01-S04 (1080p BDRip x265 10bit DTS-HD MA 2 0 - Species180) [TAoE]",
    "Goodnight.Sweetheart.1993.S03E01.Between.The.Devil.And.The.Deep.Blue.Sea.1080p.AIUS.DVDRip.x265.10bit.AC3.2.0.Species180.TAoE",
    "Lucifer (2015) S06 (1080p BDRip x265 10bit DTS 5 1 - Species180) [TAoE]",
    "Lucifer (2015) S01 (1080p BDRip x265 10bit DTS 5 1 - Species180) [TAoE]",
    "seaQuest.DSV.1993.S03E11.Brainlock.1080p.BDRip.x265.10bit.PCM.2.0.Species180.TAoE",
    "Dark Matter (2015) S01 (1080p BluRay x265 SDR DDP 5.1 English - Species180 TAoE)",
    "The Big Bang Theory (2007) S11 (1080p BluRay x265 SDR DTS-HD MA 5.1 English - Species180 TAoE)",

    "The.Lord.of.the.Rings.The.Two.Towers.2002.Extended.1080p.BDRip.x265.10bit.EAC3.5.1-r0b0t.[TAoE]",
    "The Lord of the Rings The Fellowship of the Ring (2001) Extended (1080p BDRip x265 10bit EAC3 5 1 - r0b0t) [TAoE]",
    "The Lord of the Rings The Return of the King (2003) Extended (1080p BDRip x265 10bit EAC3 5 1 - r0b0t) [TAoE]",
    "Jackass.3D.2010.Unrated.1080p.BDRip.x265.10bit.EAC3.5.1.r0b0t.TAoE",
    "Megamind.2010.1080p.BDRip.x265.10bit.TrueHD.7.1.r0b0t",
    "The.Man.with.the.Iron.Fists.2.2015.Unrated.1080p.BDRip.x265.10bit.DTS-HD.MA.5.1-r0b0t.[TAoE]",
    "Promising Young Woman (2020) (1080p BDRip x265 10bit AC3 5 1 - r0b0t) [TAoE] mkv",
    "Soul (2020) (1080p BDRip x265 10bit AC3 5 1 - r0b0t) [TAoE] mkv",
    "Hocus.Pocus..1993...2160p.HDR.BDRip.x265.10bit.DTS-HD.MA.5.1.+.AC3.5.1.r0b0t...TAoE.",
    "Skylines (2020) (1080p BDRip x265 10bit AC3 5 1 - r0b0t) [TAoE] mkv",
    "Robot.Chicken.S00E26.720p.AMZN.WEB-DL.DDP2.0.H.264-R0B0T",
    "Child's Play 2 (1990) (1080p BluRay x265 SDR DD 2.0 English - r0b0t TAoE)",

    "Game.of.Thrones.2011.S05E05.2160p.HDR.BDRip.x265.10bit.AC3.5.1-xtrem3x.[TAoE]",
    "House of 1000 Corpses 2003 1080p BDRip x265 10bit DTS-HD HRA 7.1 xtrem3x TAoE",
    "Home Alone 2 Lost in New York (1992) (1080p BDRip x265 10bit EAC3 5 1 - xtrem3x) [TAoE]",
    "Gamer (2009) Extended Cut (1080p BDRip x265 10bit EAC3 5 1 - xtrem3x) [TAoE]",
    "Tenet (2020) IMAX (2160p HDR BDRip x265 10bit AC3 5 1 - xtrem3x) [TAoE]",
    "Game.Of.Thrones.2011.S05e02.2160P.Hdr.Bdrip.X265.10Bit.Truehd.7.1.Atmos-Xtrem3x.[Taoe]",
    "The Recruit (2003) (1080p BDRip x265 10bit DTS-HD MA 5 1 - xtrem3x) [TAoE]",
    "Game.Of.Thrones.2011.S02e03.2160P.Hdr.Bdrip.X265.10Bit.Truehd.7.1.Atmos-Xtrem3x.[Taoe]",
    "Jay And Silent Bob Strike Back (2001) (1080p BluRay x265 SDR DDP 5.1 English - xtrem3x TAoE)",
    "Spartacus Blood And Sand (2010) S01 (1080p BluRay x265 SDR TrueHD 5.1 English - xtrem3x TAoE)",
    "Bad Santa (2003) UNRATED (1080p BDRip x265 10bit EAC3 5.1 - xtrem3x) [TAoE].mkv",
    "REQ at NZBSRUS.com - xtrem3x",

    "Marvels Ant-Man (2017) S01 (1080p DSNP Webrip x265 10bit EAC3 5 1 - HxD) [TAoE]",
    "Dynasty.2017.S01E01.I.Hardly.Recognized.You.1080p.AMZN.Webrip.x265.10bit.EAC3.5.1.HxD.TAoE",
    "Memorist - 1x01 (1080p WEBRip HEVC HxD)",
    "50 States of Fright (2020) S01 (1080p QUIBI WEB-DL x265 SDR AAC 2.0 English - HxD TAoE)",
    "365 - Repeat the Year (2020) S01 (1080p Webrip KOREAN x265 10bit AAC 2 0 - HxD) [TAoE]",
    "After Life (2019) S01 (1080p NF Webrip x265 10bit EAC3 5 1 - HxD) [TAoE]",
    "Buffaloed (2020) (1080p BDRip x265 10bit TrueHD 5 1 - HxD) [TAoE] mkv",
    "Pixar In Real Life (2019) S01E10 WALL·E - BnL Pop-up Shop (1080p DSNYP Webrip x265 10bit AAC 2 0 - HxD) [TAoE] mkv",
    "The.Tom.and.Jerry.Show.2014.S02E05.Squeaky.Clean.1080p.VRV.WEB-DL.x265.10bit.AAC.2.0-HxD.[TAoE]",
    "The Tom and Jerry Show (2014) S02E10 Cheesy Ball Run (1080p VRV WEB-DL x265 10bit AAC 2.0 - HxD) [TAoE]",
    "Alex Rider 2020 S01 1080p AMZN Webrip x265 10bit EAC3 5.1 - HxD TAoE",
    "Mr Sunshine S01 1080p AMZN WEBRip DD+ 5.1 x265-HxD",
    "365.Repeat.the.Year.2020.S01E01.I.Just.Want.to.Go.Back.to.How.Things.Were.Before.1080p.Webrip.x265.10bit.AAC.2.0.HxD.TAoE",
    "Breeders.2020.S01E01.No.Sleep.1080p.AMZN.WEB-DL.x265.HEVC.10bit.EAC3.5.1.HxD",
    "Miracle.Workers.2019.S01E05.3.Days.1080p.AMZN.Webrip.x265.10bit.EAC3.5.1.HxDTAoE",
    "Ip.Man.Kung.Fu.Master.2019.1080p.BluRay.REMUX.AVC.DTS-HD.MA.5.1-HxD.mkv",
    "Total Drama 2007 S01E27 Total Drama Drama Drama Drama Island PAL DVD DD2.0 MPEG-2 REMUX-HxD",

    "Snowden.2016.1080p.BDRip.x265.10bit.AC-3.5.1-ArcX.TAoE",
    "Blonde (2022) (1080p NF WEB-DL x265 SDR DDP Atmos 5.1 English ArcX TAoE)",
    "Spirited (2022) 1080p WED-DL x265 SDR DDP 5.1 English ArcX-TAoE",
    "Batwoman (2019) S03E01 Mad As a Hatter (1080p AMZN Webrip x265 10bit EAC3 5 1 - ArcX)[TAoE]",
    "The Boys (2019) S01 (1080p BDRip x265 10bit AC3 5 1 - ArcX)[TAoE]",
    "Batwoman.2019.S02E14.And.Justice.For.All.1080p.AMZN.Webrip.x265.10bit.EAC3.5.1-ArcX[TAoE]",
    "Dickie.Roberts.Former.Child.Star.2003.1080p.AMZN.Webrip.x265.10bit.EAC3.5.1.ArcX.TAoE",
    "Austin.Powers.The.Spy.Who.Shagged.Me.1999.1080p.BDRip.x265.10bit.TrueHD.5.1.ArcX.TAoE",
    "Things Heard And Seen (2021) (1080p Webrip x265 10bit EAC3 5.1 - ArcX)[TAoE]",
    "Batwoman.2019.S03E06.How.Does.Your.Garden.Grow.1080p.AMZN.Webrip.x265.10bit.EAC3.5.1.ArcXTAoE",
    "The.Woman.King.2022.1080p.AMZN.Webrip.x265.10bit.EAC3.5.1.ArcX.TAoE",

    "Chernobyl (2019) S01E04 The Happiness of All Mankind (1080p BDRip x265 10bit DTS-HD MA 5.1 - WEM) TAoE",
    "Deadmau5_and_Billy_Newton_Davis-Outta_My_Life_(PD4003)-WEB-2007-WEM",
    "3000 Miles to Graceland (2001) (1080p x265 SDR DDP 5.1 English - WEM TAoE)",
    "Chivalry (2022) S01 1080p ALL4 WEB-DL H264 AAC 2.0 English-WEM",
    "The Split (2018) S01 1080p BBC WEB-DL H264 AAC 2.0 English-WEM",
    "Agatha Christie's Poirot (1989) S01 - S13 (1080p BDRip x265 10bit Mixed - WEM)[TAoE]",
    "Shameless (2004) S11 (1080p NF Webrip x265 10bit EAC3 2 0 - WEM)[TAoE]",
    "Charmed (1998) S01 (1080p BDRip x265 10bit FLAC 2.0 - WEM)[TAoE]",
    "Chernobyl (2019) S01E01 1 - 23 - 45 (1080p BDRip x265 10bit DTS-HD MA 5.1 - WEM)[TAoE]",

    "Alcatraz (2012) S01 (1080p BDRip x265 10bit AC3 5 1 - Nostradamus)[TAoE]",
    "Supergirl (2015) S02 (1080p BDRip x265 10bit DTS-HD MA 5 1 - Nostradamus)[TAoE]",
    "Strange Days (1995) 20th Anniversary Edition (1080p BDRip x265 10bit DTS-HD MA 5 1 - Nostradamus)[TAoE]",

    "Aeon Flux (1991) S01-S03 (1080p AI Upscale x265 10bit EAC3 5 1 - Erie)[TAoE]",
    "Bill & Ted's Bogus Journey (1991) (1080p BDRip x265 10bit DTS-HD MA 5 1 - Erie) [TAoE]",
    "The Boys (2019) S02E02 Proper Preparation and Planning (1080p AMZN Webrip x265 10bit EAC3 5 1 - Erie) [TAoE] mkv",
    "The New Mutants (2020) (1080p BDRip x265 10bit AC3 5 1 - Erie) [TAoE]",

    "Wrath of the Titans (2012) (1080p BDRip x265 10bit EAC3 5 1 - DUHiT)[TAoE]",
    "Emma (2020) (1080p BDRip x265 10bit EAC3 5 1 - DUHiT)[TAoE]",
    "'71 (2014) (1080p BDRip x265 10bit EAC3 5 1 - DUHiT)[TAoE]",
    "1408 (2007) (1080p BDRip x265 10bit EAC3 5 1 - DUHiT)[TAoE]",

    "True Lies (1994) (1080p D-Theater Rip x265 10bit AC3 5 1 - jb2049) [TAoE]",
    "A Fish Called Wanda (1988) Arrow 4K Remaster (1080p BDRip x265 10bit AC3 5 1 + DTS-HD MA 5 1 - jb2049) [TAoE]",
    "Children of Dune (2003) S01 (1080p BDRip x265 10bit AC3 5 1 - jb2049) [TAoE]",

    "Angels in the Outfield (1994) (1080p AMZN Webrip x265 10bit EAC3 5.1 - DrainedDay)[TAoE].mkv",
    "Cabin Fever (2003) (1080p BluRay x265 SDR DD 5.1 English - DrainedDay TAoE)",
    "Veronica Mars S04 1080p Bluray DD 5.1 H.265-DrainedDay[TAoE]",
    "How.to.Get.Away.with.Murder.2014.S04E02.Im.Not.Her.1080p.AMZN.Webrip.x265.10bit.EAC3.5.1.DrainedDayTAoE",
    "Life S01 1080p AMZN WEBRiP DD+ 5.1 H265-DrainedDay TAoE",
    "DodgeBall A True Underdog Story (2004) (1080p BDRip x265 10bit AC3 5 1 - DrainedDay)[TAoE]",
    "Veronica.Mars.(2004).S02E19.Nevermind.the.Buttocks.(1080p.AMZN.Webrip.x265.10bit.EAC3.2.0-DrainedDay) TAoE",

    "Clean.with.Passion.for.Now.2018.S01E02.1080p.NF.Webrip.x265.10bit.EAC3.2.0.AJJMIN.TAoE",
    "Fight.For.My.Way.2017.S01E01.1080p.BDRip.x265.10bit.AC3.2.0-AJJMIN.[TAoE]",
    "Angel's Last Mission - Love (2019) S01 (1080p Webrip x265 10bit AAC 2 0 - AJJMIN) [TAoE]",
    "Euphoria (2019) S02E04 You Who Cannot See, Think of Those Who Can (1080p HMAX Webrip x265 10bit AC3 5 1 - AJJMIN) [TAoE]",
    "While You Were Sleeping (2017) S01 (1080p BDRip x265 10bit AC3 2 0 - AJJMIN) [TAoE]",
    "Moonshine.2021.S01E16.1080p.Webrip.x265.10bit.AAC.2.0.AJJMIN.TAoE"
]

bad_matches = [
    "ManyVids.2023.Mvngokitty.Homework.With.Stepmommy.XXX.720p.HEVC.x265.PRT[XvX]",
    "ご近所物語 第01-07巻 [Gokinjo Monogatari vol 01-07]",
    r"[Mazui]\_Gokicha!!\_Cockroach\_Girls\_-\_01\_[99E656EA]",
    "[Nerieru-Scans] Gokiburi Buster [Translated (Nerieru-Scans)]",
    "[Yuurisan-Subs] GokiMono S01 [DVD][MKV][h264][640x480][Vorbis 2.0][Softsubs (Yuurisan-Subs)]",
    "Guru Guru Gokil (2020) [720p] [WEBRip] [YTS] [YIFY]",
    "Gokicha.Cockroach.Girls.S01.WEBRip.AAC2.0.H.264-Mazui",

    "frys.planet.word.720p.hdtv.x264-ftp",
    "Fried Barry [2020] 1080p x264 Blu-Ray -TayTO",
    "Small Fry [2011] 720p x264 Blu-Ray -VietHD",
    "Stephen Frys 21st Century Firsts 2020 1080p HDTV H264-DARKFLiX",
    "Cycling.2022.03.03.Bloeizone.Fryslan.Tour-Stage.1.720p.WEB-DL.AAC2.0.H.264-VCNTRSH",
    "ried Green Tomatoes [1991] 1080p x264 Blu-Ray -decibeL",
    "Full.Frys.S01.DVDRip.AAC2.0.x264-iFLiX",
    "Magic.Numbers.Hannah.Frys.Mysterious.World.Of.Maths.S01E02.720p.iP.WEB-DL.AAC2.0.H.264-RTN",
    "Timo_de_Frys_-_Ministry_of_Beats_(Decibel)-CABLE-06-27-2014-TALiON",
    "Magic.Numbers.Hannah.Frys.Mysterious.World.of.Mathematics.S01E03.Weirder.and.Weirder.WEBRip.x264-ION10",
    "Timo_de_Frys_-_Ministry_of_Beats_(Decibel)-CABLE-07-06-2012-TALiON",
    "Kirsti Sparboe - Ikke Stå Og Frys - 46 Høydepunkter (1995) [Anthology] [FLAC Lossless / CD / Log (100%) / Cue]",

    "@sendnudesx.OnlyFans.Siterip.PPV.540p.720p.1080p.WEB-DL.AAC2.0.H.264",
    "Odnu-My.Own.Island-AB127-WEB-FLAC-2022-BABAS",
    "DFN5l3 GeoolML8Q143dnU5ig",
    "Lars Bedsted Gommesen - Endnu Levende-AUDiOBOOK-WEB-DK-2022-CRAViNGS iNT",
    "Die.goettliche.Ordnung.2017.DUAL.COMPLETE.BLURAY-iFPD",
    "Petr Muk - V Bludišti Dnů (2010) [Album] [FLAC Lossless / WEB]",
    "Helena Vondráčková & Jiří Korn - Těch Pár Dnů (2007) [Compilation] [FLAC Lossless / WEB]",

    "[REQ] Trainz.Railroad.Simulator.2006.Limited.Edition.DVD-RELOADED",
    "Trainz.A.New.Era-SKIDROW",
    "2 Chainz-Pretty Girls Like Trap Music-24BIT-WEB-FLAC-2017-TiMES",
    "[Ainz Ooal Gown] Overlord II - 02 VOSTFR (1280x720 8bit AAC) [877B3BD8]",

    "B.Traits_-_BBC_Radio1_(Guest_HXDB)-SAT-03-04-2013-TALiON",
    "BRAGKEN_and_HXDI_Stross-Mzansi-(SNA104)-WEB-2022-PTC",
    "[HxDOU] 魁拔之大战元泱界 / 魁拔2 / Kuiba 2 [1080p][无水印高画质下载版本首发，内详 / High quality / ENG SUB included]",

    "3qrCzoNqHV5ugNH4eEArcxXGVYeJIi9AIe0M5NOFpki",

    "Beyonce.Live.At.Wembley.2004.DVDRip.FLAC.x264-HANDJOB",
    "Black.Box.Wem.kannst.du.vertrauen.2023.German.AC3.WEBRip.x264-ZeroTwo",
    "Bring Me the Horizon: Live at Wembley 2015 BluRay 1080p DTS-HD MA 5.1 AVC REMUX-NOGROUP",
    "WOR 2023 10 05: Dynamite and NXT, TBS issues, Wembley, Title Tuesday battle",

    "Alberto_Ruiz-Nostradamus-(HEART050)-WEB-FLAC-2020-HRDT",
    "Friends_Of_Nostradamus_-_Die_Macht_Des_Boesen-Vinyl-1999-NBD",
    "Tosz.x.Alel-Life.Is.Just.A.Matter.Of.Time.(Alel.Remix)-(HTSLCTNS006)-SINGLE-16BIT-WEB-FLAC-2023-NostradamusCastable",
    "Nostradamus Effect S01E02 Da Vincis Armageddon iNTERNAL 720p HDTV x264-SUiCiDAL",

    "The.Lake.Erie.Murders.S02E04.720p.WEB.x264-57CHAN",
    "Carpool Karaoke - The Series (2017) S01 (1080p ATVP WEB-DL H265 SDR DD 5.1 English - HONE)",
    "A Series of Unfortunate Events (2017) S01 (1080p DS4K NF WEB-DL x265 SDR DDP 5.1 English - Ghost QxR)",
    "The Daughters of Erietown by Connie Schultz EPUB"

]

def taoe(debug_level=0):
    # Get the custom formats for "taoe" from both Radarr and Sonarr
    taoe_radarr = get_custom_format("taoe", "radarr", debug_level)
    taoe_sonarr = get_custom_format("taoe", "sonarr", debug_level)

    # Extract the regex values for both Radarr and Sonarr using get_regex
    taoe_value_radarr = get_regex(taoe_radarr, "taoe", debug_level)
    taoe_value_sonarr = get_regex(taoe_sonarr, "taoe", debug_level)

    # Replace the negative lookbehind with a negative lookahead
    taoe_value_radarr = taoe_value_radarr.replace(r"(?<=^|[\s.-])", r"(?:^|[\s.-])")
    taoe_value_sonarr = taoe_value_sonarr.replace(r"(?<=^|[\s.-])", r"(?:^|[\s.-])")

    if debug_level > 0:
        print(f"Testing with regex: {ORANGE}{taoe_value_radarr}{RESET}\n")

    # Compare Radarr and Sonarr taoe regex values
    if taoe_value_radarr != taoe_value_sonarr:
        print("Test Failed: regex value not same.")
        print(f"Radarr regex: {taoe_value_radarr}")
        print(f"Sonarr regex: {taoe_value_sonarr}")

    good_matches_passed = []
    good_matches_failed = []
    bad_matches_passed = []
    bad_matches_failed = []

    print("Checking good matches:")
    # Test good matches
    for release in good_matches:
        if re.search(taoe_value_radarr, release, re.IGNORECASE):
            good_matches_passed.append(release)
            print(f"  - {release}: {GREEN}Passed{RESET}")
        else:
            good_matches_failed.append(release)
            print(f"  - {release}: {RED}Failed{RESET}")

    print("\nChecking bad matches:")
    # Test bad matches
    for release in bad_matches:
        if re.search(taoe_value_radarr, release, re.IGNORECASE):
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