#!/usr/bin/env python3

# #Domain name enumeration tool that leverages awesome tools:
#     - Sublist3r by Ahmed Aboul-Ela (https://github.com/aboul3la/Sublist3r)
#     - enumall by Jason Haddix (https://github.com/jhaddix/domain)
#     - Knock by Gianni Amato (https://github.com/guelfoweb/knock)
#     - Subbrute by TheRook (https://github.com/TheRook/subbrute)
#     - massdns by B. Blechschmidt (https://github.com/blechschmidt/massdns)
#     - Amass by Jeff Foley (https://github.com/caffix/amass)
#     - Recon-ng by Tim Tomes (LaNMaSteR53) (https://bitbucket.org/LaNMaSteR53/recon-ng)
#     - EyeWitness by ChrisTruncer (https://github.com/ChrisTruncer/EyeWitness)
#     - SecList (DNS Recon List) by Daniel Miessler (https://github.com/danielmiessler/SecLists)
#     - LevelUp All.txt Subdomain List by Jason Haddix

# # Github - https://github.com/cakinney (Caleb Kinney)

import argparse, os, requests, time, csv, datetime, glob, subprocess
import configparser, smtplib
from signal import signal, alarm, SIGALRM

today = datetime.date.today()


def get_args():
    parser = argparse.ArgumentParser(
        description='domained')
    parser.add_argument(
        '-d', '--domain', type=str, help='Domain', required=False, default=False)
    parser.add_argument(
        '-s', '--secure', help='Secure', action='store_true', required=False, default=False)
    parser.add_argument(
        '-b', '--bruteforce', help='Bruceforce', action='store_true', default=False)
    parser.add_argument(
        '--upgrade', help='Upgrade', action='store_true', default=False)
    parser.add_argument(
        '--install', help='Install', action='store_true', default=False)
    parser.add_argument(
        '--vpn', help='VPN Check', action='store_true', default=False)
    parser.add_argument(
        '-p', '--ports', help='Ports', action='store_true', default=False)
    parser.add_argument(
        '-q', '--quick', help='Quick', action='store_true', default=False)
    parser.add_argument(
        '--bruteall', help='Bruteforce JHaddix All', action='store_true', default=False)
    parser.add_argument(
        '--fresh', help='Remove output Folder', action='store_true', default=False)
    parser.add_argument(
        '--notify', help='Notify when script completed', nargs='?', default=False)
    parser.add_argument(
        '--active', help='EyeWitness Active Scan', action='store_true', default=False)
    parser.add_argument(
        '--noeyewitness', help='No EyeWitness', action='store_true', default=False)

    return parser.parse_args()


newpath = r'output'
if not os.path.exists(newpath):
    os.makedirs(newpath)


def banner():
    print("""\033[1;31m
         ___/ /__  __ _  ___ _(_)__  ___ ___/ /
        / _  / _ \/  ' \/ _ `/ / _ \/ -_) _  /
        \_,_/\___/_/_/_/\_,_/_/_//_/\__/\_,_/
    \033[1;34m\t\t\tgithub.com/cakinney\033[1;m""")
    globpath = ("*.csv")
    globpath2 = ("*.lst")
    if (next(glob.iglob(globpath), None)) or (next(glob.iglob(globpath2), None)):
        print("\nThe following files may be left over from failed domained attempts:")
        for file in glob.glob(globpath):
            print("  - {}".format(file))
        for file in glob.glob(globpath2):
            print("  - {}".format(file))
        signal(SIGALRM, lambda x: 1 / 0)
        try:
            alarm(5)
            RemoveQ = input("\nWould you like to remove the files? [y/n]: ")
            if RemoveQ.lower() == "y":
                os.system("rm *.csv")
                os.system("rm *.lst")
                print("\nFiles removed\nStarting domained...")
                time.sleep(5)
            else:
                print("\nThank you.\nPlease wait...")
                time.sleep(1)
        except:
            print("\n\nStarting domained...")


def sublist3r(brute=False):
    print("\n\n\033[1;31mRunning Sublist3r \n\033[1;37m")
    sublist3rFileName = "{}_sublist3r.txt".format(output_base)
    Subcmd = "python {} -v -t 15 {} -d {} -o {}".format(
        os.path.join(script_path, 'bin/Sublist3r/sublist3r.py'),
        '-b' if brute else '', domain, sublist3rFileName)
    print("\n\033[1;31mRunning Command: \033[1;37m{}".format(Subcmd))
    os.system(Subcmd)
    print("\n\033[1;31mSublist3r Complete\033[1;37m")
    time.sleep(1)
    if brute:
        eyewitness(sublist3rFileName)


