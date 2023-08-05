import gzip
import os
from typing import Iterator
from unittest import SkipTest

import cbor2

from zuper_commons.fs import locate_files, read_bytes_from_file
from zuper_ipce import IPCE, ipce_from_object, object_from_ipce
from zuper_typing import dataclass


@dataclass
class Case:
    fn: str
    ipce: IPCE
    digest: str


def find_objects(load: bool = True) -> Iterator[Case]:  # pragma: no cover
    d = "test_objects"
    filenames = locate_files(d, "*.ipce.cbor.gz", normalize=False)

    def file_length(_: str) -> int:
        return os.stat(_).st_size

    filenames.sort(key=file_length)
    for f in filenames:
        if load:
            data = read_bytes_from_file(f)
            ipce = cbor2.loads(data)
        else:
            ipce = None
        digest, _, _ = os.path.basename(f).partition(".")
        n = file_length(f)
        digest += f"_len{n}"
        yield Case(f, ipce=ipce, digest=digest)


#
# def test_from_test_objects():
#     for case in find_objects():
#         print(case.fn)
#         ob = object_from_ipce(case.ipce, {})
#         ipce2 = ipce_from_object(ob)


def check_case(fn: str):
    from zuper_ipce import logger
    import traceback

    try:
        if not os.path.exists(fn):  # pragma: no cover
            raise SkipTest(f"File {fn} not found")
        # print("check_case " + fn)
        ipce_gz = read_bytes_from_file(fn)
        ipce_cbor = gzip.decompress(ipce_gz)
        ipce = cbor2.loads(ipce_cbor)
        # logger.info(f'ipce:\n\n{yaml.dump(ipce)}')
        ob = object_from_ipce(ipce)
        # logger.info(f'ob:\n\n{ob}')
        ipce2 = ipce_from_object(ob)
        # logger.info(f'ipce2:\n\n{yaml.dump(ipce2)}')
        # assert_equal_ipce("", ipce, ipce2)
        # assert ipce == ipce2
    except BaseException:  # pragma: no cover
        logger.error(traceback.format_exc())
        raise


def main():  # pragma: no cover
    print(
        """
from .test_from_testobjs import check_case
    """
    )
    for case in find_objects(load=False):
        s = f"""
def test_{case.digest}():
    fn = {case.fn!r}
    check_case(fn)
"""
        print(s)


if __name__ == "__main__":  # pragma: no cover
    main()
