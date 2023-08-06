#!/usr/bin/env python
# encoding: utf-8

import test_util


conn = test_util.get_conn()

if __name__ == '__main__':
    import sys
    assert len(sys.argv) > 1
    for i in xrange(1, len(sys.argv)):
        test_util.clean_bucket(conn, sys.argv[i])
