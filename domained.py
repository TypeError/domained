#!/usr/bin/env python3

# #Domain name enumeration tool that leverages awesome tools:
#     - Sublist3r by Ahmed Aboul-Ela (https://github.com/aboul3la/Sublist3r)
#     - enumall by Jason Haddix (https://github.com/jhaddix/domain)
#     - Knock by Gianni Amato (https://github.com/guelfoweb/knock)
#     - Subbrute by TheRook (https://github.com/TheRook/subbrute)
#     - massdns by B. Blechschmidt (https://github.com/blechschmidt/massdns)
#     - Amass by Jeff by Foley (https://github.com/OWASP/Amass)
#     - SubFinder by Ice3man543 (https://github.com/subfinder/subfinder)
#     - Recon-ng by Tim Tomes (LaNMaSteR53) (https://bitbucket.org/LaNMaSteR53/recon-ng)
#     - EyeWitness by ChrisTruncer (https://github.com/FortyNorthSecurity/EyeWitness)
#     - SecList (DNS Recon List) by Daniel Miessler (https://github.com/danielmiessler/SecLists)
#     - LevelUp All.txt Subdomain List by Jason Haddix

# # Github - https://github.com/cakinney (Caleb Kinney)

import argparse
import configparser
import colorama
import csv
import datetime
import glob
import os
import requests
import smtplib
import time
from signal import signal, alarm, SIGALRM
from installer import upgradeFiles
from color import error, info, debug, warning, colored
from shutil import which

colorama.init()
today = datetime.date.today()


def get_args():
    parser = argparse.ArgumentParser(description="domained")
    parser.add_argument(
        "-d", "--domain", type=str, help="Domain", required=False, default=False
    )
    parser.add_argument(
        "-s",
        "--secure",
        help="Secure",
        action="store_true",
        required=False,
        default=False,
    )
    parser.add_argument(
        "-b", "--bruteforce", help="Bruceforce", action="store_true", default=False
    )
    parser.add_argument("--upgrade", help="Upgrade", action="store_true", default=False)
    parser.add_argument("--install", help="Install", action="store_true", default=False)
    parser.add_argument("--vpn", help="VPN Check", action="store_true", default=False)
    parser.add_argument(
        "-p", "--ports", help="Ports", action="store_true", default=False
    )
    parser.add_argument(
        "-q", "--quick", help="Quick", action="store_true", default=False
    )
    parser.add_argument(
        "--bruteall", help="Bruteforce JHaddix All", action="store_true", default=False
    )
    parser.add_argument(
        "--fresh", help="Remove output Folder", action="store_true", default=False
    )
    parser.add_argument(
        "--notify",
        help="Notify when script completed",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "--active", help="EyeWitness Active Scan", action="store_true", default=False
    )
    parser.add_argument(
        "--noeyewitness", help="No EyeWitness", action="store_true", default=False
    )

    return parser.parse_args()


newpath = r"output"
if not os.path.exists(newpath):
    os.makedirs(newpath)


def banner():
    warning(
        """
         ___/ /__  __ _  ___ _(_)__  ___ ___/ /
        / _  / _ \/  ' \/ _ `/ / _ \/ -_) _  /
        \_,_/\___/_/_/_/\_,_/_/_//_/\__/\_,_/
    {}\t\t\tgithub.com/cakinney{}""".format(
            colorama.Fore.BLUE, colorama.Style.RESET_ALL
        )
    )
    globpath = "*.csv"
    globpath2 = "*.lst"
    if (next(glob.iglob(globpath), None)) or (next(glob.iglob(globpath2), None)):
        info("\nThe following files may be left over from failed domained attempts:")
        for file in glob.glob(globpath):
            info("  - {}".format(file))
        for file in glob.glob(globpath2):
            info("  - {}".format(file))
        signal(SIGALRM, lambda x: 1 / 0)
        try:
            alarm(5)
            RemoveQ = input("\nWould you like to remove the files? [y/n]: ")
            if RemoveQ.lower() == "y":
                os.system("rm *.csv")
                os.system("rm *.lst")
                info("\nFiles removed\nStarting domained...")
                time.sleep(5)
            else:
                info("\nThank you.\nPlease wait...")
                time.sleep(1)
        except:
            info("\n\nStarting domained...")


def sublist3r(brute=False):
    info("\n\nRunning Sublist3r \n")
    sublist3rFileName = "{}_sublist3r.txt".format(output_base)
    Subcmd = "python {} -v -t 15 {} -d {} -o {}".format(
        os.path.join(script_path, "bin/Sublist3r/sublist3r.py"),
        "-b" if brute else "",
        domain,
        sublist3rFileName,
    )
    debug("\nRunning Command: {}".format(Subcmd))
    os.system(Subcmd)
    info("\nSublist3r Complete")
    time.sleep(1)
    if brute:
        eyewitness(sublist3rFileName)


def enumall():
    info("\n\nRunning Enumall \n")
    enumallCMD = "python {} {}".format(
        os.path.join(script_path, "bin/domain/enumall.py"), domain
    )
    debug("\nRunning Command: {}".format(enumallCMD))
    os.system(enumallCMD)
    info("\nenumall Complete")
    time.sleep(1)


