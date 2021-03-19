import argparse
import requests
import sys
import aprslib
import pyowm


def fetch_geoip_location():

    # Make request
    response = requests.get("https://ipinfo.io/json").json()

    # Parse location
    return response["loc"]


def main():
    # Handle program arguments
    ap = argparse.ArgumentParser(
        prog='aprs-bcn', description='Command-line tool for sending out APRS-IS beacons')
    ap.add_argument("-c", "--callsign", help="Callsign", required=True)
    ap.add_argument("--ssid", help="APRS SSID", default="-10")
    ap.add_argument("--symbol", help="APRS Symbol", default="0")
    ap.add_argument(
        "--latlong", help="Comma-seperated lat and long of the station (defaults to geoip)", default=None)
    ap.add_argument("--message", help="APRS message", default="APRS-BCN")
    ap.add_argument(
        "--wx-mode", help="Run in WX mode", action="store_true")
    ap.add_argument(
        "--dry-run", help="Run without actually sending the packet", action="store_true")
    args = ap.parse_args()

    # Determine station location
    location = args.latlong
    if not location:
        print("Using geoip-supplied location")
        location = fetch_geoip_location()
    else:
        print("Using user-supplied location")

    # Convert the location to a useful format
    lat_fmt = float(location.split(",")[0])
    long_fmt = float(location.split(",")[1])
    lat_ddm = aprslib.util.latitude_to_ddm(lat_fmt)
    long_ddm = aprslib.util.longitude_to_ddm(long_fmt)

    # Get the location weather
    wx_json = requests.get(
        f"http://wttr.in/{lat_fmt},{long_fmt}?format=j1").json()
    temperature_f = wx_json["current_condition"][0]["temp_F"].zfill(3)
    wind_direction = wx_json["current_condition"][0]["winddirDegree"].zfill(3)
    wind_speed = wx_json["current_condition"][0]["windspeedMiles"].zfill(3)
    humidity_percent = wx_json["weather"][0]["hourly"][0]["humidity"].zfill(3)
    pressure = wx_json["weather"][0]["hourly"][0]["pressure"] + "0"

    # Construct packet
    packet_header = f"{args.callsign.upper()}{args.ssid}>APRS:!"
    packet_position = f"{lat_ddm}/{long_ddm}"
    packet_wx_data = f"{wind_direction}/{wind_speed}t{temperature_f}h{humidity_percent}b{pressure}"
    wx_packet = f"{packet_header}{packet_position}_{packet_wx_data}{args.message}"
    info_packet = f"{packet_header}{packet_position}{args.symbol}{args.message}"

    if args.wx_mode:
        packet = wx_packet
    else:
        packet = info_packet

    # Send
    print(f"Sending packet: {packet}")
    if not args.dry_run:
        AIS = aprslib.IS(args.callsign, passwd=aprslib.passcode(
            args.callsign), port=14580)
        AIS.connect()
        AIS.sendall(packet)
    else:
        print("--dry-run mode enabled. Not actually sending packet")

    return 0


if __name__ == '__main__':
    sys.exit(main())
