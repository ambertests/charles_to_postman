#!/usr/local/bin/python
"""
charles_to_postman.py
by: Amber Race
python version: 3.7

Converts the *.chlsj output of Charlesproxy to the Postman json format.
    Charles Schema:
    [
        {
            "method": "POST",
            "protocolVersion": "HTTP/1.1",
            "scheme": "https",
            "host": "www.example.com",
            "port": null,
            "path": "/foo",
            "query": null,
            "request": {
                "sizes": {
                    "headers": 556,
                    "body": 67
                },
                "mimeType": "application/json",
                "charset": "UTF-8",
                "contentEncoding": null,
                "header": {
                    "firstLine": "POST /foo HTTP/1.1",
                    "headers": [
                        {
                            "name": "Connection",
                            "value": "keep-alive"
                        },
                        {
                            "name": "Content-Length",
                            "value": "67"
                        }
                    ]
                },
                "body": {
                    "text": "{\"key\":\"value\"}",
                    "charset": "UTF-8"
                }
            },
            "response": {
                "status": 200,
                "sizes": {
                    "headers": 0,
                    "body": 281
                },
                "mimeType": "application/json",
                "charset": "UTF-8",
                "contentEncoding": null,
                "header": {
                    "firstLine": "HTTP/1.1 200 OK",
                    "headers": [
                        {
                            "name": "content-type",
                            "value": "application/json; charset=UTF-8"
                        },
                        {
                            "name": "content-length",
                            "value": "281"
                        }
                    ]
                },
                "body": {
                    "text": "{\"the\":\"response\"}",
                    "charset": "UTF-8"
                }
            }
        }
    ]
    Postman Schema:
    {
        "info": {
                    "description": "Converted from <input_file>",
                    "schema": "https://schema.getpostman.com/json/collection/v2.0.0/collection.json"
                },
        "item":[
                    {
                        "name": "/foo",
                        "request": {
                            "url": "https://www.example.com/foo",
                            "method": "POST",
                            "header": [
                                {
                                    "key": "Connection",
                                    "value": "keep-alive"
                                },
                                {
                                    "key": "Content-Length",
                                    "value": "67"
                                }
                            ],
                            "body": {
                                "mode": "raw",
                                "raw": "{\"key\":\"value\"}"
                            }
                        },
                        "response": [
                            {
                                "name": "/foo",
                                "originalRequest": {
                                        "url": "https://www.example.com/foo",
                                        "method": "POST",
                                        "header": [
                                            {
                                                "key": "Connection",
                                                "value": "keep-alive"
                                            },
                                            {
                                                "key": "Content-Length",
                                                "value": "67"
                                            }
                                        ],
                                        "body": {
                                            "mode": "raw",
                                            "raw": "{\"key\":\"value\"}"
                                        },
                                "status": "OK",
                                "code": 200,
                                "_postman_previewlanguage": "json",
                                "_postman_previewtype": "parsed",
                                "header": [
                                        {
                                            "name": "content-type",
                                            "value": "application/json; charset=UTF-8"
                                        },
                                        {
                                            "name": "content-length",
                                            "value": "281"
                                        }
                                ],
                                "body": "{\"the\":\"response\"}"
                            }
                        ]
                    }
                ]
    }
"""
import json
import os
import argparse


def convert_charles_to_postman(charles_node):
    """Converts the request/response info from Charles into a Postman item"""
    postman_item = {}
    protocol = charles_node['protocolVersion']
    path = charles_node['path']
    method = charles_node['method']
    postman_item['name'] = path
    if 'port' in charles_node:
        url = '%s://%s:%s%s' % (charles_node['scheme'],
                                charles_node['host'], charles_node['port'], path)
    else:
        url = '%s://%s%s' % (charles_node['scheme'],
                             charles_node['host'], path)

    if charles_node['query']:
        url = "%s?%s" % (url, charles_node['query'])

    c_request = charles_node['request']
    p_request = {'url': url, 'method': method, 'header': [],
                 'body': {'mode': 'raw', 'raw': ''}, 'description': ''}
    for header in c_request['header']['headers']:
        p_request['header'].append(
            {'key': header['name'], 'value': header['value']})

    if c_request['sizes']['body'] > 0:
        if 'text' in c_request['body']:
            body = {'mode': 'raw', 'raw': c_request['body']['text']}
            p_request['body'] = body

    postman_item['request'] = p_request

    c_response = charles_node['response']
    postman_item['response'] = []
    status_code = c_response['status']
    p_response = {'name': path, 'originalRequest': p_request,
                  'code': status_code, 'header': [], 'cookie': []}
    try:
        p_status = c_response['header']['firstLine'].replace(
            '%s %d ' % (protocol, status_code), '')

        p_response['status'] = p_status
    except KeyError:
        pass
        
    for header in c_response['header']['headers']:
        p_response['header'].append(
            {'key': header['name'], 'value': header['value']})

    if c_response['sizes']['body'] > 0:
        if 'text' in c_response['body']:
            p_response['body'] = c_response['body']['text']
            if c_response['mimeType'] == 'application/json':
                p_response['_postman_previewlanguage'] = 'json'
                p_response['_postman_previewtype'] = 'parsed'

    postman_item['response'].append(p_response)

    return postman_item


def get_json_dict_from_input_file(input_file):
    """Extracts json string from input file and converts to a dict"""
    if not os.path.isfile(input_file):
        print("File does not exist: ", input_file)
        return

    input_string = open(input_file, "r").read()
    try:
        chls_json = json.loads(input_string)
    except ValueError as value_err:
        print("File does not contain valid json", value_err)
    return chls_json


if __name__ == '__main__':
    PARSER = argparse.ArgumentParser(
        description='Charlesproxy to Postman converter')
    PARSER.add_argument(
        '-i', '--input', help='Input file in the *.chlsj format', required=True)
    PARSER.add_argument('-o', '--output', help='Output file', required=True)
    PARSER.add_argument(
        '-n', '--name', help='Name of the target Postman collection', required=True)
    ARGS = PARSER.parse_args()

    CHARLES_JSON = get_json_dict_from_input_file(ARGS.input)
    if CHARLES_JSON:
        POSTMAN_JSON = {
            "info": {
                "name": ARGS.name,
                "description": "Converted from " + ARGS.input,
                "schema": "https://schema.getpostman.com/json/collection/v2.0.0/collection.json"
            },
            "item": []
        }

        for CHARLES_NODE in CHARLES_JSON:
            POSTMAN_JSON['item'].append(
                convert_charles_to_postman(CHARLES_NODE))

        OUTPUT_FILE = open(ARGS.output, 'w')
        OUTPUT_FILE.write(json.dumps(POSTMAN_JSON))
        OUTPUT_FILE.flush()
        OUTPUT_FILE.close()
