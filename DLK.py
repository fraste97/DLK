import Interpreter

text_file = open("DLK.txt")
text = text_file.read()
print(Interpreter.run(text))
text_file.close