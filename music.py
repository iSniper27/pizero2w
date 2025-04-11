from gpiozero import TonalBuzzer
from gpiozero.tones import Tone
from math import ceil
from time import sleep

# Note: gpiozero.Tone accepts standard note strings like "A4", "C#5", etc.
# So we can skip defining `tones` unless you want to validate or map manually.

class music:
    def __init__(self, songString='0 D4 8 0', looping=True, tempo=3, pin=None, pins=[13]):
        self.tempo = tempo  # Lower = faster playback
        self.song = songString
        self.looping = looping
        
        self.stopped = False
        
        self.timer = -1
        self.beat = -1
        self.arpnote = 0
        
        self.buzzers = []

        # Convert pin numbers to TonalBuzzers
        if pin is not None:
            pins = [pin]
        self.pins = pins
        for p in pins:
            self.buzzers.append(TonalBuzzer(p))
        
        self.notes = []
        self.playingNotes = []
        self.playingDurations = []

        # Calculate end of song
        self.end = 0
        splitSong = self.song.split(";")
        for note in splitSong:
            snote = note.split(" ")
            testEnd = round(float(snote[0])) + ceil(float(snote[2]))
            if testEnd > self.end:
                self.end = testEnd
        
        # Create empty song structure
        while len(self.notes) < self.end:
            self.notes.append(None)

        # Fill song structure
        for note in splitSong:
            snote = note.split(" ")
            beat = round(float(snote[0]))
            if self.notes[beat] is None:
                self.notes[beat] = []
            self.notes[beat].append([snote[1], ceil(float(snote[2]))])  # Note, Duration

        self.end = ceil(self.end / 8) * 8  # Round to nearest bar

    def stop(self):
        for buzzer in self.buzzers:
            buzzer.stop()
        self.stopped = True

    def restart(self):
        self.beat = -1
        self.timer = 0
        self.stop()
        self.buzzers = [TonalBuzzer(p) for p in self.pins]
        self.stopped = False

    def resume(self):
        self.stop()
        self.buzzers = [TonalBuzzer(p) for p in self.pins]
        self.stopped = False

    def tick(self):
        if self.stopped:
            return False

        self.timer += 1

        # Loop
        if self.timer % (self.tempo * self.end) == 0 and self.timer != 0:
            if not self.looping:
                self.stop()
                return False
            self.beat = -1
            self.timer = 0

        # On beat
        if self.timer % self.tempo == 0:
            self.beat += 1

            # Update durations and remove expired notes
            i = 0
            while i < len(self.playingDurations):
                self.playingDurations[i] -= 1
                if self.playingDurations[i] <= 0:
                    self.playingNotes.pop(i)
                    self.playingDurations.pop(i)
                else:
                    i += 1

            # Add new notes
            if self.beat < len(self.notes) and self.notes[self.beat]:
                for note in self.notes[self.beat]:
                    self.playingNotes.append(note[0])
                    self.playingDurations.append(note[1])

            # Play notes on available buzzers
            for i, buzzer in enumerate(self.buzzers):
                if i >= len(self.playingNotes):
                    buzzer.stop()
                else:
                    try:
                        buzzer.play(Tone(self.playingNotes[i]))
                    except:
                        buzzer.stop()

        # Arpeggiate remaining notes using last buzzer (if more notes than buzzers)
        if len(self.playingNotes) > len(self.buzzers):
            buzzer = self.buzzers[-1]
            if self.arpnote >= len(self.playingNotes) - len(self.buzzers) + 1:
                self.arpnote = 0
            try:
                buzzer.play(Tone(self.playingNotes[self.arpnote + len(self.buzzers) - 1]))
            except:
                buzzer.stop()
            self.arpnote += 1

        return True
