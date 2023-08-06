import re
import math
import time
from django.conf import settings
from log_labeler import LOG_LABEL_OBFUSCATE

class Utils:
    @classmethod
    def array_difference(cls, array1, array2):
        return list(set(array1) - set(array2))

    @classmethod
    def array_intersection(cls, array1, array2):
        return list(set(array1) & set(array2))

    @classmethod
    def remove_new_lines(cls, data):
        return data.replace("\n", "").replace("\r", "")

    @classmethod
    def get_nim_headers(cls, request):
        NIM_HEADER_REG_EXP = r"^HTTP\_NIM\_"
        HTTP_REG_EXP = r"^HTTP\_"
        nim_headers = dict()
        for key, value in request.META.items():
            if re.match(NIM_HEADER_REG_EXP, key):
                transformed_key = re.sub(HTTP_REG_EXP, "", key).replace("_", "-")
                nim_headers[transformed_key] = value

        return nim_headers

    @classmethod
    def get_all_headers(cls, request):
        headers = dict()
        for key, value in request.META.items():
            headers[key] = value

        return headers

    @classmethod
    def get_header_by_name(cls, request, header_name, default_value):
        return request.META.get(header_name, default_value)

    @classmethod
    def adjust_string_length(cls, value, max_length):
        TRUNCATE_INDICATOR = "---[TRUNCATED]---"
        if isinstance(value, bytes):
            value = value.decode("UTF-8")
        output = value

        if max_length and max_length.upper() != "OFF":
            max_length = int(max_length)
            value = value
            length = len(value)
            if length > max_length:
                extra_chars = int(math.floor((length - max_length) / 2))
                adjust_even = 1 if length % 2 == 0 else 0
                middle = int(math.ceil(length / 2))
                output = "".join([value[:middle - extra_chars], TRUNCATE_INDICATOR, value[middle + extra_chars + adjust_even:]])
        return output

    @classmethod
    def get_time_in_milliseconds(cls):
        return int(round(time.time() * 1000))

    @classmethod
    def obfuscate_headers(cls, headers):
        _headers = headers.copy()
        log_label_obfuscate = getattr(settings, LOG_LABEL_OBFUSCATE, dict())
        if "headers" in log_label_obfuscate:
            headers_to_obfuscate = cls.array_intersection(log_label_obfuscate["headers"], _headers)
            for header_name in headers_to_obfuscate:
                _headers[header_name] = "[--HIDDEN--]"

        return _headers

    @classmethod
    def obfuscate_body(cls, body):
        body = cls.remove_new_lines(body)
        log_label_obfuscate = getattr(settings, LOG_LABEL_OBFUSCATE, dict())
        if "body" in log_label_obfuscate:
            for pattern, replacement in log_label_obfuscate["body"].items():
                if re.search(pattern, body):
                    body = re.sub(pattern, replacement, body)

        return body

    @classmethod
    def obfuscate_response(cls, response):
        response = cls.remove_new_lines(response)
        log_label_obfuscate = getattr(settings, LOG_LABEL_OBFUSCATE, dict())
        if "response" in log_label_obfuscate:
            for pattern, replacement in log_label_obfuscate["response"].items():
                if re.search(pattern, response):
                    response = re.sub(pattern, replacement, response)

        return response

    @classmethod
    def obfuscate_url(cls, url):
        log_label_obfuscate = getattr(settings, LOG_LABEL_OBFUSCATE, dict())
        if "url" in log_label_obfuscate:
            for pattern, replacement in log_label_obfuscate["url"].items():
                if re.search(pattern, url):
                    url = re.sub(pattern, replacement, url)

        return url
