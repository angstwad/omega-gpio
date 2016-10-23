# omega-gpio

[![Build Status](https://travis-ci.org/angstwad/omega-gpio.svg?branch=master)](https://travis-ci.org/angstwad/omega-gpio)

Extremely simple GPIO for the Onion Omega IoT device

## Install

### pip

It's uploaded to PyPI.

```
pip install omega_gpio
```

## Use
```
from omega_gpio import OmegaGPIO

omega = OmegaGPIO()

omega.pin_on(5)
omega.pin_off(5)
```

## Issues

Looks like the sysfs GPIO driver doesn't properly expose pin 8.  There's an apparent issue in sysfs not providing a place to set the pin direction.  I don't try to solve for that case here.
