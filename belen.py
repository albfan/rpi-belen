#!/usr/bin/env python

import time
import sys
import os
from tinytag import TinyTag
from playsound import playsound
from multiprocessing import Pool
import random
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(8, GPIO.OUT, initial=GPIO.LOW)

def switch_lights(max_random_wait = 0):
    while True:
            GPIO.output(8, GPIO.LOW)
            if max_random_wait > 0:
                waiting = random.random() * max_random_wait
                print("lights off %d" % waiting)
                time.sleep(waiting)
       
            GPIO.output(8, GPIO.HIGH)
            waiting = random.random() * max_random_wait
            print("lights on %d" % waiting)
            time.sleep(waiting)
       


def play_dir(dir, max_random_wait = 0, min_play_sound = 0):
    while True:
        for sound in os.listdir (dir):
            if max_random_wait > 0:
                waiting = random.random() * max_random_wait
                print("waiting %s: %d" % (dir, waiting))
                time.sleep(waiting)
       
            if os.path.isdir(sound):
                continue
            file = os.path.join (dir, sound)
            tag = TinyTag.get(file)
            duration = tag.duration
            print ("%s, %d" % (file, duration))
            time_playing = 0
            while time_playing <= min_play_sound:
                playsound (file)
                time_playing = time_playing + duration

            """
            for i in range(100):
                time.sleep(duration/100)
                sys.stdout.write("\r%d%%" % i)
                sys.stdout.flush()
            """

if __name__ == '__main__':
    pool = Pool () 
    result = pool.apply_async (play_dir, ["music", 120]) 
    result = pool.apply_async (play_dir, ["ambient", 60]) 
    result = pool.apply_async (play_dir, ["sounds", 10, 10]) 
    result = pool.apply_async (switch_lights, [100]) 
    pool.close ()
    pool.join ()
    
