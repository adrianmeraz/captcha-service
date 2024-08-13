from importlib.resources import files

TEST_RESOURCE_PATH = files('py_aws_core.spoofing._tests.twocaptcha._resources')

TEST_API_RESOURCE_PATH = TEST_RESOURCE_PATH.joinpath('api')
