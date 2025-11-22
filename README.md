# github-backup
Backup tool for public GitHub repositories


Description
---------
Script fetches all public repositories of given user and perform git clone --mirror.
It is intended to create local mirror for backup purposes.
WARNING It automatically removes directory named the same as GH user in current path!


Requirements
---------
- git


Usage
---------
github-backup.py -u GH_user


License
---------
See LICENSE file