import base64, re


def base64_to_bytes(base64_string):
    return base64.b64decode(base64_string)

def base64_to_hex(base64_string):
    return base64.b64decode(base64_string).hex()

def hex_to_base64(hex_string):
    return base64.b64encode(bytes.fromhex(hex_string)).decode('utf-8')

def hex_to_bytes(hex_string):
    # We will convert hex to base64, then base64 to bytes
    dataInBase64 = hex_to_base64(hex_string)
    dataInBytes = base64_to_bytes(dataInBase64)
    return dataInBytes

def extract_jwt(text):
  pattern = r'eyJ[a-zA-Z0-9_-]*\.[a-zA-Z0-9_-]*\.[a-zA-Z0-9_-]*'
  match = re.search(pattern, text)
  if match:
      return match.group(0)
  else:
      return None

def get_www_headers(jwt):
    required_headers = {
        "content-type" : "application/grpc-web+proto",
        "authorization" : f"Bearer {jwt}",
    }

    additional_headers = {
        "Host": "www.tayara.tn",
        "Connection": "keep-alive",
        "sec-ch-ua": '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
        "sec-ch-ua-mobile": '?0',
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        "sec-ch-ua-platform": '"Windows"',
        "Accept": "*/*",
        "Origin": "https://www.tayara.tn",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://www.tayara.tn/post-listing/?postStep=celebrate",
        "Accept-Language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7,de;q=0.6,ar;q=0.5",
    }

    www_headers =  dict(required_headers.items() | additional_headers.items())
    return www_headers


def get_auth_headers():
    authentification_headers = {
        'Host': 'authentication.tayara.tn',
        'Connection': 'keep-alive',
        'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
        'x-grpc-web': '1',
        'Content-Type': 'application/grpc-web+proto',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'sec-ch-ua-platform': '"Windows"',
        'Accept': '*/*',
        'Origin': 'https://www.tayara.tn'
    }
    return authentification_headers

def clean_spaces_from_hex_code(hex_code):
    while ' ' in hex_code:
        hex_code = hex_code.replace(' ','')
    return hex_code