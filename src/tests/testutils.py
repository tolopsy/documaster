def is_4xx(status: int):
    return status // 100 == 4

def is_2xx(status: int):
    return status // 100 == 2