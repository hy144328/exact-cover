# Copyright (C) 2025  Hans Yu <hans.yu@outlook.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import argparse
import os.path
import tempfile
import urllib.parse

import cv2 as cv
import requests

import exact_cover.solve
import exact_cover.sudoku

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()

    session = requests.Session()
    session.headers.update({"User-Agent": "exact-cover"})

    if os.path.exists(args.filename):
        img = cv.imread(args.filename, cv.IMREAD_GRAYSCALE)
    elif urllib.parse.urlparse(args.filename).scheme != "":
        response = session.get(args.filename)
        response.raise_for_status()

        with tempfile.TemporaryDirectory() as dir_name:
            with tempfile.NamedTemporaryFile(
                suffix = os.path.splitext(args.filename)[1],
                dir = dir_name,
                delete = False,
            ) as f:
                f.write(response.content)

            img = cv.imread(f.name, cv.IMREAD_GRAYSCALE)
    else:
        raise FileNotFoundError(args.filename)

    assert img is not None
    puzzle = exact_cover.sudoku.read_sudoku(img)
    solver = exact_cover.solve.AlgorithmX()

    print("Puzzle:")
    print(puzzle)
    print("\n")

    print("Solutions:")
    for sol_it in puzzle.solve(solver):
        print(sol_it)
        print("\n")

if __name__ == "__main__":
    main()
