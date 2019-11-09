## Information:
Adds a sensor with a stream source of a available NHL game by team. Can be used in scripts as a media source to play on TV's. If no stream or game available a "sorry" video will be the default sensor state

## Installation:
Install via HACS by adding repo source: https://github.com/spitfire1337/caststreams/ as integration

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
## Example Script:
```
watch_game:
  alias: Watch Rangers game
  sequence:
  - service: media_player.play_media
    data_template:
      entity_id: media_player.big_screen
      media_content_id: "{{ states('sensor.nhl_game_stream') }}"
      media_content_type: video
```      
