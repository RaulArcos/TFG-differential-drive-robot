import pygame

# Initialize pygame mixer
pygame.mixer.init()

# Load the MP3 file
pygame.mixer.music.load('/home/robot/rah01/sounds/whatsapp.mp3')

# Play the MP3 file
pygame.mixer.music.play()

# Keep the program running while the music plays
# You can replace this with any other way to keep the program running
import time
while pygame.mixer.music.get_busy(): 
    time.sleep(1)