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
Performing backup:
- cd DESTINATION_PATH
- github-backup.py -u GITHUB_USER

Restoration (tested on Codeberg.org):
- Create empty repository REPO_NAME
- cd USERNAME/REPO_NAME.git
- git push --mirror https://codeberg.org/USERNAME/REPO_NAME.git


Security
---------
- Script automatically removes directory named the same as GH user in current path!
- User name is not sanitized
- Repos names are not sanitized


License
---------
See LICENSE file