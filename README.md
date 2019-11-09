## Information:
Adds a sensor with a stream source of a available NHL game by team. Can be used in scripts as a media source to play on TV's

## Installation:
Install via HACS by adding repo source: https://github.com/spitfire1337/caststreams/

## Usage:
Add to configuration.yaml:

```
sensor:
  - platform: caststreams
    email: [caststreams.com login]
    password: [caststreams.com login]
    team: [short code team name, IE: NYR, BOS, TBL]
    usertype: [(Optional) Free or donor. Default: free]
    region: [(Optional) EU defaults: us EU only available to donor]
```