def enumall():
    print("\n\n\033[1;31mRunning Enumall \n\033[1;37m")
    enumallCMD = "python {} {}".format(
        os.path.join(script_path, 'bin/domain/enumall.py'), domain)
    print("\n\033[1;31mRunning Command: \033[1;37m{}".format(enumallCMD))
    os.system(enumallCMD)
    print("\n\033[1;31menumall Complete\033[1;37m")
    time.sleep(1)


def massdns():
    print("\n\n\033[1;31mRunning massdns \n\033[1;37m")
    word_file = os.path.join(script_path, 'bin/sublst/all.txt' if bruteall else 'bin/sublst/sl-domains.txt')
    massdnsCMD = 'python {} -s {} {} | {} -r resolvers.txt -t A -a -o -w {}-massdns.txt -'.format(
        os.path.join(script_path, 'bin/subbrute/subbrute.py'), word_file, domain,
        os.path.join(script_path, 'bin/massdns/bin/massdns'), output_base)
    print("\n\033[1;31mRunning Command: \033[1;37m{}".format(massdnsCMD))
    os.system(massdnsCMD)
    print("\n\033[1;31mMasscan Complete\033[1;37m")
    time.sleep(1)


def knockpy():
    print("\n\n\033[1;31mRunning Knock \n\033[1;37m")
    knockpyCmd = "python {} -c {}".format(
        os.path.join(script_path, 'bin/knockpy/knockpy/knockpy.py'), domain)
    print("\n\033[1;31mRunning Command: \033[1;37m {}".format(knockpyCmd))
    os.system(knockpyCmd)
    rootdomainStrip = domain.replace(".", "_")
    knockpyFilenameInit = "{}_knock.csv".format(output_base)
    os.system("mv {}* {}".format(rootdomainStrip, knockpyFilenameInit))
    time.sleep(1)
    knockpySubs = []
    try:
        with open(knockpyFilenameInit, 'rb') as f:
            reader = csv.reader(f, delimiter=',')
            for row in reader:
                knockpySubs.append(row[3])
        filenameKnocktxt = "{}.txt".format(knockpyFilenameInit)
        f1 = open(filenameKnocktxt, "w")
        for hosts in knockpySubs:
            hosts = "".join(hosts)
            f1.writelines("\n" + hosts)
        f1.close()
    except:
        print("\nKnock File Error\n")
    time.sleep(1)


def amass():
    print("\n\n\033[1;31mRunning Amass \n\033[1;37m")
    amassFileName = "{}_amass.txt".format(output_base)
    amassCmd = "~/go/bin/amass -d {} -o {}".format(domain, amassFileName)
    print("\n\033[1;31mRunning Command: \033[1;37m{}".format(amassCmd))
    os.system(amassCmd)
    print("\n\033[1;31mAmass Complete\033[1;37m")
    time.sleep(1)

def subfinder():
    print("\n\n\033[1;31mRunning Subfinder \n\033[1;37m")
    subfinderFileName = "{}_subfinder.txt".format(output_base)
    subfinderCmd = "/root/go/bin/subfinder -d {} -o {}".format(domain, subfinderFileName)
    print("\n\033[1;31mRunning Command: \033[1;37m{}".format(subfinderCmd))
    os.system(subfinderCmd)
    print("\n\033[1;31msubfinder Complete\033[1;37m")
    time.sleep(1)

def eyewitness(filename):
    print("\n\n\033[1;31mRunning EyeWitness  \n\033[1;37m")
    EWHTTPScriptIPS = "python {} -f {} {} --no-prompt --headless  -d {}-{}-EW".format(
        os.path.join(script_path, 'bin/EyeWitness/EyeWitness.py'), filename,
        '--active-scan' if active else '',
        output_base, time.strftime('%m-%d-%y-%H-%M'))
    if vpn:
        print(
            "\n\033[1;31mIf not connected to VPN manually run the following command on reconnect:\n\033[1;37m{}".format(
                EWHTTPScriptIPS))
        vpncheck()
    print("\n\033[1;31mRunning Command: \033[1;37m{}".format(EWHTTPScriptIPS))
    os.system(EWHTTPScriptIPS)
    print("\a")


