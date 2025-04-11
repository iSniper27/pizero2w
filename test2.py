from time import sleep

# Example song string from your comment
song = "0 D4 8 0;0 D5 8 0;0 G4 8 0;8 C5 2 0;10 B4 2 0;12 G4 2 0;14 F4 1 0;15 G4 17 0;16 D4 8 0;24 C4 8 0"

player = music(songString=song, tempo=3, pins=[13])  # One buzzer
# Or for polyphony: pins=[13, 14, 15]

while player.tick():
    sleep(0.01)
