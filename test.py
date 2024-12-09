import pygame
import psutil
import random
import time

# Initialize pygame mixer
pygame.mixer.init()

# Function to load songs from a file
def load_songs_from_file(filename="songs.txt"):
    try:
        with open(filename, "r") as file:
            song_list = file.read().splitlines()
        return song_list
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        return []

# Function to monitor above-average network activity with decay
def detect_network_activity(interval=1, decay_rate=0.8, threshold_factor=1.5):
    # Store network stats over time
    prev_stats = psutil.net_io_counters()
    byte_diff_history = []  # List to store byte differences

    while True:
        time.sleep(interval)
        current_stats = psutil.net_io_counters()

        # Calculate byte differences
        bytes_sent_diff = current_stats.bytes_sent - prev_stats.bytes_sent
        bytes_recv_diff = current_stats.bytes_recv - prev_stats.bytes_recv
        byte_diff_history.append((bytes_sent_diff, bytes_recv_diff))

        # Calculate the average byte difference over the history
        avg_sent_diff = sum(x[0] for x in byte_diff_history) / len(byte_diff_history) if byte_diff_history else 0
        avg_recv_diff = sum(x[1] for x in byte_diff_history) / len(byte_diff_history) if byte_diff_history else 0

        # Decay the activity sensitivity over time
        avg_sent_diff *= decay_rate
        avg_recv_diff *= decay_rate

        # Compare current activity with average activity
        if (bytes_sent_diff > avg_sent_diff * threshold_factor or
            bytes_recv_diff > avg_recv_diff * threshold_factor):
            return True
        
        prev_stats = current_stats

# Function to play music from the list
def play_music_from_list():
    song_list = load_songs_from_file()  # Load songs from songs.txt
    if not song_list:
        print("No songs found to play.")
        return
    
    for song in song_list:
        print(f"Now playing: {song}")
        pygame.mixer.music.load(song)
        pygame.mixer.music.play(loops=0)  # Play the song once
        while pygame.mixer.music.get_busy():  # Wait for the song to finish
            if detect_network_activity():
                print("Above average network activity detected! Skipping...")
                # Skip a random amount of time (1-5 seconds)
                skip_time = random.randint(1, 5)  # Seconds to skip
                current_pos = pygame.mixer.music.get_pos() // 1000  # Current position in seconds
                new_pos = current_pos + skip_time
                pygame.mixer.music.set_pos(new_pos)

# Start the music player
play_music_from_list()

