import argparse
import subprocess


parser = argparse.ArgumentParser(prog='cert')
parser.add_argument('--pfx_path', dest='pfx_path', type=str, help='full path to Pfx')
parser.add_argument('--pfx_passwd', dest='pfx_passwd', type=str, help='Pfx password')
args = parser.parse_args()

class Certificate():


    def __init__(self, pfx_path, pfx_passwd):
        self.pfx_path = pfx_path
        self.pfx_passwd = pfx_passwd

    def get_value(self, value):
        command = "/usr/bin/openssl pkcs12 -in {} -passin pass:{} -nodes {} 2>/dev/null".format(self.pfx_path, self.pfx_passwd, value)
        with subprocess.Popen(command, shell=True, stdout=subprocess.PIPE) as self.value:
            self.requested_value = self.value.stdout.read()
        return(self.requested_value)

    def get_cert(self):
        #command = "/usr/bin/openssl pkcs12 -in {} -passin pass:{} -nodes -nokeys 2>/dev/null".format(self.pfx_path, self.pfx_passwd)
        #with subprocess.Popen(command, shell=True, stdout=subprocess.PIPE) as self.cert:
        #    self.certificate = self.cert.stdout.read()
        return(get_value('-nokeys'))


    def get_key(self):
        command = "/usr/bin/openssl pkcs12 -in {} -passin pass:{} -nodes -nocerts 2>/dev/null".format(self.pfx_path, self.pfx_passwd)
        with subprocess.Popen(command, shell=True, stdout=subprocess.PIPE) as self.key:
            self.key = self.key.stdout.read()
        return(self.key)

    def get_pem(self):
        command = "/usr/bin/openssl pkcs12 -in {} -passin pass:{} -nodes 2>/dev/null".format(self.pfx_path, self.pfx_passwd)
        with subprocess.Popen(command, shell=True, stdout=subprocess.PIPE) as self.pem:
            self.pem = self.pem.stdout.read()
        return(self.pem)


cert = Certificate(args.pfx_path, args.pfx_passwd)
print(cert.get_pem().decode("utf8"))
