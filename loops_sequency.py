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
    for i in range(len(words)):
        
        if len(longest_word)< len(words[i]) or len(longest_word) == len(words[i]) :
            longest_word = words[i]
        else :
            shortest_word = words[i]

        if words[i] not in unique_words :
            unique_words.append(words[i])
        

    return print (words, word_count,longest_word, shortest_word, unique_words)
text1 = 'Justin haciendo codigo codigo grandisima we'
text_analyzer(text1)
