import Interpreter

print('\n##########################################################################################################')
print('##########################################################################################################')
print('#####################          BENVENUTO NELL\'INTERPRETE DLK          ####################################')
print('##########################################################################################################')
print('##########################################################################################################')

stay_in_loop = True

# ciclo per l'aquisizione dell'indirizzo del file da interpretare ed eseguire
while(stay_in_loop):
    file_name = input('\n\033[0mInserire il nome del file contenente il programma da interpretare (ESC per uscire) --> ')
    print()

    if file_name != "ESC":
        try:
            text_file = open(file_name, encoding='utf-8')
            Interpreter.run(text_file.read())  # interpreta ed esegue il programma di cui è stato inserito l'indirizzo
            text_file.close
            input(f'\033[0m\nProgramma \'{file_name}\' terminato, premi invio per continuare')
        except:
            print(f'\033[91mImpossibile trovare il file: \'{file_name}\'')
            print('Controllare che il file sia nella stessa cartella dell\'interprete')
    else:
        stay_in_loop = False

print('\033[0mArrivederci, a presto!\n')