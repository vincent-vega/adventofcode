#!/usr/bin/env python3

from datetime import datetime, timedelta, UTC
import os
import requests


def fetch_leaderboard_data(leaderboard_id):
    url = f"https://adventofcode.com/2024/leaderboard/private/view/{leaderboard_id}.json"
    response = requests.get(url, cookies={"session": os.getenv("AOC_SESSION", "")})
    if response.status_code == 200:
        return response.json()
    else:
        print(f"An error occurred while fetching data for leaderboard with ID {leaderboard_id}: {response.status_code}")
        return None


if __name__ == '__main__':
    seen = set()
    for leaderboard_id in os.getenv("AOC_LEADERBOARD", "").split(","):
        if data := fetch_leaderboard_data(leaderboard_id):
            for member_id, member_data in filter(lambda n: n[0] not in seen, data["members"].items()):
                seen.add(member_id)
                print(f"\nPlayer: {member_data['name']} (ID: {member_id})")
                sorted_days = sorted(member_data["completion_day_level"].items(), key=lambda x: int(x[0]))

                for day, levels in sorted_days:
                    print(f"  Day {day}:")

                    part1 = levels.get("1")
                    if part1:
                        ts1 = part1.get("get_star_ts")
                        if ts1:
                            readable_time1 = datetime.fromtimestamp(ts1, UTC)
                            print(f"    Part 1: {readable_time1}")

                    part2 = levels.get("2")
                    if part2:
                        ts2 = part2.get("get_star_ts")
                        if ts2:
                            readable_time2 = datetime.fromtimestamp(ts2, UTC)
                            if part1 and ts1:
                                delta_seconds = ts2 - ts1
                                delta = str(timedelta(seconds=delta_seconds))
                                print(f"    Part 2: {readable_time2} (Delta: {delta})")
                            else:
                                print(f"    Part 2: {readable_time2}")
        else:
            print(f"Missing data for leaderbord with ID {leaderboard_id}")
