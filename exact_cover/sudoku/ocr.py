import csv
import itertools
import typing

import pytesseract

def parse_digit(img) -> typing.Tuple[int, float] | typing.Tuple[None, None]:
    res = pytesseract.image_to_data(
        img,
        config = "--psm 10 outputbase digits",
    )

    csv_reader = csv.reader(res.split("\n"), delimiter="\t")
    csv_header = next(csv_reader)

    if "text" not in csv_header:
        raise KeyError(f"TSV header missing text field.")

    if "conf" not in csv_header:
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

    if not csv_row["text"].isdigit():
        raise ValueError(f"Text field is not numeric.")

    if not csv_row["conf"].isdigit():
        raise ValueError(f"Conf field is not numeric.")

    return int(csv_row["text"]), 0.01 * int(csv_row["conf"])
