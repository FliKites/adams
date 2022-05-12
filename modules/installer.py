"""               _                                    
     __ _      __| |     __ _      _ _ _      ____     
    / _` |    / _` |    / _` |    | ` ` |    / __/     
   | (_| |   | (_| |   | (_| |    | | | |    \__ \     
    \__,_| ⍟ \__,_|▄⍟▄\__,_|█⍟▄|_|_|_| ⍟ /___/ ⍟  
                   ███           ███                   
                 ███               ███                 
                ██                   ██                
                         ▄▄█▄▄                         
               ▄       ███───███       ▄               
              ███     ███──█──███     ███              
               ▀       ██──▄──██       ▀               
                         ▀▀█▀▀                         
                ██                   ██                
                 ███               ███                 
    Automated Decentralization And Management System   
                    ▀▀▀█████████▀▀▀                    
"""

import os
import sys
import subprocess
import json

from sys import platform
from time import sleep as sleep
from colours import colours
from display import clear_screen

if platform == "linux":
    from getch import getch as getch
elif platform == "win32":
    from msvcrt import getch as getch

class install:
    NEED_RESTART = False
    PATH = os.getcwd()                                      # A.D.A.M.S. Directory
    DATA_PATH = PATH + '/data/'                             # Data Directory Path
    HSD_PATH = PATH + '/hsd/'                               # Handshake Directory Path
    SKYNET_PATH = PATH + '/skynet-webportal/'               # Skynet Webportal Directory Path
    ANSIBLE_PLAYBOOKS_PATH = PATH + '/ansible-playbooks/'   # Ansible Playbooks Directory Path
    ANSIBLE_PRIVATE_PATH = PATH + '/ansible-private/'       # Ansible Private Directory Path
    POWERDNS_PATH = PATH + '/pdns/'                         # PowerDNS Directory Path

    def __init__(self, type):

        if type == "adams":
            print(colours.red(self, "\nInstalling A.D.A.M.S."))
            self.installDepends(self.getDependencies(sys.platform, "all"))
            self.handshake()
            self.powerdns()
            self.nginx()
            self.skynet_webportal()

        elif type == "skynet-webportal":
            print(colours.red(self, "\nInstalling Skynet Webportal"))
            self.installDepends(self.getDependencies(sys.platform, "skynet-webportal"))
            self.skynet_webportal()

        elif type == "handshake":
            print(colours.red(self, "\nInstalling Handshake Daemon"))
            self.installDepends(self.getDependencies(sys.platform, "handshake"))
            self.handshake()

        elif type == "powerdns":
            print(colours.red(self, "\nInstalling PowerDNS"))
            self.installDepends(self.getDependencies(sys.platform, "powerdns"))
            self.powerdns()

        elif type == "nginx":
            print(colours.red(self, "\nInstalling NGINX Webserver"))
            self.installDepends(self.getDependencies(sys.platform, "nginx"))
            self.nginx()
    #################################################### END: __init__(self, type)

    def getDependencies(self, sysPlatform, depends):

        dependencies = {}

        if depends == "":
            depends = "all"

        sysPlatform = sysPlatform.lower()
        depends = depends.lower()

        # Parse DEPENDS.json
        with open("DEPENDS.json") as depends_json:
            data = json.load(depends_json)
            for platform in data:

                # Get Windows dependencies
                if platform.lower() == "windows" and sysPlatform == "win32":
                    for packageType in data[platform]:
                        if packageType == "exec":
                            for package in packageType:
                                try:
                                    dependencies["exec"].append(package)
                                except KeyError:
                                    dependencies["exec"] == []
                                    dependencies["exec"].append(package)

                # Get Linux dependencies
                elif platform.lower() == "linux" and sysPlatform == "linux":
                    for packageType in data[platform]:
                        for packages in packageType:
                            for package in packageType[packages]:
                                try:
                                    dependencies[packages].append(package)
                                except KeyError:
                                    dependencies[packages] = []
                                    dependencies[packages].append(package)

                # Get Skynet Webportal dependencies
                elif platform.lower() == "skynet-webportal":
                    if depends == "all" or depends == "skynet-webportal":
                        for packageType in data[platform]:
                            for packages in packageType:
                                for package in packageType[packages]:
                                    exists = False
                                    try:
                                        if packages in dependencies[packages]:
                                            exists = True

                                        if exists == False:
                                                dependencies[packages].append(package)
                                    except KeyError:
                                        dependencies[packages] = []
                                        dependencies[packages].append(package)

                # Get Handshake dependencies
                elif platform.lower() == "handshake":
                    if depends == "all" or depends == "handshake":
                        for packageType in data[platform]:
                            for packages in packageType:
                                for package in packageType[packages]:
                                    exists = False
                                    try:
                                        if package in dependencies[packages]:
                                            exists = True

                                        if exists == False:
                                                dependencies[packages].append(package)
                                    except KeyError:
                                        dependencies[packages] = []
                                        dependencies[packages].append(package)

                # Get PowerDNS dependencies
                elif platform.lower() == "powerdns":
                    if depends == "all" or depends == "powerdns":
                        for packageType in data[platform]:
                            for packages in packageType:
                                for package in packageType[packages]:                                
                                    exists = False
                                    try:
                                        if package in dependencies[packages]:
                                            exists = True

                                        if exists == False:
                                                dependencies[packages].append(package)
                                    except KeyError:
                                        dependencies[packages] = []
                                        dependencies[packages].append(package)

                # Get NGINX dependencies
                elif platform.lower() == "nginx":
                    if depends == "all" or depends == "nginx":
                        for packageType in data[platform]:
                            for packages in packageType:
                                for package in packageType[packages]:                                
                                    exists = False
                                    try:
                                        if package in dependencies[packages]:
                                            exists = True

                                        if exists == False:
                                                dependencies[packages].append(package)
                                    except KeyError:
                                        dependencies[packages] = []
                                        dependencies[packages].append(package)

        # Discard un-needed dependencies for platform
        if sysPlatform == "win32":
            try:
                del dependencies["apt"]
            except KeyError:
                pass
        elif sysPlatform == "linux":
            try:
                del dependencies["exe"]
            except KeyError:
                pass

        return dependencies
    #################################################### END: getDependencies(self, sysPlatform, depends)

    def printDepends(self, depends):
        clear_screen()
        print(colours.yellow(self, " [!]") + " The following dependencies will be installed:")

        columns = 0
        packages = ""

        for packageType in depends:
            if packageType == "exe":
                print(colours.green(self, "\n  -- Windows Executable --"))

            elif packageType == "apt":
                print(colours.green(self, "\n  -- Linux APT Package --"))

            elif packageType == "pip":
                print(colours.green(self, "\n  -- Python Package --"))

            elif packageType == "git":
                print(colours.green(self, "\n  -- Github Repository --"))

            elif packageType == "npm":
                print(colours.green(self, "\n  -- Node Package Manager --"))

            elif packageType == "wget":
                print(colours.green(self, "\n  -- WGET --"))

            count = len(depends[packageType])

            for package in depends[packageType]:
                if len(package.strip()) <= 20:
                    while len(package) < 22:
                        package += " "

                packages += package

                columns += 1
                count -= 1

                if count == 0 or len(package) > 30:
                    print("\t" + packages)
                    packages = ""
                    columns = 0
                elif columns == 4:
                    print("\t" + packages)
                    columns = 0
                    packages = ""
        
        print()
        print(colours.prompt(self, "Press any key to continue, or 'ctrl+c' to return to main menu."))
        getch()
    #################################################### END: printDepends(self, depends)

    def installDepends(self, depends):
        self.printDepends(depends)

        for packageType in depends:
            # Install Windows Executable
            if packageType == "exe":
                packages = ""

                for package in depends[packageType]:
                    packages = packages + package + " "

            # Install Linux APT Package
            elif packageType == "apt":
                packages = ""

                for package in depends[packageType]:
                    packages = packages + package + " "
                
                subprocess.run(["sudo", "apt", "install", "-y", packages.strip()], check=True)

            # Install Python Packages
            elif packageType == "pip":
                packages = ""

                for package in depends[packageType]:
                    packages = packages + package + " "
                
                subprocess.run(["pip", "install", packages.strip()], check=True)

            # Clone Github Repository
            elif packageType == "git":
                for package in depends[packageType]:
                    package = str(package).strip()
                    subprocess.run(["git", "clone", package], cwd=self.PATH, check=True)

            # Install Node Package
            elif packageType == "npm":
                for package in depends[packageType]:
                    package = str(package).strip()
                    subprocess.run(["npm", "install", package], cwd=self.PATH, check=True)

            # Download/Install WGET Package
            elif packageType == "wget":
                for package in depends[packageType]:
                    package = str(package).strip()
                    print(colours.green(self, " [+] ") + "Downloading " + str(package))
                    subprocess.run(["wget", package], cwd=self.PATH, check=True)

                    if str(package).endswith("tar.gz"):
                        print("\t Unpacking...")
                        subprocess.run(["tar", "-xvf", package], cwd=self.PATH, check=True)
                        print("\t Cleaning up...")
                        subprocess.run(["rm", "-fr", package], cwd=self.PATH, check=True)
    #################################################### END: installDepends(self, depends)

    def skynet_webportal(self):
        print(colours.error(self, "skynet_webportal() method not yet complete."))
        sleep(1)

        """ print(colours.green(self, " [+] ") + "Installing Yarn")
        subprocess.run(["npm", "install", "yarn"], cwd=(self.SKYNET_PATH + "/packages/website"))

        print(colours.green(self, " [+] ") + "Building Skynet Portal Page")
        subprocess.run(["yarn", "build"], cwd=(self.SKYNET_PATH + "/packages/website"))
        print() """
    #################################################### END: skynet_webportal(self)

    def handshake(self):
        print(colours.error(self, "hsd() method not yet complete."))
        sleep(1)

        """ if os.path.isdir(self.HSD_PATH) == False:
            print(colours.green(self, " [+] ") + "Downloading Handshake Daemon")
            subprocess.run(["git", "clone", package], cwd=self.PATH, check=True)

            print(colours.green(self, " [+] ") + "Installing Handshake Daemon")
            subprocess.run(["npm", "install", "--production"], cwd=self.HSD_PATH)
            print()
        else:
            print(colours.yellow(self, " [!] ") + "Handshake Daemon Installation Detected!") """
    #################################################### END: hsd(self)

    def powerdns(self):

        #print(colours.green(self, " [+] ") + "\nConfiguring PowerDNS...")
        print(colours.error(self, "pdns() method not yet complete."))
        sleep(2)

        """if package.endswith("tar.gz"):

            if os.path.exists("./pdnsmanager") == False:
                print(colours.green(self, " [+] ") + "Extracting PowerDNS Manager")
                subprocess.run(["tar", "-xvf", package], cwd=self.PATH, check=True)
                subprocess.run(["mv", package[0:17], "pdnsmanager/"], cwd=self.PATH, check=True)
                subprocess.run(["rm", "-fr", package], cwd=self.PATH, check=True)
            
            if os.path.exists("./pdnsmanager") == True:
                print(colours.green(self, " [+] ") + "Configuring PowerDNS Manager")
            
            print()
        else:
            print(colours.green(self, " [+] ") + "Installing " + str(package))
            subprocess.run(["sudo", "apt", "install", "-y", package], check=True)
            print()

        hasRepo = False
        hasPackage = False

        # Check for existing PowerDNS APT sources
        if os.path.exists("/etc/apt/sources.list.d/pdns.list"):

            with open('/etc/apt/sources.list.d/pdns.list') as sourceFile:
                sources = sourceFile.readlines()

            for line in sources:
                if 'http://repo.powerdns.com/ubuntu' in line:
                    hasRepo = True

                if 'Package: pdns-*\nPin: origin repo.powerdns.com\nPin-Priority: 600' in line:
                    hasPackage = True

        # If PowerDNS APT sources do not exists, create them
        if hasRepo is False:
            print(colours.green(self, " [+] ") + "Adding PowerDNS Sources...")
            addSource = "echo 'deb [arch=amd64] http://repo.powerdns.com/ubuntu focal-auth-46 main' > /etc/apt/sources.list.d/pdns.list"
            subprocess.run(["sudo", "sh", "-c", addSource], cwd=self.PATH, check=True)
            print()

        if hasPackage is False:
            addSource = "echo 'Package: pdns-*\nPin: origin repo.powerdns.com\nPin-Priority: 600' > /etc/apt/preferences.d/pdns"
            subprocess.run(["sudo", "sh", "-c", addSource], cwd=self.PATH, check=True)
            
        # Downloaded and add PowerDNS APT Key
        print(colours.green(self, " [+] ") + "Adding APT-KEY...")
        subprocess.run(["wget", "https://repo.powerdns.com/FD380FBB-pub.asc"], cwd=self.PATH, check=True)
        subprocess.run(["sudo", "apt-key", "add", "FD380FBB-pub.asc"], cwd=self.PATH, check=True)
        subprocess.run(["rm", "-fr", "FD380FBB-pub.asc"], cwd=self.PATH, check=True)
        subprocess.run(["sudo", "apt", "update"], cwd=self.PATH, check=True)
        print()

        # Check and disable existing stub resolver
        dnsExists = False
        stubListenterExists = False

        # Check resolved.conf for configuration
        with open('/etc/systemd/resolved.conf') as resolveFile:
            lines = resolveFile.readlines()

        for line in lines:
            if line == "DNS=1.1.1.1":
                dnsExists = True

            if line == "DNSStubListener=no":
                stubListenterExists = True

        # Add configurations to resolved.conf
        print(colours.green(self, " [+] ") + "Disabling Stub Resolver...")
        if dnsExists == False or stubListenterExists == False:
            addLine = "# A.D.A.M.S. PowerDNS Configurations"
            subprocess.run(["sudo", "sh", "-c", addLine], check=True)
            NEED_RESTART = True

        if dnsExists == False:
            addLine = "echo 'DNS=1.1.1.1' >> /etc/systemd/resolved.conf"
            subprocess.run(["sudo", "sh", "-c", addLine], check=True)

        if stubListenterExists == False:
            addLine = "echo 'DNSStubListener=no' >> /etc/systemd/resolved.conf"
            subprocess.run(["sudo", "sh", "-c", addLine], check=True)
        print()
        # Create Symlink
        print(colours.green(self, " [+] ") + "Creating Symlink")
        subprocess.run(["sudo", "ln", "-sf", "/run/systemd/resolve/resolv.conf", "/etc/resolv.conf"], check=True) """
    #################################################### END: pdns(self)

    def nginx(self):
        print(colours.error(self, "nginx() method not yet complete."))
        sleep(1)
    #################################################### END: nginx(self)
    
