# Reconned
Bug Bounty Hunting Recon Script

**Moved from [OrOneEqualsOne/reconned](https://github.com/OrOneEqualsOne/reconned)- New Name, Same Great Recon!**

**Gist:** Some ~~terrible~~ continually updated python code leveraging some awesome tools that I use for bug bounty reconnaissance. 

**The tools contained in Reconned requires Kali Linux (preferred) or Debian 7+** 

reconned uses several subdomain enumeration tools and wordlists to create a unique list of subdmains that are passed to EyeWitness for reporting with categorized screenshots, server response headers and signature based default credential checking. *(resources are saved to ./bin and output is saved to ./output)*

Initial Install: *python reconned.py --install*

**_NOTE: This is an active recon – only perform on applications that you have permission to test against._**

##### Tools leveraged:

###### Subdomain Enumeraton Tools:
1. [Sublist3r](https://github.com/aboul3la/Sublist3r) by Ahmed Aboul-Ela 
2. [enumall](https://github.com/jhaddix/domain) by Jason Haddix 
3. [Knock](https://github.com/guelfoweb/knock) by Gianni Amato 
4. [Subbrute](https://github.com/TheRook/subbrute) by TheRook 
5. [massdns](https://github.com/blechschmidt/massdns) by B. Blechschmidt 

###### Reporting + Wordlists:
- [EyeWitness](https://github.com/ChrisTruncer/EyeWitness) by ChrisTruncer  
- [SecList](https://github.com/danielmiessler/SecLists) (DNS Recon List) by Daniel Miessler 
- [LevelUp All.txt Subdomain List](https://gist.github.com/jhaddix/86a06c5dc309d08580a018c66354a056) by Jason Haddix 

##### Usage
````
First Step:
Install Required Python Modules: sudo pip install -r ./ext/requirements.txt
Install Tools: python reconned.py --install

Example 1: python reconned.py -d example.com
Uses subdomain example.com (Sublist3r enumall, Knock)

Example 2: python reconned.py -d example.com -b -p --vpn
Uses subdomain example.com with seclist subdomain list bruteforcing (massdns, subbrute, Sublist3r and enumall), adds ports 8443/8080 and checks if on VPN

Example 3: python reconned.py -d example.com -b --bruteall
Uses subdomain example.com with large-all.txt bruteforcing (massdns, subbrute, Sublist3r and enumall)

Example 4: python reconned.py -d example.com --quick
Uses subdomain example.com and only Sublist3r (+subbrute)

Example 5: python reconned.py -d example.com --quick --notify
Uses subdomain example.com, only Sublist3r (+subbrute) and notification

Note: --bruteall must be used with the -b flag
````

Option | Description
------ | --- 
--install/--upgrade  |  Both do the same function – install all prerequisite tools (Kali is a prerequisite AFAIK)
--vpn   |   Check if you are on VPN (update with your provider)
--quick |   Use ONLY Sublis3r's subdomain methods (+ subbrute)
--bruteall  |   Bruteforce with JHaddix All.txt List instead of SecList
--fresh  |   Delete old data from output folder
--notify  |   Send Pushover or Gmail Notifications
-d  |   The domain you want to preform recon on
-b  |   Bruteforce with subbrute/massdns and SecList wordlist
-s n    |   Only HTTPs domains
-p  |   Add port 8080 for HTTP and 8443 for HTTPS 

##### Notifications
- Complete the ext/notifycfg.ini for Pushover or Gmail notifications. (*Enable must be set to True*)
- Please see the Pushover API info [here](https://pushover.net/api) and instructions on how to allow less secure apps on your gmail account [here](https://support.google.com/accounts/answer/6010255)

##### To-Do List
- Multiple Domain Names
- ~~Notifications~~

##### Updates
- 07-15-2017: Updated to include error handling and updated reconnaissance  techniques from Bugcrowd's [LevelUp](https://pages.bugcrowd.com/level-up-virtual-hacking-conference) Conference (including subbrute/masscan and subdomain lists) - influenced by Jason Haddix's talk [Bug Hunter's Methodology 2.0](https://t.co/Umhj4NUtJ5)
- 08-09-2017: Various fixes (+ phantomjs error), added --fresh option, removed redundant PyBrute folder from output and added pip requirements.txt
- 08-15-2017: Added notification (--notify) option with Pushover or Gmail support