from Songbook import Songbook, decode_lines, log, decode_songfile
from Songbook import types
import json
from os import listdir
from collections import namedtuple



def main() -> None:
    with open("settings.json", "r") as f:
        settings = json.load(f)
    songbook = Songbook(settings["generator_settings"]["title"])
    songbook.add_title_page()
    files = listdir(settings["generator_settings"]["input_path"])
    log.debug(files)
    files.sort()
    for file in files:
        song: types.Song = decode_songfile(settings["generator_settings"]["input_path"] + file)
        songbook.add_song(song.meta["title"], song.meta["artist"], song.verses, song.scheme)
        print(songbook.pdf.pagenumber)
    songbook.add_index()
    songbook.output(settings["generator_settings"]["output_path"])

if __name__ == "__main__":
    main()