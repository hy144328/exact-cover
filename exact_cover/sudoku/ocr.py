import csv
import itertools

import pytesseract

def parse_digit(img) -> tuple[int, float] | tuple[None, None]:
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

    for row_it in csv_data:
        print(row_it)

    csv_row = next(
        (row_it for row_it in csv_data if row_it["text"]),
        None,
    )
    if csv_row is None:
        return None, None

    if not csv_row["text"].isdigit():   # pragma: no cover
        raise ValueError(f"Text field is not numeric.")

    if not csv_row["conf"].isdigit():   # pragma: no cover
        raise ValueError(f"Conf field is not numeric.")

    return int(csv_row["text"]), 0.01 * int(csv_row["conf"])
