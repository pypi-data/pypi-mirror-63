import requests
from graphql.execution import ExecutionResult
from graphql.language.printer import print_ast
from gql.transport.http import HTTPTransport
from .extract_files import extract_files
import json
import os.path
from typing import Any


class GqlClientTransport(HTTPTransport):
    def __init__(self, url, timeout=None, **kwargs):
        super(GqlClientTransport, self).__init__(url, **kwargs)
        self.default_timeout = timeout

    def execute(self, document, variables=None, timeout=None):
        query_str = print_ast(document)
        payload = {"query": query_str, "variables": variables or {}}

        extracted_payload, files = extract_files(payload)

        if len(files):
            formData = dict()

            formData["operations"] = (None, json.dumps(extracted_payload))

            pathMap = {}
            i = 1
            for paths in files.values():
                pathMap[i] = paths
                i += 1
            formData["map"] = (None, json.dumps(pathMap))

            i = 1
            for file, paths in files.items():
                _file: Any = file
                formData[str(i)] = (os.path.basename(_file.name), file)
                i += 1

            post_args = {
                "headers": self.headers,
                "timeout": timeout or self.default_timeout,
                "files": formData,
            }
            request = requests.post(self.url, **post_args)
            request.raise_for_status()

            result = request.json()
            assert (
                "errors" in result or "data" in result
            ), 'Received non-compatible response "{}"'.format(result)
            return ExecutionResult(errors=result.get("errors"), data=result.get("data"))

        post_args = {
            "headers": self.headers,
            "timeout": timeout or self.default_timeout,
            "json": payload,
        }
        request = requests.post(self.url, **post_args)
        request.raise_for_status()

        result = request.json()
        assert (
            "errors" in result or "data" in result
        ), 'Received non-compatible response "{}"'.format(result)
        return ExecutionResult(errors=result.get("errors"), data=result.get("data"))
