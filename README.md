# lux-geo-python
Unofficial Python API for Lux Geo thermostats

This is quick-and-dirty, and mostly written by Cursor + ChatGPT/Claude + Flow. :)

The motivation behind this was a Lux Geo thermostat (for an in-wall gravity propane millivolt heater) that
doesn't work with Home Assistant (yet).

Usage: define your own `.env` file based on `.env_sample` and run `python main.py`.

For development/testing, I find it useful to cache `TOKENS` in the `.env` file and not force auth every time.