import argparse, os, requests, time, csv, datetime, glob, subprocess
import ConfigParser, smtplib
from signal import signal, alarm, SIGALRM

today = datetime.date.today()

__author__ = 'Caleb Kinney'


def get_args():
    parser = argparse.ArgumentParser(
        description='domained')
    parser.add_argument(
        '-d', '--domain', type=str, help='Domain', required=False, default=False)
    parser.add_argument(
        '-s', '--secure', help='Secure', nargs='?', required=False, default=False)
    parser.add_argument(
        '-b', '--bruteforce', help='Bruceforce', nargs='?', default=False)
    parser.add_argument(
        '--upgrade', help='Upgrade', nargs='?', default=False)
    parser.add_argument(
        '--install', help='Install', nargs='?', default=False)
    parser.add_argument(
        '--vpn', help='VPN Check', nargs='?', default=False)
    parser.add_argument(
        '-p', '--ports', help='Ports', nargs='?', default=False)
    parser.add_argument(
        '-q', '--quick', help='Quick', nargs='?', default=False)
    parser.add_argument(
        '--bruteall', help='Bruteforce JHaddix All', nargs='?', default=False)
    parser.add_argument(
        '--fresh', help='Remove output Folder', nargs='?', default=False)
    parser.add_argument(
        '--notify', help='Notify when script completed', nargs='?', default=False)
    parser.add_argument(
        '--active', help='EyeWitness Active Scan', nargs='?', default=False)

    return parser.parse_args()


newpath = r'output'
if not os.path.exists(newpath):
    os.makedirs(newpath)


def banner():
    print("""\033[1;31m
                                             _ 
                                            | |
     _ __ ___  ___ ___  _ __  _ __   ___  __| |
    | '__/ _ \/ __/ _ \| '_ \| '_ \ / _ \/ _` |
    | | |  __/ (_| (_) | | | | | | |  __/ (_| |
    |_|  \___|\___\___/|_| |_|_| |_|\___|\__, |`
         ___/ /__  __ _  ___ _(_)__  ___ ___/ /
        / _  / _ \/  ' \/ _ `/ / _ \/ -_) _  / 
        \_,_/\___/_/_/_/\_,_/_/_//_/\__/\_,_/  
    \033[1;34m\t\t\t\treconned.org\033[1;m""")
    globpath = ("*.csv")
    globpath2 = ("*.lst")
    if (next(glob.iglob(globpath), None)) or (next(glob.iglob(globpath2), None)):
        print("\nThe following files may be left over from failed domained attempts:")
        for file in glob.glob(globpath):
            print("  - " + file)
        for file in glob.glob(globpath2):
            print("  - " + file)
        signal(SIGALRM, lambda x: 1 / 0)
        try:
            alarm(5)
            RemoveQ = raw_input("\nWould you like to remove the files? [y/n]: ")
            if RemoveQ.lower() == "y":
                os.system("rm *.csv")
                os.system("rm *.lst")
                print("\nFiles removed\nStarting domained...")
                time.sleep(5)
            else:
                print("\nThank you.\nPlease wait...")
                time.sleep(5)
        except:
            print("\n\nStarting domained...")


def sublist3r():
    print("\n\n\033[1;31mRunning Sublist3r \n\033[1;37m")
    sublist3rFileName = ("output/" + domain + "_sublist3r.txt")
    Subcmd = (("python bin/Sublist3r/sublist3r.py -v -t 15 -d %s -o " + sublist3rFileName) % (domain))
    print("\n\033[1;31mRunning Command: \033[1;37m" + Subcmd)
    os.system(Subcmd)
    print("\n\033[1;31mSublist3r Complete\033[1;37m")
    time.sleep(1)


def sublist3rBrute():
    print("\n\n\033[1;31mRunning Sublist3r \n\033[1;37m")
    sublist3rFileName = ("output/" + domain + "_sublist3r.txt")
    Subcmd = (("python bin/Sublist3r/sublist3r.py -v -b -t 15 -d %s -o " + sublist3rFileName) % (domain))
    print("\n\033[1;31mRunning Command: \033[1;37m" + Subcmd)
    os.system(Subcmd)
    print("\n\033[1;31mSublist3r Complete\033[1;37m")
    time.sleep(1)
    eyewitness(sublist3rFileName)


