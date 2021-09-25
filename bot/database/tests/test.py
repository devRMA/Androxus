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
