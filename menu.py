from sys import exit
import main

error = False

print "\n" * 20

while True:

    print "\n\n" + """
    _________          _______  _        _______  _______  _______ _________
    \__   __/|\     /|(  ____ )( (    /|(  ____ \(  ___  )(  ___  )\__   __/
       ) (   | )   ( || (    )||  \  ( || (    \/| (   ) || (   ) |   ) (   
       | |   | |   | || (____)||   \ | || |      | |   | || (___) |   | |   
       | |   | |   | ||     __)| (\ \) || |      | |   | ||  ___  |   | |   
       | |   | |   | || (\ (   | | \   || |      | |   | || (   ) |   | |   
       | |   | (___) || ) \ \__| )  \  || (____/\| (___) || )   ( |   | |   
       )_(   (_______)|/   \__/|/    )_)(_______/(_______)|/     \|   )_(

            
            Enter a number to choose an option:
                1. Start game
                2. Exit
"""
    if error == True:
        print "\n                That's not an option!\n"
    else:
        print "\n\n"
    
    error = False
    
    print "\n\n\n\n"
    
    option = raw_input('> ')

    if option == '1':
        main.play()
    
    elif option == '2':
        exit(1)
    
    else:
        error = True