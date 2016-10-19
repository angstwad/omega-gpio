# -*- coding: utf-8 -*-

# Copyright 2016 Paul Durivage <pauldurivage@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import contextlib


class OmegaGPIO(object):
    export_path = "/sys/class/gpio/gpiochip0/subsystem/export"
    pin_dir_path = "/sys/class/gpio/gpio{}/direction"
    pin_val_path = "/sys/class/gpio/gpio{}/value"
    pins = (0, 1, 6, 7, 8, 12, 13, 14, 18, 19, 20, 21, 23, 26)

    def __init__(self):
        for pin in self.pins:
            with open(self.export_path, 'w') as f:
                f.write(str(pin))

    def _validate_pin(self, pin):
        try:
            assert pin in self.pins, "pin '%s' invalid" % pin
        except AssertionError as e:
            raise ValueError(str(e))

    @contextlib.contextmanager
    def pin_state(self, pin, state):
        self._validate_pin(pin)
        try:
            state = state.lower()
            assert state in ('r', 'read', 'w', 'write'), \
                "'%s' state invalid" % state
        except AttributeError:
            raise TypeError('state must be string type')
        except AssertionError as e:
            raise ValueError(str(e))

        if state.lower() in ('read', 'r'):
            with open(self.pin_dir_path.format(pin), 'w') as f:
                f.write("in")
        elif state.lower() in ('write', 'w'):
            with open(self.pin_dir_path.format(pin), 'w') as f:
                f.write("out")
        yield

    def pin_on(self, pin):
        self.set_pin(pin, 1)

    def pin_off(self, pin):
        self.set_pin(pin, 0)

    def set_pin(self, pin, value):
        self._validate_pin(pin)
        with self.pin_state(pin, 'w'):
            with open(self.pin_val_path.format(pin), 'w') as f:
                f.write(str(value))

    def get_pin(self, pin):
        self._validate_pin(pin)
        with self.pin_state(pin, 'r'):
            with open(self.pin_val_path.format(pin), 'r') as f:
                return int(f.read())
