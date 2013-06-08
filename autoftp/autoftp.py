import sys
import os
import inspect
from ftplib import FTP
from ftplib import error_perm
from socket import gaierror

#Get the name of the script to ignore it when uploading
ignoreFile = os.path.basename(__file__)
#Path to upload in the server
path = '/path/to/upload';

def uploadFile(ftp, dirpath,filename,actualPath):
    """
    Upload the file to the FTP server with the same structure as local server.
    """
    #If is not the PythonScript file
    if filename != ignoreFile:

        #The upload path relative to the actual folder in local in UNIX format
        uploadPath = dirpath[1:].replace("\\","/")

        #If we are not in the correct path change it (and create if not exist)
        if actualPath != uploadPath:
            try:
                ftp.cwd(path+uploadPath)
            except error_perm:
                ftp.mkd(path+uploadPath)
                ftp.cwd(path+uploadPath)
            actualPath = uploadPath

        #Store the file and change permissions
        print("Uploading: "+os.sep.join([dirpath, filename]))
        ftp.storlines("STOR "+filename,open(os.sep.join([dirpath, filename]), 'rb'))
        ftp.sendcmd('SITE CHMOD 755 '+filename)
        print("Done.")
        #Return the actualPath to modify it at the main scope
        return actualPath
            
def main():
    """
    Main execution flow
    """

    print("You are uploading to this folder: "+path)

    #Create structure of the actual folder in local
    print("Creating structure of local folders.")
    tree = os.walk(".")
    print("Done.")
    print("Starting upload.")

    try:
        #FTP configuration
        ftp = FTP('host')
        ftp.login('user','password')
        ftp.cwd(path)
    except gaierror:
        print("ERROR: Not able to connect to the server")
        sys.exit(2)
    except error_perm:
        print("ERROR: Not able to login or reach path to upload.")
        print("Check user and password and that the path exists in the FTP server.")
        sys.exit(2)

    #Control in which folder inside path we are
    actualPath = "";

    #Iterate through the tree
    for (dirpath, dirnames, filenames) in tree:
        #For each element
        for filename in filenames:
            #Upload file and overwrite the actualPath (maybe it has change inside the function)
            actualPath = uploadFile(ftp, dirpath, filename, actualPath)

    #Finish ftp session
    ftp.quit()

if __name__ == "__main__":
    sys.exit(main())