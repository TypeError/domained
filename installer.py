import os
import time
import subprocess


SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))


def upgradeFiles():
    """Upgrade all the required files
    """
    binpath = os.path.join(SCRIPT_PATH, "bin")
    old_wd = os.getcwd()
    if not os.path.exists(binpath):
        os.makedirs(binpath)
    else:
        print("Removing old bin directory: {}".format(binpath))
        os.system("rm -rf {}".format(binpath))
        os.makedirs(binpath)
    print("Changing into domained home: {}".format(SCRIPT_PATH))
    os.chdir(SCRIPT_PATH)
    unameChk = subprocess.check_output(["uname", "-am"]).decode("utf-8")

    if "kali" not in unameChk:
        print("\n\033[1;31mKali Linux Recommended!\033[1;37m")
        time.sleep(1)

    sublist3rUpgrade = (
        "git clone https://github.com/aboul3la/Sublist3r.git ./bin/Sublist3r"
    )
    print("\n\033[1;31mInstalling Sublist3r \033[1;37m")
    os.system(sublist3rUpgrade)
    subInstallReq = "pip install -r bin/Sublist3r/requirements.txt"
    os.system(subInstallReq)
    print("Sublist3r Installed\n")

    eyeWitnessUpgrade = "git clone https://github.com/FortyNorthSecurity/EyeWitness.git ./bin/EyeWitness"
    print("\n\033[1;31mInstalling EyeWitness \033[1;37m" + eyeWitnessUpgrade)
    os.system(eyeWitnessUpgrade)
    eyeInstallReq = "bash bin/EyeWitness/setup/setup.sh"
    print("\n\033[1;31mRunning Command: \033[1;37m")
    os.system(eyeInstallReq)
    cpphantomjs = "cp phantomjs ./bin/EyeWitness/bin/"
    os.system(cpphantomjs)
    movephantomjs = "mv phantomjs bin/"
    os.system(movephantomjs)
    print("\nEyeWitness Installed\n")

    enumallUpgrade = "git clone https://github.com/jhaddix/domain.git ./bin/domain"
    print("\n\033[1;31mInstalling Enumall \033[1;37m")
    print("\nenumall Installed\n")
    os.system(enumallUpgrade)

    knockpyUpgrade = "git clone https://github.com/guelfoweb/knock.git ./bin/knockpy"
    print("\n\033[1;31mInstalling Knock \033[1;37m")
    os.system(knockpyUpgrade)
    print("\nKnockpy Installed\n")

    sublstUpgrade = "git clone https://gist.github.com/jhaddix/86a06c5dc309d08580a018c66354a056 ./bin/sublst"
    print("\n\033[1;31mCopying JHaddix All Domain List: \033[1;37m")
    print("\nJHaddix All Domain List Installed\n")
    os.system(sublstUpgrade)
    SLsublstUpgrade = "wget -O ./bin/sublst/sl-domains.txt https://raw.githubusercontent.com/\
    danielmiessler/SecLists/master/Discovery/DNS/sortedcombied-knock-dnsrecon-fierce-reconng.txt"
    print("\n\033[1;31mCopying SecList Domain List \033[1;37m")
    print("\nSecList Domain List Installed\n")
    os.system(SLsublstUpgrade)

    subbruteUpgrade = "git clone https://github.com/TheRook/subbrute.git ./bin/subbrute"
    print("\n\033[1;31mInstalling Subbrute \033[1;37m")
    os.system(subbruteUpgrade)
    print("\nSubbrute Installed\n")

    amassUpgrade = "go get -u github.com/OWASP/Amass/..."
    print("\n\033[1;31mInstalling Amass \033[1;37m")
    os.system(amassUpgrade)
    subfinderUpgrade = "go get -u github.com/subfinder/subfinder"
    print("\n\033[1;31mInstalling Subfinder \033[1;37m")
    os.system(subfinderUpgrade)
    massdnsUpgrade = "git clone --branch v0.2 --single-branch https://github.com/blechschmidt/massdns ./bin/massdns"
    print("\n\033[1;31mInstalling massdns \033[1;37m")
    os.system(massdnsUpgrade)
    massdnsMake = "make -C ./bin/massdns"
    os.system(massdnsMake)
    print("\nMassdns Installed\n")
    os.system("cp ./bin/subbrute/resolvers.txt ./")

    if "kali" in unameChk:
        reconNGInstall = "apt-get install recon-ng"
        print("\n\033[1;31mInstalling Recon-ng \033[1;37m")
        os.system(reconNGInstall)
        print("\nRecon-ng Installed\n")
    else:
        print("Please install Recon-ng - https://bitbucket.org/LaNMaSteR53/")

    print("\n\033[1;31mAll tools installed \033[1;37m")
    print("Changing back to old working directory: {}".format(old_wd))
    os.chdir(old_wd)
