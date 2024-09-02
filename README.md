# rest-sprinkler

A simple HTTP server that forwards HTTP GETs to Home Assistant to turn a switch
on/off. This is useful for integration with OpenSprinkler's "HTTP station
type".

This OpenSprinkler feature feels pretty jank to me:

- They have some distressingly custom url parsing code:
  <https://opensprinkler.com/forums/topic/special-station-http-get-link-problem/>.
- OpenSprinkler doesn't seem to care what the HTTP response code is, or even if
  it can talk to the server it's trying to talk to.
- The previous point makes it seem very possible to accidentally leave a
  station on for a very long time.

I wonder if [Sustainable Irrigation Platform](https://dan-in-ca.github.io/SIP/)
is better at this?

## Run the server

Create a "Long-lived access token" in your Home Assistant profile:

    HA_API_TOKEN=[that access token you just created] python -m rest_sprinkler.serve

## Install systemd service

Urg:

    systemd/install.sh [HA_API_TOKEN]

Where `[HA_API_TOKEN]` is a "Long-lived access token" created in your Home
Assistant profile.
