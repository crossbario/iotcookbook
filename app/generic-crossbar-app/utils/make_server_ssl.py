#!/usr/bin/env python
"""
    Create a self-signed server certificate.
"""
from socket import gethostname
import base64
import io
import argparse
from OpenSSL import crypto


if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--country', dest='country', type=str,  help='Your country code')
    parser.add_argument('--state', dest='state', type=str,  help='Your state')
    parser.add_argument('--city', dest='city', type=str,  help='Your city')
    parser.add_argument('--company', dest='company', type=str,  help='Your company name')
    parser.add_argument('--org', dest='org', type=str,  help='Your organisation name')
    parser.add_argument('--hostname', dest='host', type=str,  help='Your host / domain / common name')
    parser.add_argument('--weeks', dest='weeks', type=int, help='Lifetime of certificate in weeks')
    args = parser.parse_args()

    try:
        with open('certs/server_crt.pem') as io:
            text = io.read()
            if text:
                crt = crypto.load_certificate(crypto.FILETYPE_PEM, text)
                serial = crt.get_serial_number()+1
            else:
                serial = 1
    except Exception:
        serial = 1

    key = crypto.PKey()
    key.generate_key(crypto.TYPE_RSA, 4096)
    crt = crypto.X509()
    crt.get_subject().C = args.country or 'UK'
    crt.get_subject().ST = args.state or 'South Wales'
    crt.get_subject().L = args.city or 'Pontypridd'
    crt.get_subject().O = args.company or 'Crossbar.IO'
    crt.get_subject().OU = args.org or 'XBR'
    crt.get_subject().CN = args.host or gethostname()
    crt.set_serial_number(serial)
    crt.gmtime_adj_notBefore(0)
    crt.gmtime_adj_notAfter(7*24*60*60*(args.weeks or 52))
    crt.set_issuer(crt.get_subject())
    crt.set_pubkey(key)
    crt.sign(key, 'sha1')

    c_str = crypto.dump_certificate(crypto.FILETYPE_PEM, crt)
    k_str = crypto.dump_privatekey(crypto.FILETYPE_PEM, key)

    with open('certs/server_crt.pem', 'w') as io:
        io.write(c_str.decode('utf-8'))

    with open('certs/server_key.pem', 'w') as io:
        io.write(k_str.decode('utf-8'))

    print("Server certificates installed, don't forget to regenerate your client certs!")