def upgradeFiles():
    binpath = os.path.join(script_path, 'bin')
    old_wd = os.getcwd()
    if not os.path.exists(binpath):
        os.makedirs(binpath)
    else:
        print("Removing old bin directory: {}".format(binpath))
        os.system('rm -rf {}'.format(binpath))
        os.makedirs(binpath)
    print('Changing into domained home: {}'.format(script_path))
    os.chdir(script_path)
    unameChk = str(subprocess.check_output(['uname', '-am']))
    if "kali" not in unameChk:
        print("\n\033[1;31mKali Linux Recommended!\033[1;37m")
        time.sleep(1)
    sublist3rUpgrade = ("git clone https://github.com/aboul3la/Sublist3r.git ./bin/Sublist3r")
    print("\n\033[1;31mInstalling Sublist3r \033[1;37m")
    os.system(sublist3rUpgrade)
    subInstallReq = ("pip install -r bin/Sublist3r/requirements.txt")
    os.system(subInstallReq)
    print("Sublist3r Installed\n")
    eyeWitnessUpgrade = ("git clone https://github.com/ChrisTruncer/EyeWitness.git ./bin/EyeWitness")
    print("\n\033[1;31mInstalling EyeWitness \033[1;37m" + eyeWitnessUpgrade)
    os.system(eyeWitnessUpgrade)
    eyeInstallReq = ("bash bin/EyeWitness/setup/setup.sh")
    print("\n\033[1;31mRunning Command: \033[1;37m")
    os.system(eyeInstallReq)
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
        "wget -O ./bin/sublst/sl-domains.txt https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/DNS/sortedcombied-knock-dnsrecon-fierce-reconng.txt")
    print("\n\033[1;31mCopying SecList Domain List \033[1;37m")
    print("\nSecList Domain List Installed\n")
    os.system(SLsublstUpgrade)
    subbruteUpgrade = ("git clone https://github.com/TheRook/subbrute.git ./bin/subbrute")
    print("\n\033[1;31mInstalling Subbrute \033[1;37m")
    os.system(subbruteUpgrade)
    print("\nSubbrute Installed\n")
    amassUpgrade = ("go get -u github.com/caffix/amass")
    print("\n\033[1;31mInstalling Amass \033[1;37m")
    os.system(amassUpgrade)
    subfinderUpgrade = ("go get -u github.com/subfinder/subfinder")
    print("\n\033[1;31mInstalling Subfinder \033[1;37m")
    os.system(subfinderUpgrade)
    massdnsUpgrade = ("git clone --branch v0.2 --single-branch https://github.com/blechschmidt/massdns ./bin/massdns")
    print("\n\033[1;31mInstalling massdns \033[1;37m")
    os.system(massdnsUpgrade)
    massdnsMake = ("make -C ./bin/massdns")
    os.system(massdnsMake)
    print("\nMassdns Installed\n")
    os.system("cp ./bin/subbrute/resolvers.txt ./")
    if "kali" in unameChk:
        reconNGInstall = ("apt-get install recon-ng")
        print("\n\033[1;31mInstalling Recon-ng \033[1;37m")
        os.system(reconNGInstall)
        print("\nRecon-ng Installed\n")
    else:
        print("Please install Recon-ng - https://bitbucket.org/LaNMaSteR53/")
    print("\n\033[1;31mAll tools installed \033[1;37m")
    print('Changing back to old working directory: {}'.format(old_wd))
    os.chdir(old_wd)


