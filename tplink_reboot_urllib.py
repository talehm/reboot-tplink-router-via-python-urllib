import hashlib
import urllib
import sys
import urllib.parse
import urllib.request
import codecs
from base64 import b64encode, b64decode
from urllib.error import HTTPError


class TPLink_WR840N_v2:
    """ Class for scraping/navigating the TPLink WR840N v2. Originally for
    the purpose of scheduling reboots using cron. Can probably be extended to automate
    many other functions in the web UI with a little bit of snooping around the html
    Thanks to https://github.com/vicwomg
    """

    def __init__(self, router_ip, username, password):
        self.latest_tested_version = "3.16.9 Build 160406 Rel.40792n"

        self.login_url = "http://%s/userRpm/LoginRpm.htm?Save=Save"
        self.reboot_url_path = "/userRpm/SysRebootRpm.htm"

        self.router_ip = router_ip
        self.username = username
        self.password = password.encode('utf-8')

    def login(self):
        self.cookie = self.get_auth_cookie()
        self.get_session_url()

    def get_auth_cookie(self):
        hexmd5_pw = hashlib.md5(self.password).hexdigest()
        string = self.username + ":" + hexmd5_pw
        encoded = urllib.parse.quote_plus(
            str(b64encode(string.encode('utf-8')), 'utf-8').strip())

        cookie = "Authorization=Basic%20" + encoded
        return cookie

    def get_session_url(self):
        opener = urllib.request.build_opener()
        opener.addheaders.append(('Cookie', self.cookie))
        f = opener.open(self.login_url % self.router_ip)
        output = f.read().decode("utf-8")
        router_url = "http://%s" % self.router_ip
        # router_url = bytes(router_url, 'utf-8')
        if (router_url in output):
            url_auth_string = output.split(
                self.router_ip)[1].split('/')[1]
            self.session_url = "http://%s/%s" % (
                self.router_ip, url_auth_string)
            opener.close()
            f.close()
        else:
            """  print("ERROR: Failed to scrape out session url. ")
             print("  Bad username/password? ")
             print("  Or you're already logged in to the admin interface somewhere else?")
             print("  Or perhaps unsupported web UI firmware. Last tested on: " +
                   self.latest_tested_version) """
            sys.exit(1)

    def reboot(self):

        reboot_params = "?Reboot=Reboot"
        referer = self.session_url + self.reboot_url_path
        reboot_command_url = referer + reboot_params
        # print("Rebooting router with: %s ..." % reboot_command_url)

        opener = urllib.request.build_opener()

        # needs proper cookie and referer or it will fail authorization
        opener.addheaders.append(('Cookie', self.cookie))
        opener.addheaders.append(('Referer', referer))

        f = opener.open(reboot_command_url)
        opener.close()
        f.close()
        # print("Reboot command sent")


def runScript(AP_name, address, username, password):
    try:
        print(AP_name+" : "+address)
        tp = TPLink_WR840N_v2(address, username, password)
        tp.login()
        tp.reboot()
        return None, True
    except HTTPError as e:
        # print(e)
        if e.code == 403:
            return 403, False
        return e, False


if __name__ == "__main__":
    runScript(address, username, password)
