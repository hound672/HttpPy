# Python
import json
from colorama import Fore
# Modules
from .generics import log_success, log_main


def __parse_body(response):
    content_type = response.headers.get('Content-Type')
    if response.text and content_type:
        if "application/json" in content_type:
            return json.dumps(json.loads(response.text), indent=4)
        else:
            return response.text
    return ""


def log_request(req, verbose: bool = False) -> None:
    log_data = []
    url = req.url
    method = req.method
    # log_data.append("=====> ")
    # log_data.append("Making {} request to: {} \n".format(method, url))

    if verbose:
        headers = req.headers
        body = req.body

        print('{0}{1}{2} {3}'.format(Fore.BLUE, method, Fore.GREEN, url))

        if headers is not None:
            for name, value in headers.items():
                __print_header(name, value)

        if body is not None:
            json_body = body.decode("utf-8")
            print(json.dumps(json.loads(json_body), indent=4))


def log_request_response(response, verbose=False):
    log_data = []

    if not verbose:
        log_data.append("<===== ")
        log_data.append("{}\n".format(response.status_code))
        log_success("".join(log_data))
    else:
        __print_request_part("{0}[{1}]{2} {3}".format(Fore.BLUE, response.status_code, Fore.GREEN, response.url), "response")
        for name, value in response.headers.items():
            __print_header(name, value)
        print(__parse_body(response))

def __print_header(name: str, value: str) -> None:
    print('{0}{1}{2}: {3}'.format(Fore.LIGHTGREEN_EX, name, Fore.WHITE, value))


def __print_request_part(data, part):
    __print_request_part_header(part)
    print(data)


def __print_request_part_header(part="extra"):
    log_success("-"*30, end="")
    log_success(" {} ".format(part.upper()), end="")
    log_success("-"*30, flush=True)
