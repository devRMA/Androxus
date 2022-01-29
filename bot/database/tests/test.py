# MIT License

# Copyright(c) 2021 Rafael

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files(the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and / or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from typing import Any


class Test:
    """
    Class to make tests
    """
    @staticmethod
    def assert_equal(value: Any, other: Any):
        assert value == other

    @staticmethod
    def assert_not_equal(value: Any, other: Any):
        assert value != other

    @staticmethod
    def assert_true(value: Any):
        assert value is True

    @staticmethod
    def assert_false(value: Any):
        assert value is False

    @staticmethod
    def assert_is(value: Any, other: Any):
        assert value is other

    @staticmethod
    def assert_is_not(value: Any, other: Any):
        assert value is not other

    @staticmethod
    def assert_is_none(value: Any):
        assert value is None

    @staticmethod
    def assert_is_not_none(value: Any):
        assert value is not None

    @staticmethod
    def assert_in(value: Any, other: Any):
        assert value in other

    @staticmethod
    def assert_not_in(value: Any, other: Any):
        assert value not in other

    @staticmethod
    def assert_is_instance(value: Any, other: Any):
        assert isinstance(value, other)

    @staticmethod
    def assert_not_is_instance(value: Any, other: Any):
        assert not isinstance(value, other)
