import Interpreter

text_file = open("DLK.txt", encoding='utf-8')
lexer_result = (Interpreter.run(text_file.read()))

if lexer_result != Interpreter.ERROR:
    print(lexer_result)
text_file.close
