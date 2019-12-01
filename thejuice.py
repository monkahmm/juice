from subprocess import *
import os
import sys
def thejuice():
    print("installing needed packages...")
    run('apt install -y libpam-cracklib ufw clamav', shell=True, stdout=PIPE)
    print("done.")
    print("setting password & lockout policy...")
    run('cp ./common-auth /etc/pam.d/common-auth', shell=True)
    run('cp ./common-password /etc/pam.d/common-auth', shell=True)
    run('cp ./login.defs /etc/login.defs', shell=True)
    print("done.")
    print("disabling guest account...")
    run('cp ./lightdm.conf /etc/lightdm/lightdm.conf', shell=True)
    print("done.")
    print("Configuring firewall...")
    run("ufw reset", shell=True)
    run("ufw deny 23", shell=True)
    run("ufw deny 2049", shell=True)
    run("ufw deny 515", shell=True)
    run("ufw deny 111", shell=True)
    run("ufw enable", shell=True)
    print("done.")
    print("deleting unaauthorized media files...")
    run("find / -name *.mp3 -type f -delete", shell=True)
    run("find / -name *.mov -type f -delete", shell=True)
    run("find / -name *.mp4 -type f -delete", shell=True)
    run("find / -name *.avi -type f -delete", shell=True)
    run("find / -name *.mpg -type f -delete", shell=True)
    run("find / -name *.mpeg -type f -delete", shell=True)
    run("find / -name *.flac -type f -delete", shell=True)
    run("find / -name *.m4a -type f -delete", shell=True)
    run("find / -name *.flv -type f -delete", shell=True)
    run("find / -name *.ogg -type f -delete", shell=True)
    run("find /home -name *.gif -type f -delete", shell=True)
    run("find /home -name *.png -type f -delete", shell=True)
    run("find /home -name *.jpg -type f -delete", shell=True)
    run("find /home -name *.jpeg -type f -delete", shell=True)
    print("done.")
    print("scanning for plaintext password files...")
    adminpassword = input("Type any admin password to search for: ")
    ptpasswdfile = run(["grep", "-r", adminpassword, "/boot", "/etc", "/home", "/bin"], stdout=PIPE)
    pwfiles = ptpasswdfile.stdout.decode().count('\n')
    if pwfiles > 0:
        print("\033[91m {}\033[00m".format("WARNING: %d PLAINTEXT PASSWORD FILES FOUND!!!" % pwfiles))
        print(ptpasswdfile.stdout.decode())
    else:
        print("no plaintext password files found in /boot, /etc, /home, or /bin.")
    print("auditing authorized users and admins...")
    fetchadmins = run("awk -F: '/sudo/{print $4}' /etc/group", stdout=PIPE, shell=True)
    currentadmins = fetchadmins.stdout.decode().split(',')
    with open("admins.txt", "r") as admins:
        authadmins = admins.readlines()
        for curradmin in currentadmins:
            if curradmin not in authadmins:
                run(["deluser", curradmin, "sudo"])
                run(["deluser", curradmin, "adm"])
    print("unauthorized admins demoted.")
    fetchusers = run("awk -F: '($3>=1000)&&($1!=\"nobody\"){print $1}' /etc/passwd", stdout=PIPE, shell=True)
    currentusers = fetchusers.stdout.decode().splitlines()
    with open("users.txt", "r") as users:
        authusers = users.readlines()
        for curruser in currentusers:
            if curruser not in authusers:
                run(["deluser", curruser])
    print("unauthorized users deleted.")
    print("settings secure passwords...")
    for user in authusers:
        passchanger = Popen(["passwd", user], stdin=PIPE, stdout=PIPE)
        passchanger.communicate(input="s3cur3P@55\ns3cur3P@55".encode())
    print("all user passwords changed to: s3cur3P@55")
    print("setting important file permissions...")
    run(["chmod", "600", "/boot/grub/grub.cfg"])
    run(["chmod", "640", "/etc/passwd"])
    run(["chmod", "640", "/etc/shadow"])
    run(["chmod", "640", "/etc/group"])
    run(["chmod", "640", "/etc/gshadow"])
    run(["chmod", "000", "/usr/bin/as"], stdout=PIPE, stderr=PIPE)
    run(["chmod", "000", "/usr/bin/byacc"], stdout=PIPE, stderr=PIPE)
    run(["chmod", "000", "/usr/bin/yacc"], stdout=PIPE, stderr=PIPE)
    run(["chmod", "000", "/usr/bin/bcc"], stdout=PIPE, stderr=PIPE)
    run(["chmod", "000", "/usr/bin/kgcc"], stdout=PIPE, stderr=PIPE)
    run(["chmod", "000", "/usr/bin/cc"], stdout=PIPE, stderr=PIPE)
    run(["chmod", "000", "/usr/bin/gcc"], stdout=PIPE, stderr=PIPE)
    run(["chmod", "000", "/usr/bin/*c++"], stdout=PIPE, stderr=PIPE)
    run(["chmod", "000", "/usr/bin/*g++"], stdout=PIPE, stderr=PIPE)
    run(["echo tty1 > /etc/securetty"], shell=True)
    run(["chmod", "0600", "/etc/securetty"])
    run(["chmod", "700", "/root"])
    print("file permissions set.")





if os.geteuid() == 0:
    if not (input('Did you complete forensics questions, read README, make authorized user (including admins) file named users.txt and authorized admin file named admins.txt? [yes/no]') == yes):
        print("do it then")
        exit()
    thejuice()
else:
    print("Y'aint root...try again")
    exit()
