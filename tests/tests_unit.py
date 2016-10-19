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

import unittest

import mock
from mock import call

from omega_gpio import OmegaGPIO


class TestOmegaGPIO(unittest.TestCase):
    def setUp(self):
        with mock.patch('__builtin__.open'):
            self.omega = OmegaGPIO()

    def tearDown(self):
        del self.omega

    def test_init(self):
        mo = mock.mock_open()
        with mock.patch('__builtin__.open', new=mo) as _mock:
            OmegaGPIO()
        mo.assert_called_with('/sys/class/gpio/gpiochip0/subsystem/export', 'w')
        self.assertEqual(mo.mock_calls, [
            call('/sys/class/gpio/gpiochip0/subsystem/export', 'w'),
            call().__enter__(),
            call().write('0'),
            call().__exit__(None, None, None),
            call('/sys/class/gpio/gpiochip0/subsystem/export', 'w'),
            call().__enter__(),
            call().write('1'),
            call().__exit__(None, None, None),
            call('/sys/class/gpio/gpiochip0/subsystem/export', 'w'),
            call().__enter__(),
            call().write('6'),
            call().__exit__(None, None, None),
            call('/sys/class/gpio/gpiochip0/subsystem/export', 'w'),
            call().__enter__(),
            call().write('7'),
            call().__exit__(None, None, None),
            call('/sys/class/gpio/gpiochip0/subsystem/export', 'w'),
            call().__enter__(),
            call().write('8'),
            call().__exit__(None, None, None),
            call('/sys/class/gpio/gpiochip0/subsystem/export', 'w'),
            call().__enter__(),
            call().write('12'),
            call().__exit__(None, None, None),
            call('/sys/class/gpio/gpiochip0/subsystem/export', 'w'),
            call().__enter__(),
            call().write('13'),
            call().__exit__(None, None, None),
            call('/sys/class/gpio/gpiochip0/subsystem/export', 'w'),
            call().__enter__(),
            call().write('14'),
            call().__exit__(None, None, None),
            call('/sys/class/gpio/gpiochip0/subsystem/export', 'w'),
            call().__enter__(),
            call().write('18'),
            call().__exit__(None, None, None),
            call('/sys/class/gpio/gpiochip0/subsystem/export', 'w'),
            call().__enter__(),
            call().write('19'),
            call().__exit__(None, None, None),
            call('/sys/class/gpio/gpiochip0/subsystem/export', 'w'),
            call().__enter__(),
            call().write('20'),
            call().__exit__(None, None, None),
            call('/sys/class/gpio/gpiochip0/subsystem/export', 'w'),
            call().__enter__(),
            call().write('21'),
            call().__exit__(None, None, None),
            call('/sys/class/gpio/gpiochip0/subsystem/export', 'w'),
            call().__enter__(),
            call().write('23'),
            call().__exit__(None, None, None),
            call('/sys/class/gpio/gpiochip0/subsystem/export', 'w'),
            call().__enter__(),
            call().write('26'),
            call().__exit__(None, None, None),
        ])

    @mock.patch.object(OmegaGPIO, 'pin_state')
    def test_set_pin(self, p_pin_state):
        mo = mock.mock_open()
        with mock.patch('__builtin__.open', mo, create=True):
            self.omega.set_pin(8, 1)

        p_pin_state.assert_called_once_with(8, 'w')
        mo.assert_called_once_with('/sys/class/gpio/gpio8/value', 'w')
        ctx = mo()
        ctx.write.assert_called_once_with("1")

    def test_set_pin_bad_pin(self):
        mo = mock.mock_open()
        with mock.patch('__builtin__.open', mo, create=True):
            with self.assertRaises(ValueError):
                self.omega.set_pin(None, 1)
        mo.assert_not_called()

    @mock.patch.object(OmegaGPIO, 'pin_state')
    def test_get_pin(self, p_pin_state):
        mo = mock.mock_open(read_data="1")
        with mock.patch('__builtin__.open', mo, create=True):
            pin = self.omega.get_pin(8)

        p_pin_state.assert_called_once_with(8, 'r')
        mo.assert_called_once_with('/sys/class/gpio/gpio8/value', 'r')
        ctx = mo()
        self.assertTrue(ctx.read.called)
        self.assertEqual(pin, 1)

    def test_get_pin_bad_pin(self):
        mo = mock.mock_open()
        with mock.patch('__builtin__.open', mo, create=True):
            with self.assertRaises(ValueError):
                self.omega.get_pin(None)
        mo.assert_not_called()

    @mock.patch.object(OmegaGPIO, 'set_pin')
    def test_pin_on(self, p_set_pin):
        self.omega.pin_on(8)
        p_set_pin.assert_called_once_with(8, 1)

    @mock.patch.object(OmegaGPIO, 'set_pin')
    def test_pin_off(self, p_set_pin):
        self.omega.pin_off(8)
        p_set_pin.assert_called_once_with(8, 0)

    def test_pin_state_r(self):
        mo = mock.mock_open()
        with mock.patch('__builtin__.open', mo, create=True):
            with self.omega.pin_state(8, 'r'):
                pass
        mo.assert_called_once_with('/sys/class/gpio/gpio8/direction', 'w')
        ctx = mo()
        ctx.write.assert_called_once_with('in')

    def test_pin_state_read(self):
        mo = mock.mock_open()
        with mock.patch('__builtin__.open', mo, create=True):
            with self.omega.pin_state(8, 'read'):
                pass
        mo.assert_called_once_with('/sys/class/gpio/gpio8/direction', 'w')
        ctx = mo()
        ctx.write.assert_called_once_with('in')

    def test_pin_state_w(self):
        mo = mock.mock_open()
        with mock.patch('__builtin__.open', mo, create=True):
            with self.omega.pin_state(8, 'w'):
                pass
        mo.assert_called_once_with('/sys/class/gpio/gpio8/direction', 'w')
        ctx = mo()
        ctx.write.assert_called_once_with('out')

    def test_pin_state_pin_invalid(self):
        mo = mock.mock_open()
        with mock.patch('__builtin__.open', mo, create=True):
            with self.assertRaises(ValueError) as cm:
                with self.omega.pin_state(None, None):
                    pass
        mo.assert_not_called()
        self.assertEqual("pin 'None' invalid", cm.exception.message)

    def test_pin_state_bad_state_not_str(self):
        mo = mock.mock_open()
        with mock.patch('__builtin__.open', mo, create=True):
            with self.assertRaises(TypeError) as cm:
                with self.omega.pin_state(8, None):
                    pass
        self.assertEqual('state must be string type', cm.exception.message)
        mo.assert_not_called()

    def test_pin_state_bad_state_invalid(self):
        mo = mock.mock_open()
        with mock.patch('__builtin__.open', mo, create=True):
            with self.assertRaises(ValueError) as cm:
                with self.omega.pin_state(8, 'foo'):
                    pass
        self.assertEqual("'foo' state invalid", cm.exception.message)
        mo.assert_not_called()


if __name__ == '__main__':
    unittest.main()
