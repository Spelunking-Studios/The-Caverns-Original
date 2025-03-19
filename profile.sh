#!/bin/bash

ENABLE_PROFILES=True uv run main.py
uv run flameprof -o prof.log game.prof --format=log
inferno-flamegraph prof.log --deterministic > prof.svg
