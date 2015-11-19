import site
import os.path
import sys
import fileinput


def error_message():
    print("In your site-packages folder of your python installation search for the file nt.py")
    print("This is usually located under site-packages\\Crypto\\Random\\OSRNG\\")
    print("Change the line \"import winrandom\" to \"from . import winrandom\"")
    print("And rerun the paramiko installation")
    sys.exit(0)


dir_path = site.getsitepackages()[1] + "\\Crypto\\Random\\OSRNG\\"
nt_file = dir_path + "nt123.py"

if not os.path.isfile(nt_file):
    print("The file does not exist!")
    print("Maybe you want to try to edit it manually:")
    error_message()



# If you run fileinput.input in inplace mode, the file is edited in place and
# all the output of print() is redirected to the new file until the instance is closed.
try:
    finput = fileinput.input(nt_file, inplace=1, backup=".bak")
    for line in finput:
        print(line.replace("import winrandom", "from . import winrandom"), end="")
    finput.close()
except IOError:
    print("An error occurred while processing the file.")
    print("Maybe you want to try to edit it manually:")
    error_message()

print("The file should be fixed now.")
print("If anything went wrong, please restore the backup file located at: ")
print(nt_file + ".bak")
print("In this case you might want to edit the file manually:")
error_message()
