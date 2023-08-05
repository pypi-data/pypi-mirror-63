from typing import Generator

from chunli.call import Call


global get_calls_block


def get_calls_block() -> Generator[Call, None, None]:
    yield Call(
        url='http://localhost:8001/hello',
        method='GET',
        headers=None,
        body=None,
    )
