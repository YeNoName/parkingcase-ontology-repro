# run_sparql.py
import argparse
from rdflib import Graph

def guess_format(path: str) -> str:
    p = path.lower()
    if p.endswith(".ttl") or p.endswith(".owl"):
        return "turtle"
    if p.endswith(".nt"):
        return "nt"
    if p.endswith(".rdf") or p.endswith(".xml"):
        return "xml"
    return "turtle"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", nargs="+", required=True)
    ap.add_argument("--query", required=True)
    args = ap.parse_args()

    g = Graph()
    for f in args.data:
        g.parse(f, format=guess_format(f))

    q = open(args.query, "r", encoding="utf-8-sig").read().lstrip()
    res = g.query(q)

    vars_ = [str(v) for v in res.vars]
    print("\t".join(vars_))
    for row in res:
        print("\t".join("" if v is None else str(v) for v in row))

if __name__ == "__main__":
    main()
