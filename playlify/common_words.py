from typing import Set

def process_common_words() -> Set:
    results = set()
    file_path = 'playlify/common_words.txt'
    with open(file_path, 'r') as file:
        for line in file:
            line.strip()
            if line:
                song, uri = line.rsplit(',', 1)  # rsplit splits from the rightmost occurrence
                song, uri = song.strip(), uri.strip()
                results.add((song, uri))
    return results
