from numpy.testing import print_coercion_tables
from winerror import ERROR_DELETING_ICM_XFORM

print("******************************")
print("Welcome to the login system !")
print("******************************")
userattempt = 0
maxattempts = 3
finishattempts = 0

usernames = [
    "CosmicSloth_42",
    "NeonTigerX",
    "PixelWizard_99",
    "LunarFalcon",
    "CyberNova_7",
    "DuskRider_88",
    "VaporWaveFox",
    "ShadowPanda_3",
    "GlitchHawk_22",
    "FrostByte_Alpha",
    "EmberPhantom",
    "QuantumRaven_0",
    "SolarEclipse_5",
    "VelvetViper_19",
    "RogueNebula",
    "CipherMoose",
    "ArcaneJester_6",
    "BlazingYeti",
    "SilentTornado_1",
    "NovaStar_Omega"
]

passwords = [
    "Sunset72",
    "TigerPaw9",
    "BlueSky44",
    "ForestRun3",
    "GoldenEagle7",
    "Moonlight82",
    "StormChaser5",
    "WildFire11",
    "CrystalLake6",
    "ThunderBolt4",
    "SilentWave9",
    "RedDragon2",
    "FrozenRiver8",
    "ShadowFox3",
    "IronClad7",
    "MysticFog5",
    "RapidFire1",
    "SteelWing6",
    "DustyRoad4",
    "PhoenixRise9"
]



while userattempt < maxattempts:
    username = input("Please enter your username : ")
    password = input("Please enter your password : ")

    if username in usernames and password in passwords:
            print("Logged in successfully !")
            break
    else:
        userattempt += 1
        print("Wrong username or password !")
        print(f"You have {maxattempts - userattempt} attempts left!")


if finishattempts == 0:
    print("PLEASE TRY AGAIN AFTER 2 HOURS !!")