def massdns():
    info("\n\nRunning massdns \n")
    word_file = os.path.join(
        script_path, "bin/sublst/all.txt" if bruteall else "bin/sublst/sl-domains.txt"
    )
    massdnsCMD = "python {} {} {} | {} -r resolvers.txt -t A -o S -w {}-massdns.txt".format(
        os.path.join(script_path, "bin/subbrute/subbrute.py"),
        word_file,
        domain,
        os.path.join(script_path, "bin/massdns/bin/massdns"),
        output_base,
    )
    debug("\nRunning Command: {}".format(massdnsCMD))
    os.system(massdnsCMD)
    info("\nMasscan Complete")
    time.sleep(1)


def knockpy():
    info("\n\nRunning Knock \n")
    knockpyCmd = "python {} -c {}".format(
        os.path.join(script_path, "bin/knockpy/knockpy/knockpy.py"), domain
    )
    debug("\nRunning Command:  {}".format(knockpyCmd))
    os.system(knockpyCmd)
    rootdomainStrip = domain.replace(".", "_")
    knockpyFilenameInit = "{}_knock.csv".format(output_base)
    os.system("mv {}* {}".format(rootdomainStrip, knockpyFilenameInit))
    time.sleep(1)
    knockpySubs = []
    try:
        with open(knockpyFilenameInit, "rt") as f:
            reader = csv.reader(f, delimiter=",")
            for row in reader:
                knockpySubs.append(row[3])
        filenameKnocktxt = "{}.txt".format(knockpyFilenameInit)
        f1 = open(filenameKnocktxt, "w")
        for hosts in knockpySubs:
            hosts = "".join(hosts)
            f1.writelines("\n" + hosts)
        f1.close()
    except:
        error("\nKnock File Error\n")
    time.sleep(1)


def check_gopath(cmd, install_repo):
    if os.environ["GOPATH"]:
        execs = os.listdir(os.path.join(os.environ["GOPATH"], "bin"))
    if cmd in execs:
        warning(
            "\nFound '{}' in your $GOPATH/bin folder please add this to your $PATH".format(
                cmd
            )
        )
    else:
        ans = input(
            "\n{}{} does not appear to be installed, would you like to run `go get -u -v {}`? [y/N]{}".format(
                colorama.Fore.RED, cmd, install_repo, colorama.Style.RESET_ALL
            )
        )

        if ans.lower() == "y":
            info("\nInstalling {}".format(install_repo))
            os.system("go get -u -v {}".format(install_repo))
            return True


def amass(rerun=0):
    if which("amass"):
        info("\n\nRunning Amass \n")
        amassFileName = "{}_amass.txt".format(output_base)
        amassCmd = "amass enum -d {} -o {}".format(domain, amassFileName)
        debug("\nRunning Command: {}".format(amassCmd))
        os.system(amassCmd)
        info("\nAmass Complete")
        time.sleep(1)
    else:
        warning("\n\nmass is not currently in your $PATH \n")
        if check_gopath("amass", "github.com/OWASP/Amass/...") and rerun != 1:
            amass(rerun=1)


def subfinder(rerun=0):
    if which("subfinder"):
        info("\n\nRunning Subfinder \n")
        subfinderFileName = "{}_subfinder.txt".format(output_base)
        subfinderCmd = "subfinder -d {} -o {}".format(domain, subfinderFileName)
        debug("\nRunning Command: {}".format(subfinderCmd))
        os.system(subfinderCmd)
        info("\nsubfinder Complete")
        time.sleep(1)
    else:
        warning("\n\nubfinder is not currently in your $PATH \n")
        if check_gopath("subfinder", "github.com/subfinder/subfinder") and rerun != 1:
            subfinder(rerun=1)


def eyewitness(filename):
    info("\n\nRunning EyeWitness  \n")
    EWHTTPScriptIPS = "python {} -f {} {} --no-prompt --web  -d {}-{}-EW".format(
        os.path.join(script_path, "bin/EyeWitness/EyeWitness.py"),
        filename,
        "--active-scan" if active else "",
        output_base,
        time.strftime("%m-%d-%y-%H-%M"),
    )
    if vpn:
        info(
            "\nIf not connected to VPN manually run the following command on reconnect:\n{}".format(
                EWHTTPScriptIPS
            )
        )
        vpncheck()
    debug("\nRunning Command: {}".format(EWHTTPScriptIPS))
    os.system(EWHTTPScriptIPS)
    print("\a")


