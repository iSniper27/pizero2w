from gpiozero import TonalBuzzer
from gpiozero.tones import Tone
from time import sleep

buzzer = TonalBuzzer(13)

def playBuzzer(buzzer):
    buzzer.play(Tone("A4"))
    sleep(1)
    buzzer.stop()
    

playBuzzer(buzzer)