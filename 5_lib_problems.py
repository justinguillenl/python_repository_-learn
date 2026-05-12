import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#problema 1
a= np.array([150.5, 148.3, 152.1, 149.8, 155.2, 153.7, 157.0])
max = a.max()
min = a.min()
prom = a.mean()
maxf = np.max(a)
minf = np.min(a)
promf = np.mean(a)

b = a*1.1

c = a[a>152]

# problema 2

arr = np.arange(1,13)
matrix_data = arr.reshape((3,4))


sum_axis_1 = matrix_data.sum(axis=1)
sum_axis_0 = matrix_data.sum(axis=0)


two_row = matrix_data[1]
element = matrix_data[1][2] ##[1,2]
 


# problema 3

data_s= pd.read_csv("students.csv")

#print (data_s[:5])# print(data_s.head(5))

#print(data_s.describe())

#print(data_s[data_s["nota"]>= 70])

data_s["aprobado"] =data_s["nota"]>=60# data_s["aprobado"] = np.where(data_s["nota"]>=60,"aprobado","false")

#print(data_s)

promedio_por_materia = data_s.groupby("materia")["nota"].mean()# los dobles corchetes deveulven data y solo necesito una serie

#print(promedio_por_materia)

# problema 4 

data_sales = pd.read_csv("sales.csv")

data_sales["fecha"] = pd.to_datetime(data_sales["fecha"])# cambiandolo a un tipo de dato de panda
#print(data_sales)

data_sales["total_ventas"] = data_sales["precio"]*data_sales["cantidad"] # creo una nueva categoría para poder sumarla, ya que no se puede en el .groupby

total_ventas_categoria= data_sales.groupby("categoria")["total_ventas"].sum()
#print(total_ventas_categoria)

ventas_mes = data_sales.groupby(data_sales["fecha"].dt.month)["total_ventas"].sum()# ojo el dt.month que transforme

#mes = ventas_mes.idxmax() Te da el me en el que fue mayor
#valor = ventas_mes.max()
#print(f"Mes {mes} con ventas totales: ${valor:,.2f}")

#print (ventas_mes.max())

data_sales["ganancia"] = data_sales["precio"]*data_sales["cantidad"]*0.3

sales_mayor_promedio = data_sales[data_sales["ganancia"]>data_sales["ganancia"].mean()]

sales_mayor_promedio.to_csv("top_ventas.csv")#agregar ,index =False para que no se agrege 0 1 2 3 4 5 6

# problema 5 

fig, axs = plt.subplots(ncols=2, nrows=1, figsize=(10, 4),layout="constrained")

axs[0].bar(total_ventas_categoria.index,total_ventas_categoria, color= "red", label = "Ventas ($)")
axs[0].set_title("ventas por categorias")
#axs[0].setx_label("categorias")
axs[0].set_ylabel("total $")
axs[0].legend()

axs[1].plot(ventas_mes.index, ventas_mes, color= "green", marker= "o")
axs[1].set_title("ventas por mes")
axs[1].set_xlabel("mes")
axs[1].set_ylabel("ventas en $")
fig.suptitle('graficas del problema 5')

#plt.savefig("dashboard.png", dpi=150) # Guardado con la calidad solicitada

plt.show()

 



