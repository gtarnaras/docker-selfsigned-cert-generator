#!/usr/bin/env python3
"""

    Name:           gen_self_signed_cert.py
    Author:         George Tarnaras
    Description:    Generates a self signed cert to be used with AWS LBs
    Kudos:          https://stackoverflow.com/questions/27164354/create-a-self-signed-x509-certificate-in-python

"""
import os, sys
from time import gmtime, mktime
from OpenSSL import crypto, SSL


class certGenerator():

    def __init__(self):
        """
        Init
        """
        self.emailAddress = "emailAddress"
        self.commonName = "commonName"
        self.countryName = "countryName"
        self.localityName = "localityName"
        self.stateOrProvinceName = "stateOrProvinceName"
        self.organizationName = "organizationName"
        self.serialNumber = 0
        self.validityStartInSeconds = 0
        self.validityEndInSeconds = 1*365*24*60*60 # 1 year
        self.KEY_FILE = "private.key"
        self.CERT_FILE = "selfsigned.crt"

    def cert_gen(self):
        """
        Generate the self signed certs according
        to constructor's values
        """

        # create a key pair
        k = crypto.PKey()
        k.generate_key(crypto.TYPE_RSA, 4096)

        # create a self-signed cert
        cert = crypto.X509()
        cert.get_subject().C = self.countryName
        cert.get_subject().ST = self.stateOrProvinceName
        cert.get_subject().L = self.localityName
        cert.get_subject().O = self.organizationName
        cert.get_subject().OU = self.organizationName
        cert.get_subject().CN = self.commonName
        cert.get_subject().emailAddress = self.emailAddress
        cert.set_serial_number(self.serialNumber)
        cert.gmtime_adj_notBefore(0)
        cert.gmtime_adj_notAfter(int(self.validityEndInSeconds))
        cert.set_issuer(cert.get_subject())
        cert.set_pubkey(k)
        cert.sign(k, 'sha512')

        with open(self.CERT_FILE, "wt") as f:
            f.write(
                crypto.dump_certificate(
                    crypto.FILETYPE_PEM,
                    cert
                    ).decode("utf-8")
            )
        with open(self.KEY_FILE, "wt") as f:
            f.write(
                crypto.dump_privatekey(
                    crypto.FILETYPE_PEM,
                    k).decode("utf-8")
            )
        return 0

    def print_upload_commands(self):
        """
        Print the upload commands
        :returns: string
        """
        print(
            f"Now run: "
            f"aws iam upload-server-certificate "
            f"--server-certificate-name {self.commonName} "
            f"--certificate-body file://{self.CERT_FILE} "
            f"--private-key file://{self.KEY_FILE}"
        )
        return 0

    def validate(self):
        """
        Look at generated file using openssl
        """
        is_valid = os.system(
            f"openssl x509 "
            f"-inform pem "
            f"-in {self.CERT_FILE} "
            f"-noout "
            f"-text"
        )
        if is_valid == 0:
            return True
        else: False

def main():
    generator = certGenerator()
    generator.cert_gen()
    if generator.validate():
        generator.print_upload_commands()
        sys.exit(0)
    else:
        print(f"Cert was not valid, exiting...")
        sys.exit(1)

if __name__ == "__main__":
    main()
