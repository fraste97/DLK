import Interpreter

print('##########################################################################################################')
print('##########################################################################################################')
print('#####################          BENVENUTO NELL\'INTERPRETE DLK          ####################################')
print('##########################################################################################################')
print('##########################################################################################################')

while(True):

    file_name = input('\nInserire il nome del file contenente il programma da interpretare --> ')
    print()
    text_file = open(file_name, encoding='utf-8')
    lexer_result = (Interpreter.run(text_file.read()))

    text_file.close
    print('\033[0m')
    input("Premi invio per continuare")