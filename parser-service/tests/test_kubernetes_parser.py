import os
from app.kubernetes_parser import parse_kubernetes


def test_kustomizegoat():

    folder = "benchmarks/kustomizegoat"

    for file in os.listdir(folder):

        if file.endswith(".yaml") or file.endswith(".yml"):

            path = os.path.join(folder, file)

            # IMPORTANT: Force UTF-8
            with open(path, encoding="utf-8", errors="ignore") as f:

                resources = parse_kubernetes(f.read())

                assert isinstance(resources, list)