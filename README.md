A to C
======

`a_to_c.py` is a script to convert songs from one pitch to the other, and
optionally change their tempo.

This work was inspired by the great harmonica study songs from
<https://www.bluesharmonica.com/>. The music files from that website are created
for an A-harmonica, but the author of `a_to_c` only owns a C-harmonica.


Usage
-----

    a_to_c.py [-h]
              [--source-note {D,D#,Eb,E,F,F#,Gb,G,G#,Ab,A,A#,Bb,B,H,C}]
              [--target-note {D,D#,Eb,E,F,F#,Gb,G,G#,Ab,A,A#,Bb,B,H,C}]
              [--tempo TEMPO] [--verbose]
              files [files ...]

### Examples

Convert a song from the key of A to the key of C, without changing the tempo.
This is the default operation:

    ./a_to_c.py song.mp3

This will create `song-A-to-C.mp3` in the same folder as the song.

Batch-convert all files in the `exercise3` folder, changing pitch from A to G
and slowing down the songs to 80% speed for practice:

    ./a_to_c.py -s A -t G --tempo 0.8 exercise3/*.mp3


Installation
------------

`a_to_c.py` uses Python 3 and FFMPEG.

On Mac OS:

    brew install python3 ffmpeg

On Debian, Ubuntu and similar Linuxes:

    sudo apt install python3 ffmpeg

On Windows, I don't know... Suggestions to update this documentation are
welcome.

Once the dependencies are installed, simply download and run the `a_to_c.py`
file.
