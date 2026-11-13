"""Shared duck. The ffmpeg mix lives in lib.mix; this module is the music-skill entry."""

from lib.mix import duck_under_voice, sidechain_gain

# Older imports.
sidechain = sidechain_gain
ffmpeg_duck = duck_under_voice
