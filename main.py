import os, time, requests, subprocess, sys
from halo import Halo

# Just a quick check to make sure this script is only being run on Windows PC's
if os.name == 'nt':
    pass
elif os.name == 'posix':
    print("✖|⚠ This program needs to be run on a Windows PC!")
    time.sleep(10)
    sys.exit()

def versionInfo() -> list:
    version = "1.0.0"
    year = "2023"
    prod = True
    owner = "J Stuff (https://j-stuff.net)"
    return [version, year, prod, owner]

def disclaimer():
    os.system('cls')
    version = versionInfo()
    if not version[2]:
        print("THIS SCRIPT IS RUNNING IN NON-PROD!!!!")
    print(f'''
Copyright - {version[1]}, {version[3]}
Version - {version[0]}

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

No Data is sent off of this device to SCP:SL Technical Support or NORTHWOOD Studios. There is 1 request made to (https://api.ipify.org/) to get this device's IP address, which is required for this test to run. Their Privacy policy & TOS can be found here: (https://geo.ipify.org/privacy-policy, https://geo.ipify.org/terms-of-service)

If you do not concent to these conditions, Close this program now by pressing close on this window, or by pressing the keybind (CTRL + C)!
''')
    input("Press ENTER to continue...")
    os.system('cls')

class getIP():
    def __init__(self) -> None:
        pass

    class fetchFailed(Exception):
        pass

    def fetch(self) -> str:
        url = "https://api.ipify.org"
        try:
            x = requests.get(url)
        except:
            raise self.fetchFailed("THE FETCH ATTEMPT FAILED!")
        return x.text

    def ip(self) -> str:
        spinner = Halo(text="Retrieving IP Address for test...", spinner="bouncingBar", animation="bounce", color="blue", text_color="yellow")
        spinner.start()
        try:
            ip = self.fetch()
        except self.fetchFailed:
            spinner.fail(text="The fetch attempt failed, Please ensure you are connected to the internet and try again. If this keeps happening please inform the Technical Support Agent helping you that this has happened.")
            input("Press ENTER to close ")
            raise Exception("Fetch Failed!")
        spinner.succeed(f"Got IP address: {ip}")
        return ip

class NAT_test():
    def __init__(self) -> None:
        pass

    def run(self, ip:str) -> list:
        version = versionInfo()
        cmd = [ 'tracert', '-4', ip]
        output = subprocess.Popen( cmd, stdout=subprocess.PIPE ).communicate()[0]
        formatted = output.decode()
        if not version[2]:
            print(formatted)
        listFormatted = formatted.splitlines()
        listFormatted = listFormatted[4:]
        traceLength = listFormatted[:len(listFormatted) - 2]
        if not version[2]:
            print([line for line in traceLength])
        return traceLength
    
    def test(self, ip:str) -> None:
        spinner = Halo(text="Running CG-NAT Test (This may take some time...)", spinner="bouncingBar", animation="bounce", color="blue", text_color="yellow")
        spinner.start()
        trace = self.run(ip)
        if len(trace) == 0:
            spinner.warn("The test couldn't complete successfully. Please try again.")
            print("DEBUG:")
            for line in trace:
                print(" -- " + line)
            input("Press ENTER to close ")
            raise Exception("Test Failed! (is 0 len)")
        elif len(trace) <= 2:
            spinner.succeed("Test Passed. Please post this in your ticket.")
            print("DEBUG:")
            for line in trace:
                print(" -- " + line)
            input("Press ENTER to close ")
            return 
        elif len(trace) >= 3:
            spinner.fail("Test Failed. Please screenshot this and post it in your ticket (Press WIN + SHIFT + S)")
            print("DEBUG:")
            for line in trace:
                print(" -- " + line)
            input("Press ENTER to close ")
            return
        else:
            spinner.warn("The test couldn't complete successfully. Please try again.")
            input("Press ENTER to close ")
            return

disclaimer()
NATtest = NAT_test()
ipTest = getIP()
NATtest.test(ipTest.ip())
# NATtest.test("1.1.1.1")