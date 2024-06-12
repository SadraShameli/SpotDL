import os
import sys
import multiprocessing
from urllib.parse import urlparse, urlunparse


def get_songs_list(dir):
    song_set = set()
    current_directory = os.path.join(os.getcwd(), dir)
    for filename in os.listdir(current_directory):
        if filename.endswith(".txt"):
            filepath = os.path.join(current_directory, filename)
            with open(filepath, "r") as file:
                urls = file.read().splitlines()
                for url in urls:
                    parsed_url = urlparse(url)
                    clean_url = urlunparse(
                        (
                            parsed_url.scheme,
                            parsed_url.netloc,
                            parsed_url.path,
                            "",
                            "",
                            "",
                        )
                    )
                    song_set.add(clean_url)
    return list(song_set)


def download_songs(song_url, dir):
    url = song_url if isinstance(song_url, str) else " ".join(song_url)
    output = f'"{dir}/{{list-name}}/{{artists}} - {{title}}.{{output-ext}}"'
    command = f"spotdl download {url} --output {output} --threads {multiprocessing.cpu_count()}"
    os.system(command)


def main():
    dir = "downloaded"
    os.makedirs(dir, exist_ok=True)
    songs = get_songs_list("urls")
    download_songs(songs, dir)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)
