# play_song.py

from time import sleep
from music import music

# Example song string (you can generate these from onlinesequencer.net)
song = "0 D4 8 0;0 D5 8 0;0 G4 8 0;8 C5 2 0;10 B4 2 0;12 G4 2 0;14 F4 1 0;15 G4 17 0;16 D4 8 0;24 C4 8 0"

# Create music player instance
# If you have only one buzzer, keep pins=[13]; otherwise, add more pins for polyphony
player = music(songString=song, tempo=3, pins=[13])

# Play the song
while player.tick():
    sleep(0.01)  # Short delay for smooth playback
