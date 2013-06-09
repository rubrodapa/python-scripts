import sys
import os
from ftplib import FTP
from ftplib import error_perm
from socket import gaierror

#Get the name of the script to ignore it when uploading
ignoreFile = os.path.basename(__file__)
#Path to upload in the server
path = '/path/to/upload';

def main():
    lista = os.listdir()
    try:
        #FTP configuration
        ftp = FTP('host')
        ftp.login('user','pass')
        ftp.cwd(path)
    except gaierror:
        print("ERROR: Not able to connect to the server")
        sys.exit(2)
    except error_perm:
        print("ERROR: Not able to login or reach path to upload.")
        print("Check user and password and that the path exists in the FTP server.")
        sys.exit(2)
    recursive(".\\",lista,ftp)
    ftp.quit()

def recursive(actualPath,lista,ftp):
    for element in lista:
        if os.path.isdir(actualPath+element):
            try:
                newDir = actualPath[1:].replace("\\","/")+element
                ftp.mkd(path+newDir)
            except:
                pass
            recursive(actualPath+element+"\\",os.listdir(actualPath+element),ftp)
        elif os.path.isfile(actualPath+element) and element != ignoreFile:
            uploadPath = actualPath[1:].replace("\\","/")
            ftp.cwd(path+uploadPath)
            ftp.storlines("STOR "+element,open(actualPath+element, 'rb'))
            ftp.sendcmd('SITE CHMOD 755 '+element)

if __name__ == "__main__":
        main()