def enumall():
    print("\n\n\033[1;31mRunning Enumall \n\033[1;37m")
    enumallCMD = "python bin/domain/enumall.py %s" % (domain)
    print("\n\033[1;31mRunning Command: \033[1;37m" + enumallCMD)
    os.system(enumallCMD)
    print("\n\033[1;31menumall Complete\033[1;37m")
    time.sleep(1)


def massdns():
    print("\n\n\033[1;31mRunning massdns \n\033[1;37m")
    if bruteall is not False:
        massdnsCMD = (
            "./bin/subbrute/subbrute.py -s ./bin/sublst/all.txt " + domain + " | ./bin/massdns/bin/massdns -r resolvers.txt -t A -a -o -w ./output/" + domain + "-massdns.txt -")
        print("\n\033[1;31mRunning Command: \033[1;37m" + massdnsCMD)
        os.system(massdnsCMD)
        print("\n\033[1;31mMasscan Complete\033[1;37m")
    else:
        massdnsCMD = (
            "./bin/subbrute/subbrute.py -s ./bin/sublst/sl-domains.txt " + domain + " | ./bin/massdns/bin/massdns -r resolvers.txt -t A -a -o -w ./output/" + domain + "-massdns.txt -")
        print("\n\033[1;31mRunning Command: \033[1;37m" + massdnsCMD)
        os.system(massdnsCMD)
        print("\n\033[1;31mMasscan Complete\033[1;37m")
    time.sleep(1)


def knockpy():
    print("\n\n\033[1;31mRunning Knock \n\033[1;37m")
    knockpyCmd = ("python bin/knockpy/knockpy/knockpy.py -c " + domain)
    print("\n\033[1;31mRunning Command: \033[1;37m" + knockpyCmd)
    os.system(knockpyCmd)
    rootdomainStrip = domain.replace(".", "_")
    knockpyFilenameInit = ("output/" + domain + "_knock.csv")
    os.system("mv " + rootdomainStrip + "* " + knockpyFilenameInit)
    time.sleep(1)
    knockpySubs = []
    try:
        with open(knockpyFilenameInit, 'rb') as f:
            reader = csv.reader(f, delimiter=',')
            for row in reader:
                knockpySubs.append(row[3])
        filenameKnocktxt = (knockpyFilenameInit + ".txt")
        f1 = open(filenameKnocktxt, "w")
        for hosts in knockpySubs:
            hosts = "".join(hosts)
            f1.writelines("\n" + hosts)
        f1.close()
    except:
        print("\nKnock File Error\n")
    time.sleep(1)


def eyewitness(filename):
    print("\n\n\033[1;31mRunning EyeWitness  \n\033[1;37m")
    rootdomain = domain
    if active is not False:
        EWHTTPScriptIPS = (
            "python bin/EyeWitness/EyeWitness.py -f " + filename + " --active-scan --no-prompt --headless  -d " + "output/" + rootdomain + "-" + time.strftime(
                '%m-%d-%y-%H-%M') + "-EW ")
    else:
        EWHTTPScriptIPS = (
            "python bin/EyeWitness/EyeWitness.py -f " + filename + " --no-prompt --headless  -d " + "output/" + rootdomain + "-" + time.strftime(
                '%m-%d-%y-%H-%M') + "-EW ")
    if vpn is not False:
        print(
            "\n\033[1;31mIf not connected to VPN manually run the following command on reconnect:\n\033[1;37m" + EWHTTPScriptIPS)
        vpncheck()
    print("\n\033[1;31mRunning Command: \033[1;37m" + EWHTTPScriptIPS)
    os.system(EWHTTPScriptIPS)
    print("\a")


