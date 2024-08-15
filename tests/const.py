from importlib.resources import files

TEST_RESOURCE_PATH = files('tests._resources')

TEST_API_RESOURCE_PATH = TEST_RESOURCE_PATH.joinpath('api')
TEST_DB_RESOURCE_PATH = TEST_RESOURCE_PATH.joinpath('db')
