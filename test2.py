
from gpiozero import Pin
from music import music
from time import sleep

f = open('words.txt', 'r')
song = f.read()

#One buzzer on pin 0
mySong = music(song, pins=[Pin(13)])

#Four buzzers
#mySong = music(song, pins=[Pin(0),Pin(1),Pin(2),Pin(3)])

while True:
    print(mySong.tick())
    sleep(0.04)