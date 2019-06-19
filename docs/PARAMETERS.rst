Parameters
===========

* ``-d`` or ``--domain``
    This argument is used to provide the domained that is to be enumerated.
    Ex: ``python vault.py -d http://example.com``

* ``-b`` or ``--bruteforce``
    With this argument following tools will be used for enumeration::
        - massdns
        - sublist3r
        - enumall
        - amass
        - subfinder

* ``-p`` or ``--ports``
    This argument is used to use different port for enumeration.

* ``-q`` or ``--quicks``
    This argument is used to do a quick domain enumeration.
    This will use only two tools:
    - Amass
    - Subfinder

* ``--upgrade``
    This argument is used to upgrade the installed tools.

* ``--install``
    This argument is used to install all the tools required by domained.

* ``--vpn``
    This argument is used to check if you are connected to a VPN.

* ``--bruteall``
    This argument is used to let domained use `LevelUp All.txt Subdomain List <https://gist.github.com/jhaddix/86a06c5dc309d08580a018c66354a056>`_.

* ``--fresh``
    This argument is used to remove ``output`` directory and start the scan with fresh eyes.

* ``--notify``
    This argument is used to notify user when the script is finished.
    There are two ways to notify the user

        - `Pushover <https://pushover.net/>`_ notification
        - Email

    To use this argument modify the `notifycfg.ini <../ext/notifycfg.ini>`_ file.

* ``--active``
    This argument is used to run ``eyewitness`` with `active scan <https://www.christophertruncer.com/eyewitness-and-active-account-enumeration/>`_.

* ``--noeyewitness``
    This argument is for not using ``eyewitness`` for output reporting.

