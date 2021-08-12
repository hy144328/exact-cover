#!/usr/bin/env python3

from collections.abc import Sequence

from cover import incidence as cover_incidence


class IncidenceMatrix(cover_incidence.IncidenceMatrix):
    @staticmethod
    def read_json(data: dict[object, Sequence]) -> "IncidenceMatrix":
        df = cover_incidence.IncidenceMatrix.read_json(data)
        return IncidenceMatrix(df.T)

