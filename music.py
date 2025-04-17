from gpiozero.tones import Tone

class music ():
    def __init__(self, song, buzzer):
        self.song = song
        self.buzzer = buzzer
        self.notes = []

        beats = self.song.split(";")
        for note in beats:
            splitNote = note.split(' ')
            self.notes.append(splitNote[1])