import time
import sys
from threading import Thread, Lock
import requests
import tempfile
from playsound import playsound

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
        ("\nAduh, Abang bukan maksudku begitu", 0.07),
        ("Masalah stecu bukan berarti tak mau", 0.07),
        ("Jual mahal dikit kan bisa", 0.06),
        ("Coba kase effort-nya saja", 0.06),
        ("Kalo memang cocok bisa datang ke rumah\n", 0.06),
        ("Stecu, stecu, stelan cuek baru malu", 0.09),
        ("Aduh, Ade ini mau juga Abang yang rayu", 0.06),
        ("Stecu, stecu, stelan cuek baru malu", 0.09),
        ("Aduh, Ade ini mau juga abang yang maju", 0.06),
    ]
    delays = [0.3, 3.7, 7.1, 8.7, 10.5, 13.7, 17.4, 20.4, 24.0]

    threads = []
    for i in range(len(lyrics)):
        lyric, speed = lyrics[i]
        t = Thread(target=sing_lyric, args=(lyric, delays[i], speed))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()

def download_and_play(url):
    resp = requests.get(url, stream=True)
    resp.raise_for_status()
    # simpan ke file sementara
    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp:
        for chunk in resp.iter_content(chunk_size=8192):
            if chunk:
                tmp.write(chunk)
        tmp_path = tmp.name

    # mainkan file mp3-nya
    playsound(tmp_path)

if __name__ == "__main__":
    audio_url = "https://files.catbox.moe/cett4d.mp3"
    # start audio di thread terpisah
    t_audio = Thread(target=download_and_play, args=(audio_url,))
    t_audio.start()

    # tampilkan lirik
    sing_song()

    # opsional: tunggu audio selesai
    t_audio.join()
