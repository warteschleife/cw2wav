# -*- coding: <encoding name> -*-
"""
This module provides the function play_sound(), which expects the name of a WAV-file as parameter.
If the system provides the winsound lib, the function will use the lib to play the WAV-file.
Otherwise, it just prints a message that the WAV file has to be played manually by the user.
"""

# The default behaviour of 'play_sound()' is to just print a message:
play_sound = lambda x: print("No player found. You have to play '" + str(x) +
                             "' manually.")

# Try to import the winsound lib and - on success - provide an appropriate
# implementation of 'play_sound()'
try:
    import importlib
    if importlib.util.find_spec("winsound"):
        import winsound
        play_sound = lambda file_name: winsound.PlaySound(
            file_name, winsound.SND_FILENAME)
except:
    pass
