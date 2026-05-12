import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df_transacciones = pd.read_csv("transacciones.csv")
df_clientes = pd.read_csv("clientes.csv")
df_productos = pd.read_csv("productos.csv")

#df_trans[df_trans['fecha'].notna() & fechas_convertidas.isna()]
#t_id(int), cli_id(int),p_id(int), can_id(int), pu(float>0)

# cada dato de las diferentes df (saber qué y cómo filtrar esa data)
# transaccion_id  cliente_id  producto_id  cantidad  precio_unitario       fecha
# cliente_id     nombre_cliente tipo_cliente     ciudad
# producto_id    nombre_producto    categoria  precio_base   proveedor

# ─── 1. FECHAS ──────────────────────────────────────────
# Intenta convertir todo a datetime, lo que falle → NaT
fechas_convertidas = pd.to_datetime(df_transacciones["fecha"], errors="coerce")

# Encuentra las filas que fallaron
mask_fechas_malas = fechas_convertidas.isna() #mascaras booleneas para encontrar los valores erroneos
#print("Fechas inválidas encontradas:")
#print(df_transacciones[mask_fechas_malas][["transaccion_id", "fecha"]])# comprobando si mask_fechas_malas es true? entonces print id y fecha

# ─── 2. PRECIOS NEGATIVOS ────────────────────────────────
mask_precios_neg = df_transacciones["precio_unitario"] < 0
#print("\nPrecios negativos encontrados:")
#print(df_transacciones[mask_precios_neg][["transaccion_id", "precio_unitario"]])

# ─── 3. NULOS ────────────────────────────────────────────
#print("\nNulos por columna:")
#print(df_transacciones.isnull().sum())

# Fechas: reemplaza las malas con NaT y luego elimina esas filas
df_transacciones["fecha"] = pd.to_datetime(df_transacciones["fecha"], errors="coerce")
df_transacciones = df_transacciones.dropna(subset=["fecha"])

# Precios negativos: conviértelos a positivo (probablemente error de signo)
df_transacciones["precio_unitario"] = df_transacciones["precio_unitario"].abs()

# Nulos en cantidad y precio: elimina esas filas

# Usando merge para unir los 3 df en uno solo

df_transacciones = df_transacciones.dropna(subset=["cantidad", "precio_unitario"])

df_master_sub = pd.merge(df_transacciones,df_clientes, on = "cliente_id", how="right")

df_master = pd.merge(df_master_sub, df_productos, on= "producto_id", how="right")

# calculando ingreso total, descuento e ingreso neto

df_master["ingreso_total"] = df_master["cantidad"]*df_master["precio_unitario"]

# .value_counts() , .nunique() y .unique() utiles si no se me hubieran dicho cuantos tipos de clientes hay en el df

#print(df_master["tipo_cliente"].unique()) solo para comprobar

#np.select(condiciones, valores, default) 

condiciones = [
    df_master["tipo_cliente"] == "Premium",
    df_master["tipo_cliente"] == "Regular",
    df_master["tipo_cliente"] == "Nuevo"
]

valores = [0.15, 0.05, 0.0]  

df_master["descuento_aplicado"] = np.select(condiciones, valores, default=0.0)

df_master["ingreso_neto"] = df_master["ingreso_total"]*(1-df_master["descuento_aplicado"])

# Top 3 por mayores ingresos netos

print(df_master["ingreso_neto"].sort_values()[-3:])# .nlargest(3)

#agrupo por meses para poder trabajar lo siguiente

ventas_mes = df_master.groupby(df_master["fecha"].dt.month)["ingreso_neto"].sum()

mayor_crecimiento_porcentual = ventas_mes.pct_change()*100 #metodo CREADO!! para ello literalmente aunque también se pueden agregar la cantidad de periodos a compara .pct_change(periods=n)

print(mayor_crecimiento_porcentual.max())

# tabla pivot con: filas = mes, columnas = categoría, valores = suma de ingreso_neto

df_pivot = pd.pivot_table(df_master, values="ingreso_neto", index= df_master["fecha"].dt.month, columns=["categoria"], aggfunc= "sum")# me faltó el utlimo argumento

#print(df_pivot)

serie = df_pivot.stack()# stack() comprieme en una serie de elementos y lo vuelve solo una columna? 

#al parecer se necesita la creación de serie par ael uso de stack() WHYYYYYYYYYYYYYY?

#print(serie)

tope = np.percentile(serie.dropna(), 80)# El dropna es defensivo ya que el pivot puede haber creado Nan. 

print(serie[serie>=tope])

# Los clientes que compraron más de 3 categorías 

a = df_master.groupby(["nombre_cliente"])["categoria"].nunique()# uso a, b porque el nombre de lo que piden es demasiado largo xd

b = a[a>=3] 
#print(b)

