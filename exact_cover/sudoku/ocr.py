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

import csv
import itertools

import pytesseract

def parse_digit(img) -> tuple[int | None, float | None]:
    res = pytesseract.image_to_data(
        img,
        config = "--psm 10 outputbase digits",
    )

    csv_reader = csv.reader(res.split("\n"), delimiter="\t")
    csv_header = next(csv_reader)

    if "text" not in csv_header:    # pragma: no cover
        raise KeyError(f"TSV header missing text field.")

    if "conf" not in csv_header:    # pragma: no cover
        raise KeyError(f"TSV header missing conf field.")

    csv_data = [
        dict(itertools.zip_longest(csv_header, row_it))
        for row_it in csv_reader
    ]

    csv_row = next(
        (row_it for row_it in csv_data if row_it["text"]),
        None,
    )
    if csv_row is None:
        return None, None

    try:
        return int(float(csv_row["text"])), 0.01 * float(csv_row["conf"])
    except ValueError:  # pragma: no cover
        return None, 0.01 * float(csv_row["conf"])
