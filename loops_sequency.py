#Escribe una función text_analyzer(text) que reciba un string y retorne un diccionario con:
#words: lista de palabras (sin espacios vacíos)
#word_count: cantidad total de palabras
#longest_word: la palabra más larga
#shortest_word: la palabra más corta
#unique_words: lista de palabras sin repetir (en orden de aparición)

def text_analyzer(text):
    
    words = text.split()
    word_count = len(words)
    longest_word = words[0]
    shortest_word =words[0]
    unique_words = []
    for i in range(len(words)):# tienen que coordinar int and int or str and str
        
        if len(longest_word)< len(words[i]) or len(longest_word) == len(words[i]) :
            longest_word = words[i]
        if len(longest_word)> len(words[i]):
            shortest_word = words[i]

        if words[i] not in unique_words :#pregunto si el elemento esta en la nueva lista creada, sino esta se agrega
            unique_words.append(words[i])
    return {#sintaxis correcta del diccionario que he creado
        "words":words,
        "word_count": word_count,
        "longest_word": longest_word,
        "shortest_word": shortest_word,
        "unique_words": unique_words

    }

    return print (words, word_count,longest_word, shortest_word, unique_words)
text1 = 'Justin haciendo codigo codigo grandisima we'
text_analyzer(text1)
#Escribe una función columnar_cipher(text, key) que cifre un mensaje escribiendo el texto en filas de longitud key 
#y leyendo las columnas de izquierda a derecha. Si la última fila queda incompleta, rellena con '_'.
#También escribe columnar_decipher(ciphertext, key) que revierta el proceso.
#Solo for loops y manejo de listas/strings
#Sin librerías externas
#columnar_decipher debe reconstruir la matriz por columnas y leer por filas
def columnar_cipher(text, key):
    list_text = list(text)# convirtiendo a este text en un iterable 
    matriz_text = []
    line_text = []
    aux = 0
    cipher_text= ''
    if len(list_text) % key != 0 :#todo este pedazo de código añade los '_' que falten de acuerdo a key
       res = len(list_text) % key
       
       for i in range(key -res):
           list_text.append('_')
            
    for char in list_text:
        
        if aux < key:
            line_text.append(char)
            aux += 1
        if len(line_text) == key and aux != 0:
            matriz_text.append(line_text.copy())# sino usaba copy se borraba también la list_text dentro de matriz
            line_text.clear()
            aux = 0
    for j in range(key):
        for i in range(int (len(list_text) / key)):
            cipher_text += str(matriz_text[i][j])
    
    return cipher_text

    #return '\n'.join(str(x) for x in matriz_text)# forma de imprimir dejando un \n 
def columnar_decipher(ciphertext, key):
    
    list_text= list(ciphertext)
    line_text = []
    matriz_text = []
    aux = 0
    decipher_text = ''
    for char in list_text:
        
        if aux < int (len(list_text) / key):
            line_text.append(char)
            aux += 1
        if len(line_text) == int (len(list_text) / key) and aux != 0:
            matriz_text.append(line_text.copy())# sino usaba copy se borraba también la list_text dentro de matriz
            line_text.clear()
            aux = 0

    for j in range(int (len(list_text) / key)):
        for i in range(key):
            if matriz_text[i][j] != '_':
                decipher_text += str(matriz_text[i][j])
            else :
                break
            
    return decipher_text

texxt = 'Justincode'
text_cod = str(columnar_cipher(texxt,4))

print (columnar_cipher(texxt,4))


print(columnar_decipher(text_cod,4))



