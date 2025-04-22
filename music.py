from time import sleep

class Note():
    def __init__(self, time, tone, duration):
        self.time = float(time)
        self.tone = tone
        self.duration = float(duration)

class music():
    def __init__(self, song):
        self.notes = []
        beats = self._trim_song(song)
        for note in beats:
            parts = note.split()
            if len(parts) == 3:
                self.notes.append(Note(parts[0], parts[1], parts[2]))

    def _trim_song(self, raw_song):
        entries = raw_song.strip().split(";")
        trimmed = []
        for entry in entries:
            parts = entry.strip().split()
            if len(parts) >= 3:
                trimmed.append(f"{parts[0]} {parts[1]} {parts[2]}")
        return trimmed

    def play(self, buzzer):
        for i, note in enumerate(self.notes):
            buzzer.play(note.tone)
            sleep(note.duration)
            buzzer.stop()
            # Optional: Add delay to account for timing differences
            if i + 1 < len(self.notes):
                next_note = self.notes[i + 1]
                gap = next_note.time - (note.time + note.duration)
                if gap > 0:
                    sleep(gap)


class MockBuzzer():
    def play(self, tone):
        print(f"Playing {tone}")

    def stop(self):
        print("Stopped")