#!/usr/bin/env python
# encoding: utf-8

from mssapi.s3.connection import S3Connection
from mssapi.exception import MssapiServerError

def mss_test_get_bucket(conn, name):
    b0 = None
    try:
        b0 = conn.get_bucket(name)
    except MssapiServerError as e:
        if e.error_code == 'NoSuchBucket':
            b0 = conn.create_bucket(name)
        else:
            raise e
    return b0

def assert_meta_result(meta, exp_meta):
    for k in meta:
        if k not in exp_meta:
            return False
        elif meta[k] != exp_meta[k]:
            return False
    for k in exp_meta:
        if k not in meta:
            return False
    return True

def test_add(b0, key_name):
    print '==== test add meta ===='
    key = b0.new_key(key_name)
    key.set_contents_from_string("Hello, world!")
    key = b0.get_key(key_name)
    meta = key._get_remote_metadata()
    #print 'Before: ', meta
    key.set_remote_metadata(metadata_minus={}, metadata_plus={'content-type': 'plain/xml', 'x-amz-meta-location': 'Beijing'})
    key = b0.get_key(key_name)
    meta = key._get_remote_metadata()
    exp_meta = {
            'x-amz-meta-location': 'Beijing',
            'content-type': 'plain/xml'
    }
    assert assert_meta_result(meta, exp_meta)
    #print 'After: ', meta
    key.delete()

def test_del(b0, key_name):
    print '==== test del meta ===='
    key = b0.new_key(key_name)
    key.set_metadata('location', 'Beijing')
    key.set_metadata('content-type', 'plain/text')
    key.set_contents_from_string("Hello, world!")
    key = b0.get_key(key_name)
    meta = key._get_remote_metadata()
    #print 'Before: ', meta
    key.set_remote_metadata(metadata_minus={'x-amz-meta-location': 'Beijing'}, metadata_plus={})
    key = b0.get_key(key_name)
    meta = key._get_remote_metadata()
    exp_meta = {
            'content-type': 'plain/text'
    }
    #print 'After: ', meta
    assert assert_meta_result(meta, exp_meta)
    key.delete()

def test_xor(b0, key_name):
    print '==== test add and del meta ===='
    key = b0.new_key(key_name)
    key.set_metadata('location', 'Beijing')
    key.set_metadata('content-type', 'plain/text')
    key.set_contents_from_string("Hello, world!")
    key = b0.get_key(key_name)
    meta = key._get_remote_metadata()
    #print 'Before: ', meta
    key.set_remote_metadata(metadata_minus={'x-amz-meta-location': 'Beijing'}, metadata_plus={'content-type': 'plain/xml'})
    key = b0.get_key(key_name)
    meta = key._get_remote_metadata()
    #print 'After: ', meta
    exp_meta = {
            'content-type': 'plain/xml'
    }
    assert assert_meta_result(meta, exp_meta)
    key.delete()

def test_metadata(host, access_key, secret_key):
    conn = S3Connection(aws_access_key_id=access_key, aws_secret_access_key=secret_key, host=host, is_secure=True)
    b0 = mss_test_get_bucket(conn, 'example')
    key_name = 'test_copy_meta'
    test_xor(b0, key_name)
    test_add(b0, key_name)
    test_del(b0, key_name)

if  __name__ == '__main__':
    import os
    mss_host = os.getenv('MSS_HOST', None)
    mss_access_key = os.getenv('MSS_ACCESS_KEY', None)
    mss_secret_key = os.getenv('MSS_SECRET_KEY', None)
    print mss_host, mss_access_key, mss_secret_key
    if mss_host is None or mss_access_key is None or mss_secret_key is None:
        print 'Usage: env MSS_HOST=XXX MSS_ACCESS_KEY=YYY MSS_SECRET_KEY=ZZZ python ./test_metadata.py'
    else:
        test_metadata(mss_host, mss_access_key, mss_secret_key)