def upgradeFiles():
    binpath = r'bin'
    if not os.path.exists(binpath):
        os.makedirs(binpath)
    else:
        os.system("rm -r bin")
        os.makedirs(binpath)
    sublist3rUpgrade = ("git clone https://github.com/aboul3la/Sublist3r.git ./bin/Sublist3r")
    print("\n\033[1;31mInstalling Sublist3r \033[1;37m")
    os.system(sublist3rUpgrade)
    subInstallReq = ("sudo pip install -r bin/Sublist3r/requirements.txt")
    os.system(subInstallReq)
    print("Sublist3r Installed\n")
    eyeWitnessUpgrade = ("git clone https://github.com/ChrisTruncer/EyeWitness.git ./bin/EyeWitness")
    print("\n\033[1;31mInstalling EyeWitness \033[1;37m" + eyeWitnessUpgrade)
    os.system(eyeWitnessUpgrade)
    eyeInstallReq = ("sudo bash bin/EyeWitness/setup/setup.sh")
    print("\n\033[1;31mRunning Command: \033[1;37m")
    os.system(eyeInstallReq)
    if os.path.isfile("phantomjs") == False:
        print("\nNo phantomjs File Found")
        unameChk = subprocess.check_output(['uname', '-m'])
        if "x86_64" in unameChk:
            print("\nDownloading 64-Bit phantomjs")
            os.system("wget -O phantomjs https://www.christophertruncer.com/InstallMe/kali2phantomjs")
        elif "arm" in unameChk:
            print("\nDownloading RaspberryPi phantomjs")
            os.system(
                "wget -O phantomjs https://github.com/fg2it/phantomjs-on-raspberry/releases/download/v2.1.1-wheezy-jessie-armv6/phantomjs")
        else:
            print("\nDownloading 32-Bit phantomjs")
            os.system("wget -O phantomjs https://www.christophertruncer.com/InstallMe/phantom32kali2")
        os.system("chmod +x phantomjs")
    delGeco = ("rm gecko*")
    os.system(delGeco)
    cpphantomjs = ("cp phantomjs ./bin/EyeWitness/bin/")
    os.system(cpphantomjs)
    movephantomjs = ("mv phantomjs bin/")
    os.system(movephantomjs)
    print("\nEyeWitness Installed\n")
    enumallUpgrade = ("git clone https://github.com/jhaddix/domain.git ./bin/domain")
    print("\n\033[1;31mInstalling Enumall \033[1;37m")
    print("\nenumall Installed\n")
    os.system(enumallUpgrade)
    knockpyUpgrade = ("git clone https://github.com/guelfoweb/knock.git ./bin/knockpy")
    print("\n\033[1;31mInstalling Knock \033[1;37m")
    os.system(knockpyUpgrade)
    print("\nKnockpy Installed\n")
    sublstUpgrade = ("git clone https://gist.github.com/jhaddix/86a06c5dc309d08580a018c66354a056 ./bin/sublst")
    print("\n\033[1;31mCopying JHaddix All Domain List: \033[1;37m")
    print("\nJHaddix All Domain List Installed\n")
    os.system(sublstUpgrade)
    SLsublstUpgrade = (
        "wget -O ./bin/sublst/sl-domains.txt https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/DNS/sorted_knock_dnsrecon_fierce_recon-ng.txt")
    print("\n\033[1;31mCopying SecList Domain List \033[1;37m")
    print("\nSecList Domain List Installed\n")
    os.system(SLsublstUpgrade)
    subbruteUpgrade = ("git clone https://github.com/TheRook/subbrute.git ./bin/subbrute")
    print("\n\033[1;31mInstalling Subbrute \033[1;37m")
    os.system(subbruteUpgrade)
    print("\nSubbrute Installed\n")
    massdnsUpgrade = ("git clone https://github.com/blechschmidt/massdns ./bin/massdns")
    print("\n\033[1;31mInstalling massdns \033[1;37m")
    os.system(massdnsUpgrade)
    massdnsMake = ("make -C ./bin/massdns")
    os.system("apt-get install libldns-dev -y")
    os.system(massdnsMake)
    print("\nMassdns Installed\n")
    os.system("cp ./bin/subbrute/resolvers.txt ./")
    print("\n\033[1;31mAll tools installed \033[1;37m")


