'''               _                                    
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
'''

from getpass import getpass
import os
import sys

from sys import platform
from time import sleep as sleep
from colours import colours
from display import clear_screen

if platform == 'linux':
    from getch import getch as getch
elif platform == 'win32':
    from msvcrt import getch as getch
        
class cli:
    menu_title = ''
    menu_options = ''

    def __init__(self, _type:str=None):
        clear_screen()

        if _type == None or _type.upper() == "MAIN": 
            self.main_menu()
        elif _type.upper() == "SKYNET-WEBPORTAL" or _type.upper() == "SKYNET": 
            import skymanager
            skymanager.cli()
        elif _type.upper() == "HSD" or _type.upper() == "HANDSHAKE":
            import hsmanager
            hsmanager.cli()
        elif _type.upper() == "PDNS" or _type.upper() == "POWERDNS": 
            import pdnsmanager
            pdnsmanager.cli()
        elif _type.upper() == "NGINX":
            import nginxmanager
            nginxmanager.cli()
        
        self.main_menu()
    #################################################### END: __init__(self)

    def get_input(self, prompt):
        user_input = input(colours().prompt(prompt))
        return user_input         
    #################################################### END: get_input(prompt)

    def get_input_pass(self, prompt):
        user_input = getpass(colours().prompt(prompt))
        return user_input         
    #################################################### END: get_input(prompt)

    def print_header(self):
        clear_screen()  # Clear console window
        print(colours().title('\n\t' + menu_title[1] + '\n\n'))   # Print menu title
    #################################################### END: print_header()

    def print_options(self):
        for option in menu_options:     # Print menu options to screen
            print('\t    ' + option)
        print()
    #################################################### END: print_options()

    def set_menu(self, menu_id):
        global menu_title
        global menu_options
        
        if menu_id.upper() == 'MAIN':       # Main Menu Options
            menu_title = ['ADAMS_MANAGMENT',
                          'A.D.A.M.S. Management']
                          
            menu_options = [colours().cyan('1') + ': Skynet Webportal',
                            colours().cyan('2') + ': Handshake Daemon',
                            colours().cyan('3') + ': PowerDNS',
                            colours().cyan('4') + ': NGINX Webserver',
                            '',
                            colours().cyan('B') + ': Back to A.D.A.M.S.',
                            colours().cyan('Q') + ': Quit A.D.A.M.S.']

    #################################################### END: set_menu(menu_id)
    ### START: main_menu()

    def main_menu(self):
        self.set_menu('MAIN')    # Initialize A.D.A.M.S. Configuration Menu
        
        try:
            while True: # Display A.D.A.M.S. Configuration Menu
                self.print_header()
                self.print_options()
                
                user_input = self.get_input('\n\tWhat would you like to do? : ')
                
                if user_input.upper() == '1':   # Skynet Webportal Management
                    import skymanager
                    skymanager.cli()

                elif user_input.upper() == '2': # Handshake Daemon Management
                    import hsmanager
                    hsmanager.cli()

                elif user_input.upper() == '3': # PowerDNS Management
                    import pdnsmanager
                    pdnsmanager.cli()

                elif user_input.upper() == '4': # NGINX Management
                    import nginxmanager
                    nginxmanager.cli()
                    
                elif user_input.upper() == 'B':
                    import main
                    main.main(['adams','main'])

                elif user_input.upper() == 'EXIT' or user_input.upper() == 'Q' or user_input.upper() == 'QUIT':
                    clear_screen()    # Clear console window
                    sys.exit(0)

        except AttributeError as e:
            print(colours().error(str(e)))
            sleep(2)
            self.main_menu()
        except KeyboardInterrupt:
            import main
            main.main(['adams','main'])
    #################################################### END: main_menu()

if __name__ == "__main__":
    os.system("cls")
    cli()
#################################################### END: __main__
