# IdiotsGuide.md
## Dose Nudge (Home Assistant) – Manual install (Option B)

This is the install method for real humans.
It installs BOTH the integration and the big PNG icons for Lovelace.

If you miss the icons step, your dashboard will look broken.
So don't.

## What you’re installing (two folders)

1) Integration code (Home Assistant loads this)
- goes in: `/config/custom_components/dose_nudge/`

2) Lovelace PNG icons (Home Assistant serves these to the UI)
- goes in: `/config/www/dose_nudge/`

They are separate on purpose. Home Assistant enforces it.

## Step-by-step

### 1) Copy the integration folder

Put this repo folder:
- `custom_components/dose_nudge/`

into your HA config:
- `/config/custom_components/dose_nudge/`

You should end up with files like:
- `/config/custom_components/dose_nudge/manifest.json`
- `/config/custom_components/dose_nudge/sensor.py`

### 2) Copy the icons folder

Put this repo folder:
- `www/dose_nudge/`

into your HA config:
- `/config/www/dose_nudge/`

You should end up with files like:
- `/config/www/dose_nudge/icons/tablet/tablet_icon_128px.png`
- `/config/www/dose_nudge/icons/refill/refill_Icon_128px.png`

### 3) Restart Home Assistant

Settings → System → Restart

Do not skip this.

### 4) Add the integration

Settings → Devices & Services → Add Integration → “Dose Nudge”

## Quick test (icons)

Open this in a browser:

`http://YOUR_HA_IP:8123/local/dose_nudge/icons/tablet/tablet_icon_128px.png`

If it loads, icons are installed correctly.
If it 404s, you put `www/` in the wrong place.

## Lovelace usage

Use these URLs in Lovelace image-capable cards:

- `/local/dose_nudge/icons/tablet/tablet_icon_256px.png`
- `/local/dose_nudge/icons/refill/refill_Icon_256px.png`

If you want proper “buttons with big icons”, use `custom:button-card`.
(See README for examples.)
