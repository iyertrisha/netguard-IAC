import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.terraform_parser import parse_terraform
import os

def test_terragoat_files():

    folder = "benchmarks/terragoat"

    for file in os.listdir(folder):

        if file.endswith(".tf"):

            with open(os.path.join(folder,file), encoding="utf-8") as f:

                resources = parse_terraform(f.read())

                assert isinstance(resources,list)