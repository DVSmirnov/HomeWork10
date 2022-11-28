import socket

HOST = "127.0.0.1"
PORT = 65222


def full_proc(data):
    codes = {100: b"Continue", 101: b"Switching Protocols", 102: b"Processing", 103: b"Early Hints", 201: b"Created",
             202: b"Accepted", 203: b"Non-Authoritative Information", 204: b"No Content", 205: b"Reset Content",
             206: b"Partial Content", 207: b"Multi-Status", 208: b"Already Reported", 226: b"IM Used",
             300: b"Multiple Choices", 301: b"Moved Permanently", 302: b"Moved Temporarily, Found", 303: b"See Other",
             304: b"Not Modified", 305: b"Use Proxy", 306: b"Switch Proxy", 307: b"Temporary Redirect",
             308: b"Permanent Redirect", 400: b"Bad Request", 401: b"Unauthorized", 402: b"Payment Required",
             403: b"Forbidden", 404: b"Not Found", 405: b"Method Not Allowed", 406: b"Not Acceptable",
             407: b"Proxy Authentication Required", 408: b"Request Timeout", 409: b"Conflict", 410: b"Gone",
             411: b"Length Required", 412: b"Precondition Failed", 413: b"Payload Too Large", 414: b"URI Too Long",
             415: b"Unsupported Media Type", 416: b"Range Not Satisfiable", 417: b"Expectation Failed",
             419: b"Authentication Timeout", 421: b"Misdirected Request", 422: b"Unprocessable Entity", 423: b"Locked",
             424: b"Failed Dependency", 425: b"Too Early", 426: b"Upgrade Required", 428: b"Precondition Required",
             429: b"Too Many Requests", 431: b"Request Header Fields Too Large", 449: b"Retry With",
             451: b"Unavailable For Legal Reasons", 499: b"Client Closed Request", 500: b"Internal Server Error",
             501: b"Not Implemented", 502: b"Bad Gateway", 503: b"Service Unavailable", 504: b"Gateway Timeout",
             505: b"HTTP Version Not Supported", 506: b"Variant Also Negotiates", 507: b"Insufficient Storage",
             508: b"Loop Detected", 509: b"Bandwidth Limit Exceeded", 510: b"Not Extended",
             511: b"Network Authentication Required", 520: b"Unknown Error", 521: b"Web Server Is Down",
             522: b"Connection Timed Out", 523: b"Origin Is Unreachable", 524: b"A Timeout Occurred",
             525: b"SSL Handshake Failed", 526: b"Invalid SSL Certificate"}
    part_one, headers = data.split(b"\r\n", 1)

    method, part_two = part_one.split(b" ", 1)
    first_part_to_transfer = b"Request Method: " + method + b"\r\n"
    if br"/?status=" in part_two:
        index = part_two.find(b"=")
        if part_two[index + 4:index + 5] == b" ":
            three_character_string_in_bytes = part_two[index + 1:index + 4]
            three_character_string = three_character_string_in_bytes.decode("utf-8")
            if three_character_string.isdigit():
                code = int(three_character_string)
                if code in codes:
                    second_part_to_transfer = b"Response Status: " + three_character_string_in_bytes + b" " + codes[
                        code] + b"\r\n"
                else:
                    second_part_to_transfer = b"Response Status: 200 OK\r\n"
            else:
                second_part_to_transfer = b"Response Status: 200 OK\r\n"
        else:
            second_part_to_transfer = b"Response Status: 200 OK\r\n"
    else:
        second_part_to_transfer = b"Response Status: 200 OK\r\n"
    second_part_to_transfer += headers
    return first_part_to_transfer, second_part_to_transfer


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print("Сервер запущен")
    while True:
        conn, addr = s.accept()
        with conn:
            data = conn.recv(1024)
            print(f"Получено: {data}")
            first_part, second_part = full_proc(data)
            sending_data = first_part + b"Request Source: " + str(addr).encode("utf-8") + b"\r\n" + second_part
            conn.send(sending_data)
