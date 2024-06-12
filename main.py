import os
import multiprocessing
from urllib.parse import urlparse, urlunparse


def get_song_list_from_files(dir):
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


def download_song(song_url, dir):
    try:
        command = f'spotdl download {" ".join(song_url)} --output "{dir}/{{list-name}}/{{artists}} - {{title}}.{{output-ext}}" --threads {multiprocessing.cpu_count()}'
        os.system(command)
    except Exception as e:
        print(f"Error downloading {song_url}: {e}")


def main():
    dir = "downloaded"
    os.makedirs(dir, exist_ok=True)
    song_list = get_song_list_from_files("urls")
    download_song(song_list, dir)


if __name__ == "__main__":
    main()
