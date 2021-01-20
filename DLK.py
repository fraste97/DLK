import Interpreter

print('\n##########################################################################################################')
print('##########################################################################################################')
print('#####################          BENVENUTO NELL\'INTERPRETE DLK          ####################################')
print('##########################################################################################################')
print('##########################################################################################################')

# ciclo infinito per l'aquisizione dell'indirizzo del file da interpretare ed eseguire
while(True):
    file_name = input('\n\033[0mInserire il nome del file contenente il programma da interpretare --> ')
    print()
    try:
        text_file = open(file_name, encoding='utf-8')
        Interpreter.run(text_file.read())  # interpreta ed esegue il programma di cui è stato inserito l'indirizzo
        text_file.close
        input("\033[0m\nProgramma terminato, premi invio per continuare")
    except:
        print(f'\033[91mImpossibile trovare il file: \'{file_name}\'')
        print('Controllare che il file sia nella stessa cartella dell\'interprete')