def writeFiles(name):
    """Writes info of all hosts from subhosts
    """
    subdomainCounter = 0
    subdomainAllFile = "{}-all.txt".format(output_base)
    fileExt = {
        "sublist3r": ".txt",
        "knock": ".csv.txt",
        "enumall": ".lst",
        "massdns": ".txt",
        "amass": ".txt",
        "subfinder": ".txt",
    }
    fileName = output_base + "_" + name + fileExt[name]

    debug("\n Opening %s File" % name)
    try:
        with open(fileName, "r") as f:
            SubHosts = f.read().splitlines()

        with open(subdomainAllFile, "a") as f:
            f.writelines("\n\n" + name)
            for hosts in SubHosts:
                hosts = "".join(hosts)
                f.writelines("\n" + hosts)
                subdomainCounter = subdomainCounter + 1
        os.remove(fileName)
        info("\n{} Subdomains discovered by {}".format(subdomainCounter, name))
    except:
        error("\nError Opening %s File!\n" % name)
    return subdomainCounter


def subdomainfile():
    subdomainAllFile = "{}-all.txt".format(output_base)
    names = ["sublist3r", "knock", "enumall", "massdns", "amass", "subfinder"]

    for name in names:
        writeFiles(name)

    debug("\nCombining Domains Lists\n")
    with open(subdomainAllFile, "r") as domainList:
        uniqueDomains = set(domainList)
        domainList.close()
        subdomainUniqueFile = "{}-unique.txt".format(output_base)
        uniqueDomainsOut = open(subdomainUniqueFile, "w")
        for domains in uniqueDomains:
            domains = domains.replace("\n", "")
            if domains.endswith(domain):
                uniqueDomainsOut.writelines("https://{}\n".format(domains))
                if ports is not False:
                    uniqueDomainsOut.writelines("https://{}:8443\n".format(domains))
                if secure is False:
                    uniqueDomainsOut.writelines("http://{}\n".format(domains))
                    if ports is not False:
                        uniqueDomainsOut.writelines("http://{}:8080\n".format(domains))
    time.sleep(1)
    rootdomainStrip = domain.replace(".", "_")
    info("\nCleaning Up Old Files\n")
    try:
        os.system("rm {}*".format(domain))
        os.system("rm {}*".format(rootdomainStrip))
    except:
        error("\nError Removing Files!\n")
    if not noeyewitness:
        eyewitness(subdomainUniqueFile)


def vpncheck():
    vpnck = requests.get("https://ifconfig.co/json")
    # Change "City" to your city")
    if "City" in vpnck.text:
        warning("\nNot connected via VPN ")
        warning("\n{}".format(vpnck.content))
        warning("\nQuitting domained... ")
        quit()
    else:
        info("\nConnected via VPN ")
        info("\n{}".format(vpnck.content))
        time.sleep(5)


def notified():
    notifySub = "domained Script Finished"
    notifyMsg = "domained Script Finished for {}".format(domain)
    Config = configparser.ConfigParser()
    Config.read(os.path.join(script_path, "ext/notifycfg.ini"))
    if (Config.get("Pushover", "enable")) == "True":
        poToken = Config.get("Pushover", "token")
        poUser = Config.get("Pushover", "user")
        if "device" in Config.options("Pushover"):
            poDevice = Config.get("Pushover", "device")
            poRequestPayload = {
                "token": poToken,
                "user": poUser,
                "device": poDevice,
                "title": notifySub,
                "message": notifyMsg,
            }
        else:
            poRequestPayload = {
                "token": poToken,
                "user": poUser,
                "title": notifySub,
                "message": notifyMsg,
            }
            poValidatePayload = {"token": poToken, "user": poUser}
            poValidate = requests.post(
                "https://api.pushover.net/1/users/validate.json",
                data=(poValidatePayload),
            )
            poJsonV = poValidate.json()
            if poJsonV["status"] == 1:
                info("\nPushover Account Validated\n")
                poRequest = requests.post(
                    "https://api.pushover.net/1/messages.json", data=(poRequestPayload)
                )
                poJsonR = poRequest.json()
                if poJsonV["status"] == 1:
                    info("\nPushover Account Notified\n")
                else:
                    error("\nError - Pushover Account Not Notified\n")
            else:
                error("\nError - Pushover Account Not Validated\n")
    if (Config.get("Email", "enable")) == "True":
        gmailUser = Config.get("Email", "user")
        gmailPass = Config.get("Email", "password")
        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(gmailUser, gmailPass)
            subject = "domained Script Complete"
            text = "domained Script Complete for " + domain
            msg = "Subject: {}\n\n{}".format(subject, text)
            server.sendmail(gmailUser, gmailUser, msg)
            server.quit()
            info("\nEmail Notification Sent\n")
        except:
            error("\nError - Email Notification Not Sent\n")


def options():
    if vpn:
        vpncheck()
    if fresh:
        os.system("rm -r output")
        newpath = r"output"
        os.makedirs(newpath)
    if install or upgrade:
        upgradeFiles()
    else:
        if domain:
            if quick:
                amass()
                subfinder()
            elif bruteforce:
                massdns()
                sublist3r()
                enumall()
                amass()
                subfinder()
            else:
                sublist3r(True)
                enumall()
                knockpy()
                amass()
                subfinder()
            subdomainfile()
            if notify:
                notified()
        else:
            warning("\nPlease provide a domain. Ex. -d example.com")
    colored("\nAll your subdomain are belong to us", colorama.Fore.BLUE)


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
    options()
