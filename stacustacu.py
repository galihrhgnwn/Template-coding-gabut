import time
from threading import Thread, Lock
import sys

lock = Lock()

def animate_text(text, delay=0.1):
    with lock:
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(delay)
        print()

def sing_lyric(lyric, delay, speed):
    time.sleep(delay)
    animate_text(lyric, speed)

def sing_song():
    lyrics = [
        ("\nAduh abang bukan maksudku begitu", 0.10),
        ("masalah stecu bukan bearti tak mau", 0.09),
        ("jual mahal dikit kan bisa", 0.08),
        ("coba kasi effortnya saja...", 0.09),
        ("kalau emang cocok bisa datang kerumah\n", 0.07),
    ]
    
    # jeda antar lirik (detik) → biar enak sesuai nyanyian
    gaps = [0.3, 4.0, 4.0, 3.0, 3.0]  
    
    # hitung delay kumulatif
    delays = []
    total = 0
    for g in gaps:
        total += g
        delays.append(total)

    threads = []
    for i in range(len(lyrics)):
        lyric, speed = lyrics[i]
        t = Thread(target=sing_lyric, args=(lyric, delays[i], speed))
        threads.append(t)
        t.start()
    
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    sing_song()
