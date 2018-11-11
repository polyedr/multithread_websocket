import socket
import pickle
import subprocess

import config


# List of urls to download
urls = [
    'https://www.irs.gov/pub/irs-pdf/f1040.pdf',
    'https://www.irs.gov/pub/irs-pdf/f1040a.pdf',
    'https://www.irs.gov/pub/irs-pdf/f1040ez.pdf',
    'https://www.irs.gov/pub/irs-pdf/f1040es.pdf',
    'https://www.irs.gov/pub/irs-pdf/f1040sb.pdf'
]

if __name__ == '__main__':
    # Bytes ranges check
    for url in urls:
        result = subprocess.run(['curl', '-I', url], stdout=subprocess.PIPE)
        curl_result_decode = result.stdout.decode('utf-8')
        if 'Accept-Ranges: bytes' in curl_result_decode:
            print(url, 'Bytes ranges are supported')
        else:
            print(url, 'Bytes ranges are not supported')

    # Socket start
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    sock.bind((config.host, config.port))

    sock.listen(True)

    while True:
        conn, addr = sock.accept()
        print('Connecting', addr)
        data = pickle.dumps(urls)
        conn.sendall(data)
