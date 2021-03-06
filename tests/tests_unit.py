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

try:
    import __builtin__
except ImportError:
    import builtins as __builtin__


class TestOmegaGPIO(unittest.TestCase):
    def setUp(self):
        with mock.patch.object(__builtin__, 'open'):
            self.omega = OmegaGPIO()

    def tearDown(self):
        del self.omega

    @mock.patch.object(OmegaGPIO, 'pin_state')
    def test_set_pin(self, p_pin_state):
        mo = mock.mock_open()
        with mock.patch.object(__builtin__, 'open', mo, create=True):
            self.omega.set_pin(8, 1)

        p_pin_state.assert_called_once_with(8, 'w')
        mo.assert_called_once_with('/sys/class/gpio/gpio8/value', 'w')
        ctx = mo()
        ctx.write.assert_called_once_with("1")

    def test_set_pin_bad_pin(self):
        mo = mock.mock_open()
        with mock.patch.object(__builtin__, 'open', mo, create=True):
            with self.assertRaises(ValueError):
                self.omega.set_pin(None, 1)
        mo.assert_not_called()

    @mock.patch.object(OmegaGPIO, 'pin_state')
    def test_get_pin(self, p_pin_state):
        mo = mock.mock_open(read_data="1")
        with mock.patch.object(__builtin__, 'open', mo, create=True):
            pin = self.omega.get_pin(8)

        p_pin_state.assert_called_once_with(8, 'r')
        mo.assert_called_once_with('/sys/class/gpio/gpio8/value', 'r')
        ctx = mo()
        self.assertTrue(ctx.read.called)
        self.assertEqual(pin, 1)

    def test_get_pin_bad_pin(self):
        mo = mock.mock_open()
        with mock.patch.object(__builtin__, 'open', mo, create=True):
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
        with mock.patch.object(__builtin__, 'open', mo, create=True):
            with mock.patch.object(self.omega, '_export_pin'):
                with mock.patch.object(self.omega, '_unexport_pin'):
                    with self.omega.pin_state(8, 'r'):
                        pass
        mo.assert_has_calls([
            call('/sys/class/gpio/gpio8/direction', 'w'),
            call().__enter__(),
            call().write('in'),
            call().__exit__(None, None, None)
        ])

    def test_pin_state_read(self):
        mo = mock.mock_open()
        with mock.patch.object(__builtin__, 'open', mo, create=True):
            with mock.patch.object(self.omega, '_export_pin'):
                with mock.patch.object(self.omega, '_unexport_pin'):
                    with self.omega.pin_state(8, 'read'):
                        pass
        mo.assert_has_calls([
            call('/sys/class/gpio/gpio8/direction', 'w'),
            call().__enter__(),
            call().write('in'),
            call().__exit__(None, None, None)
        ])

    def test_pin_state_w(self):
        mo = mock.mock_open()
        with mock.patch.object(__builtin__, 'open', mo, create=True):
            with mock.patch.object(self.omega, '_export_pin'):
                with mock.patch.object(self.omega, '_unexport_pin'):
                    with self.omega.pin_state(8, 'w'):
                        pass
        mo.assert_has_calls([
            call('/sys/class/gpio/gpio8/direction', 'w'),
            call().__enter__(),
            call().write('out'),
            call().__exit__(None, None, None),
        ])

    def test_pin_state_write(self):
        mo = mock.mock_open()
        with mock.patch.object(__builtin__, 'open', mo, create=True):
            with mock.patch.object(self.omega, '_export_pin'):
                with mock.patch.object(self.omega, '_unexport_pin'):
                    with self.omega.pin_state(8, 'write'):
                        pass
        mo.assert_has_calls([
            call('/sys/class/gpio/gpio8/direction', 'w'),
            call().__enter__(),
            call().write('out'),
            call().__exit__(None, None, None)
        ])

    def test_pin_state_pin_invalid(self):
        mo = mock.mock_open()
        with mock.patch.object(__builtin__, 'open', mo, create=True):
            with self.assertRaises(ValueError) as cm:
                with self.omega.pin_state(None, None):
                    pass
        mo.assert_not_called()
        self.assertEqual("pin 'None' invalid", str(cm.exception))

    def test_pin_state_bad_state_not_str(self):
        mo = mock.mock_open()
        with mock.patch.object(__builtin__, 'open', mo, create=True):
            with self.assertRaises(TypeError) as cm:
                with self.omega.pin_state(8, None):
                    pass
        self.assertEqual('state must be string type', str(cm.exception))
        mo.assert_not_called()

    def test_pin_state_bad_state_invalid(self):
        mo = mock.mock_open()
        with mock.patch.object(__builtin__, 'open', mo, create=True):
            with self.assertRaises(ValueError) as cm:
                with self.omega.pin_state(8, 'foo'):
                    pass
        self.assertEqual("'foo' state invalid", str(cm.exception))
        mo.assert_not_called()

    def test__export_pin(self):
        mo = mock.mock_open()
        with mock.patch.object(__builtin__, 'open', mo, create=True):
            self.omega._export_pin(8)
        mo.assert_has_calls([
            call('/sys/class/gpio/gpiochip0/subsystem/export', 'w'),
            call().__enter__(),
            call().write('8'),
            call().__exit__(None, None, None)
        ])

    def test__unexport_pin(self):
        mo = mock.mock_open()
        with mock.patch.object(__builtin__, 'open', mo, create=True):
            self.omega._unexport_pin(8)
        mo.assert_has_calls([
            call('/sys/class/gpio/gpiochip0/subsystem/unexport', 'w'),
            call().__enter__(),
            call().write('8'),
            call().__exit__(None, None, None)
        ])



if __name__ == '__main__':
    unittest.main()
