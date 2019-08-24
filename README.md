# domained
A domain name enumeration tool

**Gist:** Some ~~terrible~~ continually updated python code leveraging some awesome tools that I use for bug bounty reconnaissance. 

**The tools contained in domained requires Kali Linux (preferred) or Debian 7+ and Recon-ng** 

domained uses several subdomain enumeration tools and wordlists to create a unique list of subdomains that are passed to EyeWitness for reporting with categorized screenshots, server response headers and signature based default credential checking. *(resources are saved to ./bin and output is saved to ./output)*

##### Initial Install: 
* domained tools: `python3 domained.py --install`
* Python required modules: `sudo pip install -r ./ext/requirements.txt`
###### Other Dependencies: 
* [ldns](https://www.nlnetlabs.nl/documentation/ldns/) library for DNS programming:
    * `sudo apt-get install libldns-dev -y`
* [Go](https://golang.org) Programming Language: 
    * `sudo apt-get install golang`


**_NOTE: This is an active recon – only perform on applications that you have permission to test against._**

##### Tools leveraged:

###### Subdomain Enumeraton Tools:
1. [Sublist3r](https://github.com/aboul3la/Sublist3r) by Ahmed Aboul-Ela 
2. [enumall](https://github.com/jhaddix/domain) by Jason Haddix 
3. [Knock](https://github.com/guelfoweb/knock) by Gianni Amato 
4. [Subbrute](https://github.com/TheRook/subbrute) by TheRook 
5. [massdns](https://github.com/blechschmidt/massdns) by B. Blechschmidt
6. [Recon-ng](https://bitbucket.org/LaNMaSteR53/recon-ng) by Tim Tomes (LaNMaSteR53)
7. [Amass](https://github.com/OWASP/Amass) by Jeff Foley (caffix)
8. [SubFinder](https://github.com/subfinder/subfinder) by by Ice3man543

###### Reporting + Wordlists:
- [EyeWitness](https://github.com/FortyNorthSecurity/EyeWitness) by ChrisTruncer  
- [SecList](https://github.com/danielmiessler/SecLists) (DNS Recon List) by Daniel Miessler 
- [LevelUp All.txt Subdomain List](https://gist.github.com/jhaddix/86a06c5dc309d08580a018c66354a056) by Jason Haddix 

##### Usage
````
First Step:
Install Required Python Modules: sudo pip install -r ./ext/requirements.txt
Install Tools: sudo python3 domained.py --install

Example 1: python3 domained.py -d example.com
Uses subdomain example.com (Sublist3r (+subbrute), enumall, Knock, Amass, and SubFinder)

Example 2: python3 domained.py -d example.com -b -p --vpn
Uses subdomain example.com with seclist subdomain list bruteforcing (massdns, subbrute, Sublist3r, Amass, enumall, and SubFinder), adds ports 8443/8080 and checks if on VPN

Example 3: python3 domained.py -d example.com -b --bruteall
Uses subdomain example.com with large-all.txt bruteforcing (massdns, subbrute, Sublist3r, Amass, enumall and SubFinder)

Example 4: python3 domained.py -d example.com --quick
Uses subdomain example.com and only Amass and SubFinder

Example 5: python3 domained.py -d example.com --quick --notify
Uses subdomain example.com, only Amass and SubFinder and notification

Example 6: python3 domained.py -d example.com --noeyewitness
Uses subdomain example.com with no EyeWitness

Note: --bruteall must be used with the -b flag
````

Option | Description
------ | --- 
--install/--upgrade  |  Both do the same function – install all prerequisite tools
--vpn   |   Check if you are on VPN (update with your provider)
--quick |   Use ONLY Amass and SubFinder
--bruteall  |   Bruteforce with JHaddix All.txt List instead of SecList
--fresh  |   Delete old data from output folder
--notify  |   Send Pushover or Gmail Notifications
--active  |   EyeWitness Active Scan
--noeyewitness  |   No Eyewitness
-d  |   The domain you want to preform recon on
-b  |   Bruteforce with subbrute/massdns and SecList wordlist
-s n    |   Only HTTPs domains
-p  |   Add port 8080 for HTTP and 8443 for HTTPS 

##### Notifications
- Complete the ext/notifycfg.ini for Pushover or Gmail notifications. (*Enable must be set to True*)
- Please see the Pushover API info [here](https://pushover.net/api) and instructions on how to allow less secure apps on your gmail account [here](https://support.google.com/accounts/answer/6010255)

##### To-Do List
- [ ] Multiple Domains
- [x] ~~Notifications~~
- [ ] Subdomains from [censys](https://censys.io/)
- [ ] Subdomains from [Shodan](https://shodan.io/)
- [ ] Web Frontend/Dashboard
- [x] ~~Add SubFinder~~

##### Thank You to Contributors
* [ccsplit](https://github.com/ccsplit) - Multiple code improvements including the ability to run domained from any directory
* [jafoca](https://github.com/jafoca) - Massdns fix
* [mortymorty](https://github.com/mortymorty) - SecList brute file fix 
* [Chan9390](https://github.com/Chan9390) - Updates to the requirements.txt
* [dainok](https://github.com/dainok) - Python 3.6+ fixes
* [Apoorv Raj Saxena](https://github.com/apoorvrajsaxena) - Added SubFinder


##### Major Updates
- 07-15-2017: Updated to include error handling and updated reconnaissance  techniques from Bugcrowd's [LevelUp](https://pages.bugcrowd.com/level-up-virtual-hacking-conference) Conference (including subbrute/masscan and subdomain lists) - influenced by Jason Haddix's talk [Bug Hunter's Methodology 2.0](https://t.co/Umhj4NUtJ5)
- 08-09-2017: Various fixes (+ phantomjs error), added --fresh option, removed redundant PyBrute folder from output and added pip requirements.txt
- 08-15-2017: Added notification (--notify) option with Pushover or Gmail support
- 08-18-2017: Moved repo from [OrOneEqualsOne/reconned](https://github.com/OrOneEqualsOne/reconned)
- 09-28-2017: Updated for [Recon-ng](https://bitbucket.org/LaNMaSteR53/recon-ng) dependency + Python3 changes
- 06-20-2018: Added [Amass](https://github.com/caffix/amass) and option for no EyeWitness
- 10-12-2018: Added [SubFinder](https://github.com/subfinder/subfinder)
