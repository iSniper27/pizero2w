from time import sleep
from music import Music

song = '0 D4 8 0;0 D5 8 0;0 G4 8 0;8 C5 2 0;10 B4 2 0;12 G4 2 0;14 F4 1 0;15 G4 17 0'
music_player = Music(songString=song, tempo=3, pins=[13])

try:
    while music_player.tick():
        sleep(0.01)  # Adjust timing if needed for smoother playback
except KeyboardInterrupt:
    music_player.stop()