def subdomainfile():
    sublist3rFileName = ("output/" + domain + "_sublist3r.txt")
    enumallFileName = (domain + ".lst")
    subdomainAllFile = ("output/" + domain + "-all.txt")
    knockpyFileName = ("output/" + domain + "_knock.csv.txt")
    massdnsFileName = ("output/" + domain + "-massdns.txt")
    f1 = open(subdomainAllFile, "w")
    f1.close()
    print("\nOpening Sublist3r File\n")
    try:
        with open(sublist3rFileName) as f:
            SubHosts = f.read().splitlines()
        f.close()
        time.sleep(2)
        subdomainCounter = 0
        f1 = open(subdomainAllFile, "a")
        f1.writelines("\n\nsublist3r")
        for hosts in SubHosts:
            hosts = "".join(hosts)
            f1.writelines("\n" + hosts)
            subdomainCounter = subdomainCounter + 1
        f1.close()
        os.remove(sublist3rFileName)
        print("\n" + str(subdomainCounter) + " Subdomains discovered by Sublist3r")
    except:
        print("\nError Opening Sublist3r File!\n")
    print("\nOpening Enumall File\n")
    try:
        with open(enumallFileName) as f:
            SubHosts = f.read().splitlines()
        f.close()
        time.sleep(2)
        subdomainCounter = 0
        f1 = open(subdomainAllFile, "a")
        f1.writelines("\n\nenumall")
        for hosts in SubHosts:
            hosts = "".join(hosts)
            f1.writelines("\n" + hosts)
            subdomainCounter = subdomainCounter + 1
        f1.close()
        os.remove(enumallFileName)
        enumallFileNamecsv = (domain + ".csv")
        os.remove(enumallFileNamecsv)
        print("\n" + str(subdomainCounter) + " Subdomains discovered by Enumall")
    except:
        print("\nError Opening Enumall File!\n")
    print("\nOpening Knock File\n")
    try:
        with open(knockpyFileName) as f:
            SubHosts = f.read().splitlines()
        f.close()
        time.sleep(2)
        subdomainCounter = 0
        f1 = open(subdomainAllFile, "a")
        f1.writelines("\n\nknock")
        for hosts in SubHosts:
            hosts = "".join(hosts)
            f1.writelines("\n" + hosts)
            subdomainCounter = subdomainCounter + 1
        f1.close()
        knockpyFileNamecsv = ("output/" + domain + "_knock.csv")
        os.remove(knockpyFileName)
        os.remove(knockpyFileNamecsv)
        print("\n" + str(subdomainCounter) + " Subdomains discovered by Knock")
    except:
        print("\nError Opening Knock File!\n")
    print("\nOpening massdns File\n")
    try:
        with open(massdnsFileName) as f:
            SubHosts = f.read().splitlines()
        f.close()
        time.sleep(2)
        subdomainCounter = 0
        f1 = open(subdomainAllFile, "a")
        f1.writelines("\n\nmassdns")
        for hosts in SubHosts:
            hosts = hosts.split(".	")[0]
            if domain in hosts:
                hosts = "".join(hosts)
                f1.writelines("\n" + hosts)
                subdomainCounter = subdomainCounter + 1
        f1.close()
        os.remove(massdnsFileName)
        print("\n" + str(subdomainCounter) + " Subdomains discovered by massdns")
    except:
        print("\nError Opening massdns File!\n")
    print("\nCombining Domains Lists\n")
    domainList = open(subdomainAllFile, 'r')
    uniqueDomains = set(domainList)
    domainList.close()
    subdomainUniqueFile = ("output/" + domain + "-unique.txt")
    uniqueDomainsOut = open(subdomainUniqueFile, 'w')
    for domains in uniqueDomains:
        domains = domains.replace('\n', '')
        if domains.endswith(domain):
            uniqueDomainsOut.writelines("https://%s" % domains + "\n")
            if ports is not False:
                uniqueDomainsOut.writelines("https://%s" % domains + ":8443" + "\n")
            if secure is False:
                uniqueDomainsOut.writelines("http://%s" % domains + "\n")
                if ports is not False:
                    uniqueDomainsOut.writelines("http://%s" % domains + ":8080" + "\n")
    uniqueDomainsOut.close()
    time.sleep(2)
    rootdomainStrip = domain.replace(".", "_")
    print("\nCleaning Up Old Files\n")
    try:
        os.system("rm " + domain + "*")
        os.system("rm " + rootdomainStrip + "*")
    except:
        print("\nError Removing Files!\n")
    eyewitness(subdomainUniqueFile)


