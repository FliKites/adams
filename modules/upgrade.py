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

from time import sleep as sleep
from colours import colours as colours
from error_handler import MethodNotFound

class cli(object):
    def __init__(self):
        self.clear_screen
        print(colours.error(self, "upgrade.py not yet complete."))
        sleep(1)
        
        from main import main as main
        main()
#################################################### END: __init__(self)

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
#################################################### END: clear_screen(self)



if __name__ == '__main__':
    os.system('cls')
    print(colours.error("upgrade.py not yet complete."))
    sleep(1)
