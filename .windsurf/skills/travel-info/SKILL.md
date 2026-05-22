# Travel Info Skill

## Usage
1. Pick file: country mentioned? use country file. Cross-border? EUROPE.md. No country? mode file.
2. Read file, find URL
3. Fetch URL. Failed? Try Brave Search. Still stuck? Perplexity.

## Files
EUROPE.md - cross-border (Eurostar, Thalys)
FLIGHTS.md - flight tracking, delays
TRAINS.md - train tracking, stations
TRANSIT.md - city transit, buses, metro
DE.md - Germany
FR.md - France
UK.md - United Kingdom
AT.md - Austria
CH.md - Switzerland
IT.md - Italy
BE.md - Belgium
NL.md - Netherlands
ES.md - Spain

## Examples
Frankfurt flight delays -> DE.md -> Flightradar24
Eurostar disruptions -> EUROPE.md -> Eurostar status
Paris to London train -> EUROPE.md -> Eurostar
Berlin metro -> DE.md -> BVG
Flight delays Europe -> FLIGHTS.md -> Flightradar24
Train delays Italy -> IT.md -> Trenitalia

## API Cost (try in order)
T0: web_fetch ($0) - always try first
T1: Brave Search ($0.005) - find working URL
T2: Perplexity ($0.01) - synthesized answer
T3: Anthropic ($0.03) - complex research, last resort