class cli:
    menu_title = ""
    menu_options = ""

    def __init__(self):
        clear_screen()
        self.set_menu("MAIN")
        self.main_menu()
        sleep(1)
    #################################################### END: __init__(self)

    def get_input(self, prompt):
        user_input = input(colours().prompt(prompt))
        return user_input         
    #################################################### END: get_input(prompt)

    def print_header(self):
        clear_screen()  # Clear console window
        print(colours().title("\n\t" + menu_title[1] + "\n\n"))   # Print menu title
    #################################################### END: print_header()

    def print_options(self):
        for option in menu_options:     # Print menu options to screen
            print("\t    " + option)
        print()
    #################################################### END: print_options()

    def set_menu(self, menu_id):
        global menu_title
        global menu_options
        
        if menu_id.upper() == "MAIN":       # Main Menu Options
            menu_title = ["ADAMS_INSTALLER",
                          "A.D.A.M.S. Installer"]
                          
            menu_options = [colours().cyan("1") + ": Install A.D.A.M.S.",
                            colours().cyan("2") + ": Install Skynet Webportal",
                            colours().cyan("3") + ": Install Handshake Daemon",
                            colours().cyan("4") + ": Install PowerDNS",
                            colours().cyan("5") + ": Install NGINX Webserver",
                            "",
                            colours().cyan("B") + ": Back to A.D.A.M.S.",
                            colours().cyan("Q") + ": Quit A.D.A.M.S."]
    #################################################### END: set_menu(menu_id)

    def main_menu(self):
        self.set_menu("MAIN")    # Initialize A.D.A.M.S. Installer Menu
        
        try:
            while True: # Display A.D.A.M.S. Installer Menu
                self.print_header()
                self.print_options()
                
                user_input = self.get_input("\n\tWhat would you like to do? : ")
                
                if user_input.upper() == "1":   # Install A.D.A.M.S.
                    install("adams")

                elif user_input.upper() == "2": # Install Skynet Webportal
                    install("skynet-webportal")

                elif user_input.upper() == "3": # Install Handshake Daemon
                    install("handshake")

                elif user_input.upper() == "4": # Install PowerDNS
                    install("powerdns")

                elif user_input.upper() == "5": # Install NGINX Webserver
                    install("nginx")
                    
                elif user_input.upper() == "B":
                    from main import main as main
                    main()

                elif user_input.upper() == "EXIT" or user_input.upper() == "Q" or user_input.upper() == "QUIT":
                    clear_screen()    # Clear console window
                    sys.exit(0)

        except AttributeError as e:
            print(colours().error(str(e)))
            sleep(2)
            self.main_menu()
        except KeyboardInterrupt:
            from main import main as main
            main()
    #################################################### END: main_menu()

if __name__ == '__main__':
    os.system('cls')
    cli()
#################################################### END: __main__
