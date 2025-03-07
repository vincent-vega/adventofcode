# shellcheck shell=bash

download_aoc_input() {
    if [ -z "$AOC_SESSION" ]; then
        echo 1>&2 "Missing AoC session"
        return 1
    fi
    if [[ $(pwd) =~ ([0-9]{4})/day_(0[1-9]|1[0-9]|2[0-5])$ ]]; then
        local year="${BASH_REMATCH[1]}"
        local day_padded="${BASH_REMATCH[2]}"
        local day=$((10#$day_padded))
        curl "https://adventofcode.com/${year}/day/${day}/input" \
            -H "Cookie: session=$AOC_SESSION" | tee input.txt
    fi
}