def subdomainfile():
    sublist3rFileName = "{}_sublist3r.txt".format(output_base)
    enumallFileName = "{}.lst".format(domain)
    subdomainAllFile = "{}-all.txt".format(output_base)
    knockpyFileName = "{}_knock.csv.txt".format(output_base)
    massdnsFileName = "{}-massdns.txt".format(output_base)
    amassFileName = "{}_amass.txt".format(output_base)
    subfinderFileName = "{}_subfinder.txt".format(output_base)
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
        print("\n{} Subdomains discovered by Sublist3r".format(subdomainCounter))
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
        print("\n{} Subdomains discovered by Enumall".format(subdomainCounter))
    except:
        print("\nError Opening Enumall File!\n")
    print("\nOpening Knock File\n")
    try:
        with open(knockpyFileName) as f:
            SubHosts = f.read().splitlines()
        f.close()
        time.sleep(1)
        subdomainCounter = 0
        f1 = open(subdomainAllFile, "a")
        f1.writelines("\n\nknock")
        for hosts in SubHosts:
            hosts = "".join(hosts)
            f1.writelines("\n{}".format(hosts))
            subdomainCounter = subdomainCounter + 1
        f1.close()
        knockpyFileNamecsv = "{}_knock.csv".format(output_base)
        os.remove(knockpyFileName)
        os.remove(knockpyFileNamecsv)
        print("\n{} Subdomains discovered by Knock".format(subdomainCounter))
    except:
        print("\nError Opening Knock File!\n")
    print("\nOpening massdns File\n")
    try:
        with open(massdnsFileName) as f:
            SubHosts = f.read().splitlines()
        f.close()
        time.sleep(1)
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
        print("\n{} Subdomains discovered by massdns".format(subdomainCounter))
    except:
        print("\nError Opening massdns File!\n")
    print("\nOpening Amass File\n")
    try:
        with open(amassFileName) as f:
            SubHosts = f.read().splitlines()
        f.close()
        time.sleep(1)
        subdomainCounter = 0
        f1 = open(subdomainAllFile, "a")
        f1.writelines("\n\namass")
        for hosts in SubHosts:
            hosts = hosts.split(".	")[0]
            if domain in hosts:
                hosts = "".join(hosts)
                f1.writelines("\n" + hosts)
                subdomainCounter = subdomainCounter + 1
        f1.close()
        os.remove(amassFileName)
        print("\n{} Subdomains discovered by Amass".format(subdomainCounter))
    except:
        print("\nError Opening massdns File!\n")
    try:
        with open(subfinderFileName) as f:
            SubHosts = f.read().splitlines()
        f.close()
        time.sleep(2)
        subdomainCounter = 0
        f1 = open(subdomainAllFile, "a")
        f1.writelines("\n\nsubfinder")
        for hosts in SubHosts:
            hosts = "".join(hosts)
            f1.writelines("\n" + hosts)
            subdomainCounter = subdomainCounter + 1
        f1.close()
        os.remove(subfinderFileName)
        print("\n{} Subdomains discovered by Subfinder".format(subdomainCounter))
    except:
        print("\nError Opening Subfinder File!\n")
    print("\nCombining Domains Lists\n")
    domainList = open(subdomainAllFile, 'r')
    uniqueDomains = set(domainList)
    domainList.close()
    subdomainUniqueFile = "{}-unique.txt".format(output_base)
    uniqueDomainsOut = open(subdomainUniqueFile, 'w')
    for domains in uniqueDomains:
        domains = domains.replace('\n', '')
        if domains.endswith(domain):
            uniqueDomainsOut.writelines("https://{}\n".format(domains))
            if ports is not False:
                uniqueDomainsOut.writelines("https://{}:8443\n".format(domains))
            if secure is False:
                uniqueDomainsOut.writelines("http://{}\n".format(domains))
                if ports is not False:
                    uniqueDomainsOut.writelines("http://{}:8080\n".format(domains))
    uniqueDomainsOut.close()
    time.sleep(1)
    rootdomainStrip = domain.replace(".", "_")
    print("\nCleaning Up Old Files\n")
    try:
        os.system("rm {}*".format(domain))
        os.system("rm {}*".format(rootdomainStrip))
    except:
        print("\nError Removing Files!\n")
    if not noeyewitness:
        eyewitness(subdomainUniqueFile)


def vpncheck():
    vpnck = requests.get('https://ifconfig.co/json')
    # Change "Comcast" to your provider or City")
    if "Comcast" in vpnck.content:
        print("\n\033[1;31mNot connected via VPN \033[1;37m")
        print("\n{}".format(vpnck.content))
        print("\n\033[1;31mQuitting domained... \033[1;37m")
        quit()
    else:
        print("\n\033[1;31mConnected via VPN \033[1;37m")
        print("\n{}".format(vpnck.content))
        time.sleep(5)


def notified():
    notifySub = ("domained Script Finished")
    notifyMsg = "domained Script Finished for {}".format(domain)
    Config = ConfigParser.ConfigParser()
    Config.read(os.path.join(script_path, "ext/notifycfg.ini"))
    if (Config.get('Pushover', 'enable')) == "True":
        poToken = (Config.get('Pushover', 'token'))
        poUser = (Config.get('Pushover', 'user'))
        if "device" in Config.options('Pushover'):
            poDevice = (Config.get('Pushover', 'device'))
            poRequestPayload = {'token': poToken, 'user': poUser, 'device': poDevice, 'title': notifySub,
                                'message': notifyMsg}
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
    output_base = "output/{}".format(domain)
    script_path = os.path.dirname(os.path.realpath(__file__))
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
    noeyewitness = args.noeyewitness
    if vpn:
        vpncheck()
    if fresh:
        os.system("rm -r output")
        newpath = r'output'
        os.makedirs(newpath)
    if install:
        upgradeFiles()
    elif upgrade:
        upgradeFiles()
    else:
        if domain:
            if quick:
                sublist3r(True)
            elif bruteforce:
                massdns()
                sublist3r()
                enumall()
                amass()
                subdomainfile()
            else:
                sublist3r()
                enumall()
                knockpy()
                amass()
                subfinder()
                subdomainfile()
        if notify:
            notified()
        else:
            print("\nPlease provide a domain. Ex. -d example.com")
    print("\n\033[1;34mAll your subdomain are belong to us\033[1;37m")