ar = np.array(df_master["ingreso_neto"])

media = np.mean(ar)

desv_standar = ((((media-ar)**2).sum())/len(ar))**0.5 # manualmente

desv_nunpy = np.std(ar) # usarndo nunpy

print(desv_standar, desv_nunpy)

percentil_25 = np.percentile(ar,25)
percentil_50 = np.percentile(ar,50)
percentil_75 = np.percentile(ar,75)

print(percentil_25)
print(percentil_50)
print(media)
print(percentil_75)

outlier_array = ar[np.abs(df_master["ingreso_neto"]-media)>2*desv_nunpy]
print(outlier_array)

#	(0,0) Barras horizontales — Top 10 productos por ingreso neto
#	(0,1) Línea con marcadores — Evolución mensual del ingreso neto, con una línea punteada horizontal en el promedio mensual
#	(1,0) Barras apiladas — Ingreso neto por mes, separado por categoría
#	(1,1) Scatter plot — cantidad vs ingreso_neto, coloreado por categoría, con los outliers marcados en rojo con una x

fig, axs = plt.subplots(ncols=2, nrows=2, figsize=(16,8),layout="constrained")
top_10_productos= df_master.groupby("nombre_producto")["ingreso_neto"].sum().nlargest(10)
axs[0,0].barh(top_10_productos.index,top_10_productos,color= "green")
axs[0,0].set_title("Top 10 productos")
axs[0,0].set_xlabel("ganancia $")
axs[0,0].set_ylabel("productos")

mensual_ingreso_neto= df_master.groupby(df_master["fecha"].dt.month)["ingreso_neto"].sum()
media_1 = mensual_ingreso_neto.mean()
axs[0,1].plot(mensual_ingreso_neto.index,mensual_ingreso_neto, color="yellow")
axs[0,1].axhline(y=media_1, color='red', linestyle='--', linewidth=2, label=f'Media: {media:.2f}')
axs[0,1].set_title("Evolución mensual del ingreso neto")
axs[0,1].set_xlabel("mes en numero")
axs[0,1].set_ylabel("ingreso total en $")

# Paso 1: pivot con suma de ingreso_neto por mes y categoría
apilado = df_master.groupby([df_master["fecha"].dt.month, "categoria"])["ingreso_neto"].sum().unstack()
# unstack() convierte el segundo índice (categoria) en columnas:
# categoria    Electrónica  Muebles  Papelería
# fecha
# 1               15000      8000      1000
# 2               22000      6000       800

# Paso 2: graficar cada categoría apilada
# 'bottom' le dice a cada barra dónde empezar — encima de la anterior
categorias = apilado.columns          # ["Electrónica", "Muebles", "Papelería"]
colores = ["steelblue", "orange", "green"]
acumulado = np.zeros(len(apilado))    # empieza en 0 para la primera capa

for cat, color in zip(categorias, colores):
    axs[1, 0].bar(apilado.index,apilado[cat],bottom=acumulado,label=cat,color=color)# eje x: meses# altura de esta capa# dónde empieza esta capa
    acumulado += apilado[cat].values   # la siguiente capa empieza donde terminó esta

axs[1, 0].set_title("Ingreso neto por mes y categoría")
axs[1, 0].set_xlabel("Mes")
axs[1, 0].set_ylabel("Ingreso neto $")
axs[1, 0].legend()

# Paso 1: separar outliers de normales (ya lo calcule en  3.2, pero como array)
# Crea la máscara booleana
mask_outlier = np.abs(df_master["ingreso_neto"] - media) > 2 * desv_nunpy

# Agrégala como columna al DataFrame
df_master["outlier"] = mask_outlier
df_normal   = df_master[df_master["outlier"] == False]
df_outliers = df_master[df_master["outlier"] == True]

# Paso 2: un scatter por categoría para los puntos normales
categorias = df_master["categoria"].unique()   # ["Electrónica", "Muebles", "Papelería"]
colores     = ["steelblue", "orange", "green"]


for cat, color in zip(categorias, colores):
    subset = df_normal[df_normal["categoria"] == cat]
    axs[1, 1].scatter(subset["cantidad"], subset["ingreso_neto"],color=color,label=cat,alpha=0.6) # alpha transparencia para ver puntos solapados

# Paso 3: outliers encima en rojo con X
axs[1, 1].scatter(df_outliers["cantidad"],df_outliers["ingreso_neto"],color="red",marker="x",s=100,label="Outlier",zorder=5)# la X que pedía el enunciado   # tamaño del marcador  # zorder lo pinta encima de todo

axs[1, 1].set_title("Cantidad vs Ingreso neto")
axs[1, 1].set_xlabel("Cantidad")
axs[1, 1].set_ylabel("Ingreso neto $")
axs[1, 1].legend()

plt.show()







