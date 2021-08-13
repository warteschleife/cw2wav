# -*- coding: <encoding name> -*-

play_sound = lambda x: print("No player found. You have to play '" + str(x) +
                             "' manually.")
try:
    import importlib
    if importlib.util.find_spec("winsound"):
        import winsound
        winsound_support = True
        play_sound = lambda file_name: winsound.PlaySound(
            file_name, winsound.SND_FILENAME)
except:
    pass
