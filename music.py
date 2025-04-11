from gpiozero import PWMOutputDevice
from time import sleep
from math import ceil

tones = {
    'C4': 262, 'D4': 294, 'E4': 330, 'F4': 349,
    'G4': 392, 'A4': 440, 'B4': 494,
    'C5': 523, 'D5': 587, 'E5': 659, 'F5': 698,
    'G5': 784, 'A5': 880, 'B5': 988
    # Add more tones as needed...
}

class TonePWM:
    def __init__(self, pin):
        self.device = PWMOutputDevice(pin)
        self.pin = pin
        self.frequency = 440
        self.active = False

    def freq(self, frequency):
        self.frequency = frequency

    def duty(self, duty_cycle):
        if duty_cycle == 0:
            self.device.off()
            self.active = False
        else:
            self.device.value = 0.5  # Simulate square wave, 50% duty
            self.active = True

    def deinit(self):
        self.device.off()
        self.active = False

    def play_tone(self, freq, duration):
        period = 1.0 / freq
        half = period / 2
        cycles = int(duration * freq)
        for _ in range(cycles):
            self.device.on()
            sleep(half)
            self.device.off()
            sleep(half)

class Music:
    def __init__(self, songString='0 D4 8 0', looping=True, tempo=3, pin=17, pins=None):
        self.tempo = tempo
        self.song = songString
        self.looping = looping

        if pins is None:
            pins = [pin]
        self.pwms = [TonePWM(p) for p in pins]
        self.notes = []
        self.playingNotes = []
        self.playingDurations = []
        self.stopped = False
        self.timer = 0
        self.beat = -1
        self.arpnote = 0

        # Find song length
        self.end = 0
        splitSong = self.song.split(";")
        for note in splitSong:
            snote = note.split(" ")
            testEnd = round(float(snote[0])) + ceil(float(snote[2]))
            if testEnd > self.end:
                self.end = testEnd

        while len(self.notes) < self.end:
            self.notes.append(None)

        for note in splitSong:
            snote = note.split(" ")
            beat = round(float(snote[0]))
            if self.notes[beat] is None:
                self.notes[beat] = []
            self.notes[beat].append([snote[1], ceil(float(snote[2]))])

        self.end = ceil(self.end / 8) * 8

    def stop(self):
        for pwm in self.pwms:
            pwm.deinit()
        self.stopped = True

    def restart(self):
        self.beat = -1
        self.timer = 0
        self.stop()
        self.pwms = [TonePWM(p.pin) for p in self.pwms]
        self.stopped = False

    def resume(self):
        self.stop()
        self.pwms = [TonePWM(p.pin) for p in self.pwms]
        self.stopped = False

    def tick(self):
        if self.stopped:
            return False

        self.timer += 1

        if self.timer % (self.tempo * self.end) == 0 and self.timer != 0:
            if not self.looping:
                self.stop()
                return False
            self.beat = -1
            self.timer = 0

        if self.timer % self.tempo == 0:
            self.beat += 1

            i = 0
            while i < len(self.playingDurations):
                self.playingDurations[i] -= 1
                if self.playingDurations[i] <= 0:
                    self.playingNotes.pop(i)
                    self.playingDurations.pop(i)
                else:
                    i += 1

            if self.beat < len(self.notes) and self.notes[self.beat]:
                for note in self.notes[self.beat]:
                    self.playingNotes.append(note[0])
                    self.playingDurations.append(note[1])

            for i, pwm in enumerate(self.pwms):
                if i >= len(self.playingNotes):
                    pwm.duty(0)
                else:
                    pwm.freq(tones.get(self.playingNotes[i], 440))
                    pwm.duty(1)

        if len(self.playingNotes) > len(self.pwms):
            arp_pwm = self.pwms[-1]
            if self.arpnote >= len(self.playingNotes) - len(self.pwms):
                self.arpnote = 0
            note = self.playingNotes[self.arpnote + (len(self.pwms) - 1)]
            arp_pwm.freq(tones.get(note, 440))
            arp_pwm.duty(1)
            self.arpnote += 1

        return True
