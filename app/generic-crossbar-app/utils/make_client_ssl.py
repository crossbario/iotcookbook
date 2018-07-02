#!/usr/bin/env python
"""
    This routine attempts to create a client key/certificate to access a
    Crossbar server via a certificate based SSL connection.

"""
import sys
import argparse
import base64
from OpenSSL import crypto


def createKeyPair(type, bits):
    pkey = crypto.PKey()
    pkey.generate_key(type, bits)
    return pkey


def createCertRequest(pkey, digest="sha256", **name):
    req = crypto.X509Req()
    subj = req.get_subject()
    for (key, value) in name.items():
        setattr(subj, key, value)
    req.set_pubkey(pkey)
    req.sign(pkey, digest)
    return req


def createCertificate(req, issuer, serial, timing, digest="sha256"):
    (issuerCert, issuerKey) = issuer
    (notBefore, notAfter) = timing
    cert = crypto.X509()
    cert.set_serial_number(serial)
    cert.gmtime_adj_notBefore(notBefore)
    cert.gmtime_adj_notAfter(notAfter)
    cert.set_issuer(issuerCert.get_subject())
    cert.set_subject(req.get_subject())
    cert.set_pubkey(req.get_pubkey())
    cert.sign(issuerKey, digest)
    return cert


def createClient(crt, key, common_name, serial):
    cacert = crypto.load_certificate(crypto.FILETYPE_PEM, crt)
    cakey = crypto.load_privatekey(crypto.FILETYPE_PEM, key)
    pkey = createKeyPair(crypto.TYPE_RSA, 4096)
    req = createCertRequest(pkey, CN=common_name)
    cert = createCertificate(req, (cacert, cakey), serial, (0, 60*60*24*365*10))
    key = crypto.dump_privatekey(crypto.FILETYPE_PEM, pkey)
    crt = crypto.dump_certificate(crypto.FILETYPE_PEM, cert)
    return (key, crt)

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--serial', dest='serial', type=int, default='1', help='The serial number for the cert')
    parser.add_argument('--host', required=True, dest='host', type=str,  help='The host name to insert in the cert')
    args = parser.parse_args()

    with open('certs/server_key.pem') as io:
        cakey = io.read()
    with open('certs/server_crt.pem') as io:
        cacrt = io.read()

    key, crt = createClient(cacrt, cakey, args.host, args.serial)

    cacert = crypto.load_certificate(crypto.FILETYPE_PEM, crt)
    fingerprint = cacert.digest("sha256").decode('utf-8')

    with open('certs/client_{}_key.pem'.format(args.host), 'w') as io:
        io.write(key.decode('utf-8'))
    with open('certs/client_{}_crt.pem'.format(args.host), 'w') as io:
        io.write(crt.decode('utf-8'))

    print('Client fingerprint ({})'.format(fingerprint))
