#!/bin/bash

ENABLE_PROFILES=True uv run main.py
uv run flameprof -o profiles/prof.log game.prof --format=log
inferno-flamegraph profiles/prof.log --deterministic --fontsize 1 > profiles/prof.svg
