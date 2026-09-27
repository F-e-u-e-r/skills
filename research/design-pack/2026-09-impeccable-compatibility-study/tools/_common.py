"""Shared path/argument handling for the public reproduction tools.

Public inputs (documented in ../METHODOLOGY.md):
  --corpus     the Design Pack canonical corpus (default: <repo>/corpus/design-pack/public_records.json);
               its sha256 must equal the sealed corpus the study used, or the tool stops.
  --fixtures   the study's fixtures directory (default: ../fixtures).
  --workspace  a scratch directory for generated outputs (default: ./workspace); never the fixtures dir.
"""
import argparse, hashlib, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
STUDY = os.path.dirname(HERE)
REPO = os.path.abspath(os.path.join(STUDY, "..", "..", ".."))
DEFAULT_CORPUS = os.path.join(REPO, "corpus", "design-pack", "public_records.json")
DEFAULT_FIXTURES = os.path.join(STUDY, "fixtures")
CORPUS_SHA256 = "16ad01fb97f0ad321f254cce93e249e6484110862650dda39e45700be2893e5b"
DP_SEAL = "bd8cb1a"


def parser(description, need_fixtures=True, need_workspace=True):
    ap = argparse.ArgumentParser(description=description)
    ap.add_argument("--corpus", default=DEFAULT_CORPUS, help="Design Pack canonical corpus JSON")
    if need_fixtures:
        ap.add_argument("--fixtures", default=DEFAULT_FIXTURES, help="study fixtures directory")
    if need_workspace:
        ap.add_argument("--workspace", default=os.path.join(os.getcwd(), "workspace"), help="scratch output directory")
    return ap


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def load_corpus(path):
    data = open(path, "rb").read()
    h = hashlib.sha256(data).hexdigest()
    if h != CORPUS_SHA256:
        sys.exit(f"corpus sha256 {h[:16]}... != sealed corpus {CORPUS_SHA256[:16]}... (the study is pinned to seal {DP_SEAL})")
    return {r["id"]: r for r in json.loads(data)}


def ensure_dir(p):
    os.makedirs(p, exist_ok=True)
    return p
