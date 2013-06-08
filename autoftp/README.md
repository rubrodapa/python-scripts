AutoFTP
==============

>I made this script to upload "CGI SCripts" to my server. I was tired of open the usual program, connect and also after that I usually forgot to change the permissions of the files once they were upload.

Script to upload ASCII files to a FTP server and give them 755 permissions using Python 3.
It will upload all the files and directories inside the folder where the script is called to a folder specified in the server.

Usage:

- Modify the host, user and password of the script.
- Modify path of the server where the files and directories will be upload.
- Run the script, it will upload all the files except the script itself.