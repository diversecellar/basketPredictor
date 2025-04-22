import os, shutil, sys
from colorama import Fore, Style
import glob
folder_root = os.getcwd()
acceptable_toggle = ["y", "n", "Y", "N", "yes", "no", "YES", "NO", "Yes", "No"]
print(f"{Fore.RED}WARNING: this code deletes all folders and files targeted in the same Directory as the code!{Style.RESET_ALL}")
folder_target = str(input("What is the name of your target folder?: "))
folder_toggle = str(input("Would you like delete the folder as well?(y/n): "))
if folder_toggle not in acceptable_toggle:
    print("Unacceptable delete option, run again")
    sys.exit()
if folder_toggle == "y" or folder_toggle == "Y" or folder_toggle == "yes" or folder_toggle == "Yes" or folder_toggle == "YES":
    folder = os.path.join(folder_root, folder_target)
    print(folder)
    print("--->Deleting folder and contents")
    print("---->Beginning to eradicate all subfiles in folder")
    if os.path.exists(folder):
        os.chdir(folder)
        for filename in glob.glob("**/*", recursive=True):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                    os.remove(file_path)
                elif os.path.isdir(file_path):
                    os.unlink(file_path)
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))
        print("----<Done with contents")
        if os.path.isdir(folder):
            shutil.rmtree(folder)
        print("---<Done deleting folder and contents")
if folder_toggle == "n" or folder_toggle == "N" or folder_toggle == "no" or folder_toggle == "No" or folder_toggle == "NO":
    folder = os.path.join(folder_root, folder_target)
    print("--->Beginning to eradicate all subfiles in folder")
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        print(file_path)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.remove(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
        if os.path.exists(file_path):
            print("---!Unsuccessful")
    print("---<Done with contents")
print("ENDS")