import os
import time
import subprocess
from color import info, debug, warning, colored

SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))


def upgradeFiles():
    """Upgrade all the required files
    """
    binpath = os.path.join(SCRIPT_PATH, "bin")
    old_wd = os.getcwd()
    if not os.path.exists(binpath):
        os.makedirs(binpath)
    else:
        debug("Removing old bin directory: {}".format(binpath))
        os.system("rm -rf {}".format(binpath))
        os.makedirs(binpath)
    info("Changing into domained home: {}".format(SCRIPT_PATH))
    os.chdir(SCRIPT_PATH)
    unameChk = subprocess.check_output(["uname", "-am"]).decode("utf-8")

    if "kali" not in unameChk:
        warning("\nKali Linux Recommended!")
        warning("Please install ldns (https://www.nlnetlabs.nl/documentation/ldns, 'apt install libldns-dev') and Go (https://golang.org, 'apt install golang')")
        time.sleep(3)
    else:
        dependenciesInstall = "apt install libldns-dev golang"
        info("\nInstalling dependencies (ldns, Go) ")
        os.system(dependenciesInstall)
        info("\nDependencies Installed\n")

    sublist3rUpgrade = (
        "git clone https://github.com/aboul3la/Sublist3r.git ./bin/Sublist3r"
    )
    info("\nInstalling Sublist3r ")
    os.system(sublist3rUpgrade)
    subInstallReq = "pip install -r bin/Sublist3r/requirements.txt"
    os.system(subInstallReq)
    info("Sublist3r Installed\n")

    eyeWitnessUpgrade = "git clone https://github.com/FortyNorthSecurity/EyeWitness.git ./bin/EyeWitness"
    info("\nInstalling EyeWitness" + eyeWitnessUpgrade)
    os.system(eyeWitnessUpgrade)
    eyeInstallReq = "bash bin/EyeWitness/setup/setup.sh"
    debug("\nRunning Command: ")
    os.system(eyeInstallReq)
    info("\nEyeWitness Installed\n")

    enumallUpgrade = "git clone https://github.com/jhaddix/domain.git ./bin/domain"
    info("\nInstalling Enumall ")
    info("\nenumall Installed\n")
    os.system(enumallUpgrade)

    knockpyUpgrade = "git clone https://github.com/guelfoweb/knock.git ./bin/knockpy"
    info("\nInstalling Knock ")
    os.system(knockpyUpgrade)
    info("\nKnockpy Installed\n")

    sublstUpgrade = "git clone https://gist.github.com/jhaddix/86a06c5dc309d08580a018c66354a056 ./bin/sublst"
    info("\nCopying JHaddix All Domain List: ")
    info("\nJHaddix All Domain List Installed\n")
    os.system(sublstUpgrade)
    SLsublstUpgrade = "wget -O ./bin/sublst/sl-domains.txt https://github.com/danielmiessler/SecLists/raw/master/Discovery/DNS/sortedcombined-knock-dnsrecon-fierce-reconng.txt"
    info("\nCopying SecList Domain List ")
    info("\nSecList Domain List Installed\n")
    os.system(SLsublstUpgrade)

    subbruteUpgrade = "git clone https://github.com/TheRook/subbrute.git ./bin/subbrute"
    info("\nInstalling Subbrute ")
    os.system(subbruteUpgrade)
    info("\nSubbrute Installed\n")

    amassUpgrade = "GO111MODULE=on go get -v -u github.com/OWASP/Amass/v3/..."
    info("\nInstalling Amass ")
    os.system(amassUpgrade)
    subfinderUpgrade = "GO111MODULE=on go get -u -v github.com/projectdiscovery/subfinder/cmd/subfinder"
    info("\nInstalling Subfinder ")
    os.system(subfinderUpgrade)
    massdnsUpgrade = "git clone --branch v0.2 --single-branch https://github.com/blechschmidt/massdns ./bin/massdns"
    info("\nInstalling massdns ")
    os.system(massdnsUpgrade)
    massdnsMake = "make -C ./bin/massdns"
    os.system(massdnsMake)
    info("\nMassdns Installed\n")
    os.system("cp ./bin/subbrute/resolvers.txt ./")

    if "kali" in unameChk:
        reconNGInstall = "apt-get install recon-ng"
        info("\nInstalling Recon-ng ")
        os.system(reconNGInstall)
        info("\nRecon-ng Installed\n")
    else:
        info("Please install Recon-ng - https://bitbucket.org/LaNMaSteR53/")

    info("\nAll tools installed ")
    debug("Changing back to old working directory: {}".format(old_wd))
    os.chdir(old_wd)
