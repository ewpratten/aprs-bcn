# APRS Beacon
Command-line tool for sending out APRS-IS beacons

I use this script to broadcast my home `VA3ZZA` marker on the APRS network.

## How it works

The script generates a packet based on commandline arguments, and sends it to APRS-IS. Using the `--wx-mode` flag, this script will re-broadcast weather data as a WX station.

```text
usage: aprsbcn [-h] -c CALLSIGN [--ssid SSID] [--symbol SYMBOL] [--latlong LATLONG] [--message MESSAGE] [--wx-mode] [--dry-run]

Command-line tool for sending out APRS-IS beacons

optional arguments:
  -h, --help            show this help message and exit
  -c CALLSIGN, --callsign CALLSIGN
                        Callsign
  --ssid SSID           APRS SSID
  --symbol SYMBOL       APRS Symbol
  --latlong LATLONG     Comma-seperated lat and long of the station (defaults to geoip)
  --message MESSAGE     APRS message
  --wx-mode             Run in WX mode
  --dry-run             Run without actually sending the packet
```