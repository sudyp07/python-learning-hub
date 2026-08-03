usernames = ["CosmicSloth_42", "NeonTigerX", "PixelWizard_99", "LunarFalcon", "CyberNova_7", "DuskRider_88", "VaporWaveFox", "ShadowPanda_3", "GlitchHawk_22", "FrostByte_Alpha", "EmberPhantom", "QuantumRaven_0", "SolarEclipse_5", "VelvetViper_19", "RogueNebula", "CipherMoose", "ArcaneJester_6", "BlazingYeti", "SilentTornado_1", "NovaStar_Omega", "EchoWolf_12", "CrimsonComet", "TurboFalcon_9", "ZenithKnight", "MysticCobra_77", "TurboPanda", "IcePhoenix_21", "GhostVortex", "StormFalcon_3", "DarkNebula", "RapidShadow_55", "NovaWolf", "IronFalcon_88", "BlueInferno", "CyberKnight_14", "PixelStorm", "ElectricFox_7", "SilentSamurai", "FrozenOrbit", "AlphaTitan_99", "NightCrawler_X", "QuantumTiger", "ThunderNova", "ShadowRogue_5", "SolarDragon", "TurboWizard", "MysticKnight_8", "FireEagle_47", "GlacierWolf", "StealthPanther"]

username = input("Enter your username: ").lower()


if username in usernames:
    print(f"{username} is already taken")
    exit()
else:
    print(f"{username} is available for you !!")