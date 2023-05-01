import chardet

with open("file.txt", "rb") as file:
    content = file.read()
    
result = chardet.detect(content)
print(result["encoding"])