def vpncheck():
    vpnck = requests.get('http://ipinfo.io')
    # Change "Comcast" to your provider or City")
    if "Comcast" in vpnck.content:
        print("\n\033[1;31mNot connected via VPN \033[1;37m")
        print("\n" + vpnck.content)
        print("\n\033[1;31mQuitting domained... \033[1;37m")
        quit()
    else:
        print("\n\033[1;31mConnected via VPN \033[1;37m")
        print("\n" + vpnck.content)
        time.sleep(5)


def notified():
    notifySub = ("domained Script Finished")
    notifyMsg = ("domained Script Finished for " + domain)
    Config = ConfigParser.ConfigParser()
    Config.read("./ext/notifycfg.ini")
    if (Config.get('Pushover', 'enable')) == "True":
        poToken = (Config.get('Pushover', 'token'))
        poUser = (Config.get('Pushover', 'user'))
        if "device" in Config.options('Pushover'):
            poDevice = (Config.get('Pushover', 'device'))
            poRequestPayload = {'token': poToken, 'user': poUser, 'device': poDevice, 'title': poTitle,
                                'message': poMsg}
        else:
            poRequestPayload = {'token': poToken, 'user': poUser, 'title': notifySub, 'message': notifyMsg}
            poValidatePayload = {"token": poToken, 'user': poUser}
            poValidate = requests.post('https://api.pushover.net/1/users/validate.json', data=(poValidatePayload))
            poJsonV = poValidate.json()
            if poJsonV['status'] == 1:
                print("\nPushover Account Validated\n")
                poRequest = requests.post('https://api.pushover.net/1/messages.json', data=(poRequestPayload))
                poJsonR = poRequest.json()
                if poJsonV['status'] == 1:
                    print("\nPushover Account Notified\n")
                else:
                    print("\nError - Pushover Account Not Notified\n")
            else:
                print("\nError - Pushover Account Not Validated\n")
    if (Config.get('Email', 'enable')) == "True":
        gmailUser = (Config.get('Email', 'user'))
        gmailPass = (Config.get('Email', 'password'))
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(gmailUser, gmailPass)
            subject = "domained Script Complete"
            text = ("domained Script Complete for " + domain)
            msg = 'Subject: {}\n\n{}'.format(subject, text)
            server.sendmail(gmailUser, gmailUser, msg)
            server.quit()
            print("\nEmail Notification Sent\n")
        except:
            print("\nError - Email Notification Not Sent\n")


if __name__ == "__main__":
    banner()
    args = get_args()
    domain = args.domain
    secure = args.secure
    bruteforce = args.bruteforce
    upgrade = args.upgrade
    install = args.install
    ports = args.ports
    vpn = args.vpn
    quick = args.quick
    bruteall = args.bruteall
    fresh = args.fresh
    notify = args.notify
    active = args.active
    if vpn is not False:
        vpncheck()
    if fresh is not False:
        os.system("rm -r output")
        newpath = r'output'
        os.makedirs(newpath)
    if install is not False:
        upgradeFiles()
    elif upgrade is not False:
        upgradeFiles()
    else:
        if domain is not False:
            if quick is not False:
                sublist3rBrute()
            elif bruteforce is not False:
                massdns()
                sublist3r()
                enumall()
                subdomainfile()
            else:
                sublist3r()
                enumall()
                knockpy()
                subdomainfile()
        if notify is not False:
            notified()
        else:
            print("\nPlease provide a domain. Ex. -d example.com")
    print("\n\033[1;34mAll your subdomain are belong to us\033[1;37m")
