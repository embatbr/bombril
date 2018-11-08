#! coding: utf-8

"""Reads/writes objects from/to S3.
"""


import boto3


def get_s3_object(bucket_name, key):
    s3_resource = boto3.resource('s3')
    return s3_resource.Object(bucket_name, key)

def write_string(bucket_name, key, data):
    obj = get_s3_object(bucket_name, key)
    obj.put(Body=data)

def read_string(bucket_name, key):
    obj = get_s3_object(bucket_name, key)
    content = obj.get()['Body'].read()
    return content.decode('utf8')


# TODO create code similar to the ones above using airflow (using dependency injection)
