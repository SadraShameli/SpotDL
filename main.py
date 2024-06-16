import os
import multiprocessing
from multiprocessing import Process
from typing import List
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


def download_songs(urls_list, dir):
    urls = urls_list if isinstance(urls_list, str) else " ".join(urls_list)
    output = f'"{dir}/{{list-name}}/{{artists}} - {{title}}.{{output-ext}}" --threads {multiprocessing.cpu_count()}'
    command = f"spotdl download {urls} --output {output}"
    os.system(command)

    # --threads {multiprocessing.cpu_count()


def main():
    output_dir = "downloaded"
    os.makedirs(output_dir, exist_ok=True)
    urls = get_songs_list("urls")

    processes: List[Process] = []
    for url in urls:
        p = Process(
            target=download_songs,
            args=(
                url,
                output_dir,
            ),
        )
        p.start()
        processes.append(p)

    for p in processes:
        p.join()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)
