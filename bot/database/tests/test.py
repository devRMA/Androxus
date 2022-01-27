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


class Test:
    """
    Class to make tests
    """
    @staticmethod
    def assert_equal(a, b):
        assert a == b

    @staticmethod
    def assert_not_equal(a, b):
        assert a != b

    @staticmethod
    def assert_true(x):
        assert x is True

    @staticmethod
    def assert_false(x):
        assert x is False

    @staticmethod
    def assert_is(a, b):
        assert a is b

    @staticmethod
    def assert_is_not(a, b):
        assert a is not b

    @staticmethod
    def assert_is_none(x):
        assert x is None

    @staticmethod
    def assert_is_not_none(x):
        assert x is not None

    @staticmethod
    def assert_in(a, b):
        assert a in b

    @staticmethod
    def assert_not_in(a, b):
        assert a not in b

    @staticmethod
    def assert_is_instance(a, b):
        assert isinstance(a, b)

    @staticmethod
    def assert_not_is_instance(a, b):
        assert not isinstance(a, b)
