from py_aws_core.router import APIGatewayRouter


__router = APIGatewayRouter()


def get_router():
    return __router
