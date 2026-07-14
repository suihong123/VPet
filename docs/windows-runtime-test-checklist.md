# Windows Runtime Test Checklist

This checklist is for internal technical validation of the standalone cat desktop pet MVP. It is not a release checklist and does not approve commercial distribution.

## Test Environment

- Windows version:
- Architecture: x64
- .NET 8 Desktop Runtime version:
- Steam installed: yes / no
- Steam running: yes / no
- Network enabled: yes / no
- Test package artifact/run:

## Clean First Launch

- Use a clean Windows user profile or clear prior app configuration.
- App starts successfully.
- Default pet displayed is cat.
- App does not load vup as the default pet.
- No Steam error dialog appears.
- No Workshop prompt appears.
- No multiplayer prompt appears.
- No network or telemetry prompt appears.
- No crash on first launch.

## Window Behavior

- Transparent background renders correctly.
- Window is borderless.
- Window stays on top as expected.
- Mouse drag works.
- Single click feedback works.
- Double click behavior is acceptable.
- Close behavior works.
- Tray behavior works, if present.

## Cat Behavior

- Default idle animation appears.
- Boring animation appears or safely falls back.
- Squat animation appears or safely falls back.
- Left movement works.
- Right movement works.
- Sleep animation appears or safely falls back.
- Touch Head feedback works.
- Touch Body feedback works.
- Raised state works or safely falls back.
- Missing nonessential actions do not crash the app.

## Local Features

- Local MOD scan completes.
- Initial save/config is created.
- Restart reads the saved config.
- Steam is not initialized.
- Workshop is not loaded.
- Multiplayer entry is not shown or cannot be triggered.
- Error report upload is not attempted.
- Telemetry upload is not attempted.
- No active external API request is made during idle startup.

## Performance

- Startup time:
- Memory after startup:
- CPU after startup:
- Memory after 10 minutes idle:
- CPU after 10 minutes idle:
- App remains stable for 10 minutes idle.

## Result Record

- Overall result: pass / fail
- Issue summary:
- Reproduction steps:
- Screenshots attached: yes / no
- Local log path:
- Windows Event Viewer details:
- Notes:
