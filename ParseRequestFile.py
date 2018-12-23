# Python
import json


def __is_request_defined(line):
    return ("## " in line)


def __normalize_request(line):
    type_url = line.split(" ")
    return {
        "type": type_url[0].lower(),
        "url": type_url[1].lower().replace("\n", "")
    }


def parse(file_path):
    file = open(file_path)

    should_parse_request = False
    should_end_request = False
    should_append_data = False
    current_request = {}
    requests = []
    data = []

    for line in file.readlines():
        if not should_parse_request:
            should_parse_request = __is_request_defined(line)
        else:
            if not len(current_request):
                current_request = __normalize_request(line)

            type = current_request["type"]
            if type == "get" or type == "delete":
                should_end_request = True
            else:
                if "{" in line:
                    should_append_data = True
                if should_append_data:
                    data.append(line)
                    if "}" in line:
                        should_append_data = False
                        body = json.loads("".join(data))
                        data = []
                        current_request["body"] = body
                        should_end_request = True

        if should_end_request:
            requests.append(current_request)
            current_request = {}
            should_parse_request = False
            should_end_request = False

    print(requests)
    return requests
