from gpiozero import TonalBuzzer
from gpiozero.tones import Tone
from time import sleep

buzzer = TonalBuzzer(13)

def playBuzzer(buzzer):
    buzzer.play(Tone("A4"))
    sleep(0.2)
    buzzer.play(Tone("B4"))
    sleep(0.2)
    buzzer.play(Tone("C4"))
    sleep(0.2)
    buzzer.play(Tone("D4"))
    sleep(0.2)
    buzzer.play(Tone("E4"))
    sleep(0.2)
    buzzer.play(Tone("F4"))
    sleep(0.2)
    buzzer.stop()
    

playBuzzer(buzzer)