from thompcoutils.string_utils import list_to_string


class FailedTestException(Exception):
    pass


def test(method, params, expected_value=None, expected_exception=None):
    method_name = str(method).split(" ")[1]
    print("starting {}({})...".format(method_name, list_to_string(params)), end="")
    if expected_exception is None:
        if expected_value is None:
            method(*params)
        elif method(*params) == expected_value:
            print("passed")
        else:
            str1 = "FAILED EXPECTED VALUE {}({})".format(method_name, list_to_string(params))
            raise FailedTestException(str1)
    else:
        try:
            if method(*params) == expected_value:
                str1 = "FAILED EXCEPTION {}({})".format(method_name, list_to_string(params))
                raise FailedTestException(str1)
        except expected_exception:
            print("passed")
