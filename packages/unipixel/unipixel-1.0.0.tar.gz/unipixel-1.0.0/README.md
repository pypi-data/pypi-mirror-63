![tests](https://github.com/Razerfish/unipixel/workflows/tests/badge.svg?branch=master)
![Pylint](https://github.com/Razerfish/unipixel/workflows/Pylint/badge.svg?branch=master)
# Unipixel - Simulate neopixels in a terminal

`unipixel` is a package designed to be used interchangeably with the [`adafruit-circuitpython-neopixel`](https://github.com/adafruit/Adafruit_CircuitPython_NeoPixel) package for the purposes of testing and development on systems where, for whatever reason, actual neopixels aren't available.

## Note about compatibility

`unipixel` works by wrapping the &#9608; (`0x2588`) unicode character in ANSI color escape sequences. This method requires a terminal that supports both unicode and "true color" for `unipixel` to render properly.

A list of terminals that support true color can be found [here.](https://gist.github.com/XVilka/8346728)
