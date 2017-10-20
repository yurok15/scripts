import argparse
import subprocess
import os


parser = argparse.ArgumentParser(prog='cert')
parser.add_argument('--pfx_path', dest='pfx_path', type=str, help='full path to Pfx')
parser.add_argument('--pfx_passwd', dest='pfx_passwd', type=str, help='Pfx password')
args = parser.parse_args()

class Certificate():


    def __init__(self, pfx_path, pfx_passwd):
        self.pfx_path = pfx_path
        self.pfx_passwd = pfx_passwd


    def get_value(self, value=''):
        command = "/usr/bin/openssl pkcs12 -in {} -passin pass:{} -nodes {} 2>/dev/null".format(self.pfx_path, self.pfx_passwd, value)
        #print(command)
        with subprocess.Popen(command, shell=True, stdout=subprocess.PIPE) as self.pfx:
            self.requested_value = self.pfx.stdout.read()
        return(self.requested_value)


    def get_cert(self):
        return(self.get_value('-nokeys'))


    def get_key(self):
        return(self.get_value('-nocerts'))

    def get_pem(self):
        return(self.get_value())


cert = Certificate(args.pfx_path, args.pfx_passwd)

#print(cert.get_pem().decode("utf8"))
#print("".join(args.pfx_path.split('.')[:-1])+ "." + "cer")
key_path = "".join(args.pfx_path.split(".")[:-1])+ "." + "key"
cert_path = "".join(args.pfx_path.split(".")[:-1])+ "." + "crt"
key = open(key_path, 'w')
key.write(cert.get_key().decode("utf8"))
key.close()
cer = open(cert_path, 'w')
cer.write(cert.get_cert().decode("utf8"))
cer.close()
