from sys import exit
import main

error = False

while True:

    main.wipe()
    
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
                2. Start game without intro sequence
                3. Exit
"""
    if error == True:
        print "\n                That's not an option!\n"
    else:
        print "\n\n"
    
    error = False
    
    option = raw_input('> ')

    if option == '1':
        main.play(1)
    
    elif option == '2':
        main.play(2)
    
    elif option == '3':
        exit(1)
    
    else:
        error = True