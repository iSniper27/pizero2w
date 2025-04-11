from gpiozero import TonalBuzzer
from gpiozero.tones import Tone

buzzer = TonalBuzzer(13)

def playBuzzer(buzzer):
    buzzer.play(Tone("A4"))

playBuzzer(buzzer)