records = [
    {"name": "Justin", "age": "22", "grade": "8.5"},
    {"name": "Ana",    "age": "veinte", "grade": "9.0"},
    {"name": "",       "age": "25", "grade": "7.0"},
    {"name": "Luis",   "age": "19", "grade": "texto"},
    {"name": "Maria",  "age": "23", "grade": "9.5"},
]
def clean_students(records):
    clean= []
    for dictionary in records:# se tomará el diccionario completo para hacer los cambios y usar el try except 
        if dictionary["name"]=="":
            continue# se pasa al siguiente elemento del bucle for
        try:
            dictionary["age"] = int(dictionary["age"])#verificación de datos en el tipo que deseamos
        except ValueError:#captura el error de inmediato
            dictionary["age"] = None # transformación de valores si no es el correcto
        try:
            dictionary["grade"] = float(dictionary["grade"])
        except ValueError:
            dictionary["grade"] = None
        if dictionary["grade"] is None:
            dictionary["status"] = "unknown"
        elif dictionary["grade"] >= 6.0:#uso cuando hay más de dos caminos 3 vías
            dictionary["status"] = "approved"
        else:
            dictionary["status"] = "failed"

        clean.append(dictionary)
                     
    return clean

clean_students(records)


sales = [
    ("laptop", "tech", 1200),
    ("phone", "tech", 800),
    ("shirt", "clothing", 50),
    ("laptop", "tech", 950),
    ("pants", "clothing", 80),
    ("tablet", "tech", None),   # dato sucio, ignorar con continue
    ("jacket", "clothing", 120),
]

def sales_analyzer(sales):
    new_dict={
        "total_by_category": "",#suma de ventas por categoría
        "unique_products":"",#set de productos únicos
        "top_category": "" #categoría con mayor venta total
    }
    unique_set = set() # usamos en constructor para crear un set para unique_prodcutos
    sum_tech = 0
    sum_cloth = 0
    # FUCKCKKKKKKKKK se puede hacer de 3 un for xddddddddd, pero ahora que lo pienso es posible
    # for product, category, precio in sales: XDDD
    for i in range(len(sales)):
        if None in sales[i]: #  se usa el in para el None y pasar a la siguiente tupla, dato sucio
               continue
        # todo el juego de los indices es darse cuenta que las tuplas estan ordenadas con los valores, así esten sucios, debes de dejar de pensar en ello como si fuera una matriz
        if sales[i][1]=="tech":
                   sum_tech += sales[i][2]
        elif sales[i][1]=="clothing":#si entra en el primero, el segundo NI SE MIRA
                   sum_cloth +=sales[i][2] 

        unique_set.add(sales[i][0])       

    if sum_tech >= sum_cloth:
      new_dict["top_category"] = "tech"
    else:
       new_dict["top_category"] = "clothing"
            
    new_dict.update(total_by_category= f"tech = {sum_tech} , clothing = {sum_cloth}")# actualizo el valor de la llave  
    new_dict.update(unique_products =str(unique_set))

    return new_dict
   
sales_analyzer(sales)

data = [10, 12, 11, 13, 10, 9, 100, 11, 12, -80, 10]

def filter_outliers(data):
    media= 0.0
    desv = 0.0
    dif=0.0
    dif_2=0.0
    list_filtered=[]
    aux=len(data)
    while aux>0:
         media+=data[len(data)-aux]
         aux -= 1
    media=media/len(data) #se suele colocar al ultimo el valor ya que se cerró el bucle while
    aux=len(data)
    while aux>0:
        dif =(data[len(data)-aux]-media)**2
        dif_2 += dif
        aux -= 1
    desv=((dif_2)/len(data))**0.5 # de igual forma que en la media
    list_filtered =[x for x in data if abs(x-media)<2*desv]
    return list_filtered
print(filter_outliers(data))
         

