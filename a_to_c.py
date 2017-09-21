#!/usr/bin/env python3

# Converts the pitch and tempo of songs.

# Copyright 2017 Jonas Wagner <ltlygwayh@gmail.com>
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 
# 1. Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimer.
# 
# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

import argparse
import os
import shlex
import subprocess
import sys

FREQUENCIES = {
        'D': 146.83,
        'D#': 155.56,
        'Eb': 155.56,
        'E': 164.81,
        'F': 174.61,
        'F#': 185.00,
        'Gb': 185.00,
        'G': 196.00,
        'G#': 207.65,
        'Ab': 207.65,
        'A': 220.00,
        'A#': 233.08,
        'Bb': 233.08,
        'B': 246.94,
        'H': 246.94,
        'C': 261.6,
        }

COMMAND = ['ffmpeg', '-i', '{input_file}', '-filter:a',
        'asetrate={new_rate},atempo={tempo}', '-y', '{output_file}']


def output_path(input_path, source_note, target_note, tempo):
    basename, extension = os.path.splitext(input_path)
    result = basename
    if source_note != target_note:
        result += "-{source_note}-to-{target_note}".format(
                source_note=source_note, target_note=target_note)
    if abs(tempo - 1.0) > 0.01:
        result += "-{tempo:.2}".format(tempo=tempo)
    result += extension
    return result


def main():
    parser = argparse.ArgumentParser(description='Change pitch and speed of music')

    parser.add_argument('--source-note', '-s', default='A', choices=FREQUENCIES.keys(),
                        help='Current pitch of the song')
    parser.add_argument('--target-note', '-t', default='C', choices=FREQUENCIES.keys(),
                        help='Target pitch of the song')
    parser.add_argument('--tempo', '-f', type=float, default=1.0,
                        help='Factor by which to adjust the tempo')
    parser.add_argument('--verbose', '-v', action='store_true',
                        help='Be more verbose')
    parser.add_argument('files', nargs='+', help='Files to convert')
    args = parser.parse_args()

    errors = []

    for file_name in args.files:
        substitutions = {
                'input_file': file_name,
                'output_file': output_path(file_name, args.source_note,
                    args.target_note, args.tempo),
                'new_rate': int(44100 *
                    FREQUENCIES[args.target_note] /
                    FREQUENCIES[args.source_note]),
                'tempo': (args.tempo *
                    FREQUENCIES[args.source_note] /
                    FREQUENCIES[args.target_note]),
                }

        # FFMPEG's atempo filter supports values in the range of 0.5 to 2.0
        # only. Silently clamp it.
        substitutions['tempo'] = min(2.0, max(0.5, substitutions['tempo']))

        command = [c.format(**substitutions) for c in COMMAND]

        try:
            if args.verbose:
                print(" ".join(shlex.quote(c) for c in command))
                print()
                subprocess.run(command, check=True)
            else:
                subprocess.run(command, check=True,
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except subprocess.CalledProcessError as e:
            print(e, file=sys.stderr)
            errors.append(file_name)

    if errors:
        print("Conversion failed for the following files:")
        for file_name in errors:
            print("  {}".format(file_name))

    return len(errors)

if __name__ == '__main__':
    exit(main())
