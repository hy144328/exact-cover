#!/usr/bin/env python3

from cover import links as cover_links


class DancingLinks(cover_links.DancingLinks):
    @staticmethod
    def read_json(data: dict[object, list]) -> "DancingLinks":
        constraints = list(data.keys())
        choices = set()
        choices = list(constraints.union(*data.values()))

        res = DancingLinks(choices, constraints)
        for constraint_it in data:
            for choice_it in data[constraint_it]:
                res.insert(Node(), choice_it, constraint_it)

        return res
