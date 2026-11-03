# Map Glitch Lab

> **Project Eagle** | Map Exploration & Debug Tool

## Overview

Map Glitch Lab is a 3D map walker and boundary exploration tool for GTA San Andreas. It helps survey the game map, discover terrain glitches, boundary clipping issues, and LOD (Level of Detail) anomalies in Project Eagle's custom map areas.

## Features

- 🗺️ **3D Map Walker** — Navigate the GTA SA map programmatically
- 🐛 **Glitch Detection** — Identify boundary clipping, z-fighting, invisible walls
- 📍 **Coordinate Logging** — Record POI (Point of Interest) coordinates
- 📊 **Survey Reports** — Generate map area coverage reports
- 🏙️ **Custom Area Support** — Works with INLAND-03A and other custom districts

## Usage

```powershell
cd tools/map-glitch-lab

# Start interactive map walk
python eagle_map_glitch_lab.py --interactive

# Survey a specific area (coordinates in GTA SA units)
python eagle_map_glitch_lab.py --survey --x 2000 --y -1500 --radius 500

# Generate report
python eagle_map_glitch_lab.py --report --output survey_report.json
```

## File

```
map-glitch-lab/
└── eagle_map_glitch_lab.py   ← Single-file tool, all logic here
```

## Output

Survey results saved to `tools/map-glitch-lab/data/surveys/`.

## Jira

SCRUM-151 — [Map Glitch Lab](https://nguyennguyenle997.atlassian.net/browse/SCRUM-151)
