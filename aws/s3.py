#! coding: utf-8

"""Reads/writes objects from/to S3.
"""


import boto3
import json


# Generic code to deal with reading and writing of S3 objects

def get_s3_object(bucket_name, key):
    s3_resource = boto3.resource('s3')
    return s3_resource.Object(bucket_name, key)

def read_string(bucket_name, key):
    obj = get_s3_object(bucket_name, key)
    data = obj.get()['Body'].read()
    return data.decode('utf8')

def write_string(bucket_name, key, data):
    obj = get_s3_object(bucket_name, key)
    obj.put(Body=data)


def read_json_lines(bucket_name, key):
    data = read_string(bucket_name, key)
    lines = data.split('\n')
    return [json.loads(line) for line in lines]

def write_json_lines(bucket_name, key, data):
    lines = [json.dumps(obj, ensure_ascii=False) for obj in data]
    data = '\n'.join(lines)
    write_string(bucket_name, key, data)


# TODO create code similar to the ones above using airflow (using dependency injection)
