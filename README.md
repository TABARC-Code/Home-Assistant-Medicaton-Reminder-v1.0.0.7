# Dose Nudge for Home Assistant

Local medication reminders.
No cloud. No guesses. No magic.

Author: TABARC-Code  
Plugin URI: https://github.com/TABARC-Code/

If you’re setting this up for someone with partial sight, use the big PNG icons shipped in `www/`.

## What it does

- Sensor: next due time
- Binary sensor: dose due
- Sensor: doses remaining (optional)
- Services: mark taken, refill

## What it won't do

- It won't call out to the internet
- It won't invent schedules
- It won't spam notifications on its own

## Maintainer notes

- Restarts happen. State is persisted so reminders don't resurrect.
- Keep time maths in one place. Don't scatter it.
- Services should be idempotent. Users double tap and automations loop.

## Icons

Repo includes PNG icon sets under `icons/` for UI/README use, plus integration SVG under `custom_components/dose_nudge/icons/`.

## Lovelace: using the PNG icons (partial sight friendly)

Home Assistant will only load images from `/config/www/` (that’s `/local/` in URLs).

You have two ways to make the PNGs available:

### Option A: Manual path (recommended, stable URLs)

Copy `www/dose_nudge/` → `/config/www/dose_nudge/`

Use:

- `/local/dose_nudge/icons/tablet/tablet_icon_256px.png`
- `/local/dose_nudge/icons/refill/refill_Icon_256px.png`

### Option B: HACS community path (works, but the folder name depends on the repo)

HACS places extra web assets under `/config/www/community/<repo>/...`

Use:

- `/local/community/<repo>/www/dose_nudge/icons/tablet/tablet_icon_256px.png`
- `/local/community/<repo>/www/dose_nudge/icons/refill/refill_Icon_256px.png`

Yes, the `<repo>` part is annoying. That’s Home Assistant/HACS.
Pick Option A if you want this to be idiot-proof.

### Example: big “Take medication” button (button-card)

```yaml
type: custom:button-card
name: Take medication
entity: binary_sensor.dose_nudge_dose_due
show_state: true
show_icon: false
tap_action:
  action: call-service
  service: dose_nudge.mark_taken
  service_data:
    medication_id: morning_med
custom_fields:
  img: >
    [[[
      return `<img src="/local/dose_nudge/icons/tablet/tablet_icon_128px.png"
                   style="width:96px;height:96px;" />`;
    ]]]
styles:
  card:
    - height: 140px
    - padding: 16px
  name:
    - font-size: 24px
  state:
    - font-size: 20px
```

If you want built-in cards only, use `picture-entity` instead.


## Installation

### HACS (recommended)

1. Add this repository as a **custom repository** in HACS (type: Integration).
2. Install it from HACS.
3. Restart Home Assistant.
4. Add the integration via **Settings → Devices & Services → Add Integration → Dose Nudge**.

Icons for Lovelace are shipped in the repo `www/` folder.

HACS usually places extra web assets under:

- `/config/www/community/<repo>/...` on disk
- `/local/community/<repo>/...` in Lovelace URLs

The annoying bit is `<repo>` depends on the repository folder name in HACS.
If you want stable URLs, use the manual path below.

### Manual (no HACS)

Copy both of these into your Home Assistant config folder:

- `custom_components/dose_nudge/` → `/config/custom_components/dose_nudge/`
- `www/dose_nudge/` → `/config/www/dose_nudge/`

Restart Home Assistant.

This gives you stable icon URLs:

- `/local/dose_nudge/icons/tablet/tablet_icon_128px.png`
- `/local/dose_nudge/icons/refill/refill_Icon_128px.png`
