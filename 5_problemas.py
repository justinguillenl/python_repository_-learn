import csv
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
        if dictionary["grade"] is None:# uso del is para preguntar si es None
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
      new_dict["top_category"] = "tech"# accede a añadir directamente en la key el nuevo valor, así es como se call al value
    else:
       new_dict["top_category"] = "clothing"
            
    new_dict.update(total_by_category= f"tech = {sum_tech} , clothing = {sum_cloth}")# actualizo el valor de la llave a todo ese nuevo string
    new_dict.update(unique_products =str(unique_set)) 
    # creo que una pista de como mejorar esto podría ser en la forma de respuesta del word, que usa diccionarios como value de la key

    return new_dict
   
sales_analyzer(sales)

data = [10, 12, 11, 13, 10, 9, 100, 11, 12, -80, 10]

def filter_outliers(data):
    media= 0.0
    desv = 0.0
    #squared_difd =0.0 se sobreescribe en el bucle while, por lo que no se necesita definir el valor 
    sum_squared_diff=0.0# colocando nombres en ingles de las variables
    list_filtered=[]
    aux=len(data)
    while aux>0:
         media+=data[len(data)-aux]
         aux -= 1
    media=media/len(data) #se suele colocar al ultimo el valor ya que se cerró el bucle while
    aux=len(data)
    while aux>0:
        squared_diff =(data[len(data)-aux]-media)**2
        sum_squared_diff += squared_diff
        aux -= 1
    desv=((sum_squared_diff)/len(data))**0.5 # de igual forma que en la media
    list_filtered =[x for x in data if abs(x-media)<2*desv] # se agrega x del bucle for donde x pertenece y si cumple el if
    return list_filtered
filter_outliers(data)

#gender,"race/ethnicity","parental level of education","lunch","test preparation course","math score","reading score","writing score"

def proces_csv(filepath):
    with open(filepath, encoding='utf-8') as f:
    # Probamos con delimiter=';' porque Excel en español suele usarlo
       reader = csv.DictReader(f)
       new_dict = {
        "average_by_group": "",#promedio de math score por race/ethnicity
        "top_10_percent": "",#lista de estudiantes en el top 10% de math score
        "gender_gap": ""#diferencia de promedio de math entre male y female
        }
       group_data = {}#diccionario para el trabajo de los promedios de grupos, las llaves son los tipos de grupos y el value son una lista de los valores de math score ELEGANTE!!!!
       list_10_percent =[]
       gen_data = {} #intentando responder la 3era parte con la construccion de la primera
       for row in reader:
          group= row["race/ethnicity"]# verificacion de si ya existe este nuevo grupo en el diccionario group_data
          if group not in group_data:
               group_data[group]=[]# se ingresa una llave nueva con ese nombre del group y se le da el valor de una lista vacia
          group_data[group].append(float(row["math score"]))# si ya el group en el diccionario solo se añade el flotante a la lista
          list_10_percent.append(row)# guardamos todo el diccionario de filas en una lista xddddddddddd
          gen = row["gender"]
          if gen not in gen_data:
               gen_data[gen]=[]
          gen_data[gen].append(float(row["math score"]))

        
    
    # SIN COMENTARIO ANTE TAL BESTIALIDAD DICT COMPRESSION
    #{key: value for <variable> in <cualquier iterable>} , idea general de como usarlo
    new_dict["average_by_group"] = {group: sum(scores)/len(scores) for group, scores in group_data.items()}
    list_10_percent.sort(key= lambda x: float(x["math score"]), reverse=True) # forma de usar sort con la llave lambda  

    #lambda argumentos: expresión

# Función normal
#def doble(x):
#   return x * 2
# Lambda equivalente
#lambda x: x * 2    
     
    new_dict["top_10_percent"]= list_10_percent[:int(len(list_10_percent)*0.1)]

    dif= abs(sum(gen_data["female"])/len(gen_data["female"]) -sum(gen_data["male"])/len(gen_data["male"]))

    new_dict["gender_gap" ]=str(dif)
    return new_dict
proces_csv("StudentsPerformance.csv")


###########

def load_and_clean(filepaht): #lista de directorios 
    with open(filepaht) as f:
         reader = csv.DictReader(f)
         data_clean =[]
         for row in reader:
              data_clean.append(row)
    return data_clean
              
def filter_data(data, category, start_year , end_year):#lista de directorios
     filtered= []
     for row in data:
          if (category is None or row["Category"] == category) and (start_year is None or int(row["Order Date"][6:])>= start_year) and (end_year is None or int(row["Order Date"][6:])<= end_year):
               filtered.append(row)

     return filtered
def aggregate_by_region(data):#directorio
     dic_region={}
     new_dic= {}
     #Sales,Quantity,Discount,Profit
     for dict in data:
          region= dict["Region"]
          if region not in dic_region:
               dic_region[region] = []
          dic_region[region].append(float(dict["Profit"]))

     new_dic.update(metricas = {region: f"total: {sum(profit)} promedio: {sum(profit)/len(profit)} " for region, profit in dic_region.items()})     

     return new_dic
def top_profitable_products(data, n): # lista de tuplas
     list_profitable=[]
     #dict_product = {}
     my_list= []
     #for dict in data:
          #product = dict["Product Name"]
          #if product not in dict_product:
           #    dict_product[product] = []
          #dict_product[product].append()
        #  rentabilidad = (float(dict["Profit"])/float(dict["Quantity"]))*100
        #  my_list.append(dict["Product Name"])
        #  my_list.append(rentabilidad)
        #  list_profitable.append(tuple(my_list))
        #  my_list.clear()

     #print(type(list_profitable[0][1]), list_profitable[0][1]) # esto lo añadió claude XDD


     #list_profitable =sorted(list_profitable, key= lambda x: x[1], reverse= True)[:n]
     dict_product = {}
     for row in data:
        product = row["Product Name"]
        if product not in dict_product:
            dict_product[product] = 0
        dict_product[product] += (float(row["Profit"]) / float(row["Quantity"])) * 100

     list_profitable = sorted(dict_product.items(), key=lambda x: x[1], reverse=True)[:n]
     return list_profitable

#data = load_and_clean('superstore.csv')
#filtered = filter_data(data, category='Technology', start_year=2015, end_year=2017)
#metrics = aggregate_by_region(filtered)
#top = top_profitable_products(filtered)
data = load_and_clean("Sample - Superstore.csv")
filter = filter_data(data, category='Technology', start_year=2015, end_year=2017)
metrics = aggregate_by_region(filter)
print(top_profitable_products(filter, 5))



         
    
        
    

       
  
         

