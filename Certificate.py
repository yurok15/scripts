class Certificate():


    def __init__(self, pfx_path, pfx_passwd):
        self.pfx_path = pfx_path
        self.pfx_passwd = pfx_passwd


    def get_cert(self):
        command = "/usr/bin/openssl pkcs12 -in {} -passin pass:{} -nodes -nokeys 2>/dev/null".format(self.pfx_path, self.pfx_passwd)
        with subprocess.Popen(command, shell=True, stdout=subprocess.PIPE) as self.cert:
            self.certificate = self.cert.stdout.read()
        return(self.certificate)


    def get_key(self):
        command = "/usr/bin/openssl pkcs12 -in {} -passin pass:{} -nodes -nocerts 2>/dev/null".format(self.pfx_path, self.pfx_passwd)
        with subprocess.Popen(command, shell=True, stdout=subprocess.PIPE) as self.key:
            self.key = self.key.stdout.read()
        return(self.certificate)
