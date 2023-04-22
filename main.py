import mysql.connector
from prettytable import PrettyTable

# PALABRAS CONTEMPLADAS.
verbosNormales = ["dar", "abrir", "cerrar", "coger", "hablar", "mirar", "usar", "empujar", "tirar"]
verbosIr = ["ir"]
verbosTienda = ["comprar", "vender"]
conjunciones = ["a", "con"]
direcciones = ["norte", "sur", "este", "oeste"]
comandos = ["inventario", "nuevo", "guardar", "cargar", "mapa", "ayuda", "si", "no"]
# En el caso de los objetos y los personajes los cargamos desde los .txt con sus nombres.
archivoObjetos = open("objetos.txt", 'r')
archivoPersonajes = open("personajes.txt", 'r')
personajes = archivoPersonajes.read().split()
objetos = archivoObjetos.read().split()
# Cerramos los archivos.
archivoObjetos.close()
archivoPersonajes.close()

# Utilidades.
# Para facilitar la clasificación de verbos.
verbos = ["verboNormal", "verboIr", "verboTienda"]
tokens = []
# Para facilitar la validación de las expresiones.
palabras = []
entrada = ""

# REGLAS GRAMATICALES.
reglasVerbosNormales = ["objeto", "conjuncion", "personaje"]
reglasVerbosIr = ["direccion"]
reglasVerbosTienda = ["objeto"]
reglasObjetos = ["conjuncion"]
reglasConjunciones = ["objeto", "personaje"]
reglasPersonajes = ["conjuncion"]
reglasDirecciones = []  # Como detrás de una dirección no puede ir ninguna otra palabra, esta lista la dejamos vacía
# pero esto podría cambiar en el futuro.

# Conexión base de datos.
con = mysql.connector.connect(
    host="localhost",
    user="root",
    password="admin",
    database="juego"
)
cur = con.cursor()

# Variables para el juego.
nombreJugador = ""  # Nombre del jugador en la partida.
salaJugador = 1  # Sala donde está el jugador actualmente.
listaObjetosVisibles = ["mesa", "cuchillo", "cofre", "cuadro", "puerta"]  # Lista de objetos con los que puedes
# interactuar.
listaObjetosUsados = []  # Lista de objetos usados y "gastados".
habitacionesVisitadas = [1]  # Lista de las habitaciones en las que has entrado.
recordPuntuacion = 0  # Puntuación máxima conseguida en el juego.
jugadorRecord = ""  # Jugador con el récord actual.
puntuacionActual = 100  # La puntuación inicial es de 100, ya que el hecho de entrar en la primera sala te da +100.
monedasOro = 0  # Las monedas de oro que usas para comprar en la tienda.
inventario = []  # Los objetos que tienes en cada momento.


# Validamos si todas las palabras introducidas existen en el sistema.
def validar_palabra_existente(lista):
    global palabras
    correcto = True
    palabras = lista
    for palabra in lista:
        # Si la palabra no está en ninguna de las listas salimos.
        if palabra in verbosNormales or palabra in verbosIr or palabra in verbosTienda or palabra in objetos or \
                palabra in conjunciones or palabra in direcciones or palabra in personajes or palabra in comandos:
            correcto = True
        else:
            correcto = False
            return correcto
    return correcto


# Validamos la semántica y damos el resultado final.
def validacion_semantica(lista):
    # Rellenamos la lista de tokens con cada categoría de palabra en nuestra entrada.
    tokens.clear()
    for palabra in lista:
        if palabra in verbosNormales:
            tokens.append("verboNormal")
        elif palabra in verbosIr:
            tokens.append("verboIr")
        elif palabra in verbosTienda:
            tokens.append("verboTienda")
        elif palabra in objetos:
            tokens.append("objeto")
        elif palabra in conjunciones:
            tokens.append("conjuncion")
        elif palabra in direcciones:
            tokens.append("direccion")
        elif palabra in personajes:
            tokens.append("personaje")
        elif palabra in comandos:
            tokens.append("comando")
    longitud = len(tokens)
    if longitud > 4:
        print("La expresión no puede tener más de 4 palabras.")
        correcto = False
        return correcto
    contador = 1

    # Analizamos el primer elemento
    # Si la primera palabra es un comando, debe ir solo en una expresión.
    if tokens[contador - 1] == "comando":
        if len(tokens) == 1:
            correcto = True
            return correcto
        else:
            correcto = False
            return correcto
    # Si no es ni comando, tiene que ser un verbo, pero cada uno cumple sus reglas por lo que hay que comprobarlos.
    elif tokens[contador - 1] == "verboNormal" and longitud > 1:
        if tokens[contador] in reglasVerbosNormales:
            correcto = True
        else:
            correcto = False
            return correcto
    elif tokens[contador - 1] == "verboIr" and longitud > 1:
        if tokens[contador] in reglasVerbosIr:
            correcto = True
        else:
            correcto = False
            return correcto
    elif tokens[contador - 1] == "verboTienda" and longitud > 1:
        if tokens[contador] in reglasVerbosTienda:
            correcto = True
        else:
            correcto = False
            return correcto
    else:
        correcto = False
        return correcto

    # Analizamos desde el segundo hasta el último elemento
    while contador < longitud - 1:

        # Comprobamos que para cada tipo de palabra se cumplan sus reglas.
        if tokens[contador] == "objeto":
            if tokens[contador + 1] in reglasObjetos:
                correcto = True
            else:
                correcto = False
                return correcto
        elif tokens[contador] == "conjuncion":
            if tokens[contador + 1] in reglasConjunciones:
                correcto = True
            else:
                correcto = False
                return correcto
        elif tokens[contador] == "direccion":
            if tokens[contador + 1] in reglasDirecciones:
                correcto = True
            else:
                correcto = False
                return correcto
        elif tokens[contador] == "personaje":
            if tokens[contador + 1] in reglasPersonajes:
                correcto = True
            else:
                correcto = False
                return correcto

        contador += 1
    # Imprimimos el último elemento y solo salimos en caso de ser una conjunción.
    if tokens[contador] == "conjuncion":
        correcto = False
        return correcto
    return correcto


# Definimos la función introducir expresión.
def introduce_expresion():
    global entrada
    # Controlamos que se introduzca una expresión y la pasamos a minúsculas.
    entrada = input("Introduce la expresión: ")
    # Para controlar que la entrada no esté vacía ni sean espacios en blanco.
    entrada = entrada.strip()
    if entrada == "":
        print("¡Tienes que introducir una expresión!")
        return False
    entrada = entrada.lower()
    # Validamos si todas las palabras introducidas existen en el sistema.
    valida = validar_palabra_existente(entrada.split())
    if not valida:
        print("ERROR. Hay una palabra que no existe.")
        return False
    # Validamos la semántica y damos el resultado final.
    valida = validacion_semantica(entrada.split())
    if not valida:
        print("//////////ERROR DE SEMÁNTICA////////////")
        return False
    return True


# Cargamos los datos del nombre y puntuación del récord actual.
def cargar_record():
    global recordPuntuacion, jugadorRecord
    sql = "SELECT nombre, puntuacion FROM record"
    cur.execute(sql)
    listaRecords = cur.fetchall()
    if len(listaRecords) > 0:
        for x in listaRecords:
            jugadorRecord = x[0]
            recordPuntuacion = x[1]
    else:
        jugadorRecord = "Ninguno"
        recordPuntuacion = 0


# Recibe el número de la sala actual para usarla como ID a la hora de hacer
# la consulta y sacamos la descripción y las posibles salidas por pantalla.
def describe_habitacion(numeroHabitacion):
    sql = "SELECT descripcion FROM sala WHERE idsala = %s"
    val = (numeroHabitacion,)
    cur.execute(sql, val)
    for x in cur:
        print(str(numeroHabitacion) + ". " + x[0])
    sql = "SELECT salida FROM salida WHERE idsala = %s"
    val = (numeroHabitacion,)
    cur.execute(sql, val)
    posiblesSalidas = "Posibles salidas: "
    for x in cur:
        posiblesSalidas += x[0].capitalize()+" "
    print(posiblesSalidas)


# Recibe el número de la sala actual para usarla como ID a la hora de hacer
# la consulta y sacamos los nombres de los personajes en la sala por pantalla.
def enumera_personajes(numeroHabitacion):
    sql = "SELECT nombre FROM personaje WHERE idsala = %s"
    val = (numeroHabitacion,)
    cur.execute(sql, val)
    # Lo convertimos en lista para facilitar el conseguir su longitud para mayor claridad para el jugador.
    listaPersonajes = cur.fetchall()
    print("En la sala te encuentras con \'" + str(len(listaPersonajes)) + "\' personaje(s):")
    if len(listaPersonajes) == 0:
        print("")
    else:
        for x in listaPersonajes:
            print("-" + x[0].capitalize())


# Recibe el número de la sala actual para usarla como ID a la hora de hacer
# la consulta y sacamos los nombres de los objetos visibles en la sala por pantalla.
def enumera_objetos(numeroHabitacion):
    sql = "SELECT nombre FROM objeto WHERE idsala = %s"
    val = (numeroHabitacion,)
    cur.execute(sql, val)
    # Lo convertimos en lista para facilitar su iteración.
    listaObjetos = cur.fetchall()
    print("En la sala ves los siguientes objeto(s):")
    for x in listaObjetos:
        if x[0] in listaObjetosVisibles:
            print("-" + x[0].capitalize())


# Muestra nombre del jugador, récord actual y puntuación actual en la interfaz.
# Además, muestra un menú con los comandos.
def estado_puntuacion():
    print("Jugador: " + nombreJugador + " -- Récord: " + jugadorRecord + " -> " + str(recordPuntuacion) +
          "p -- Puntuación actual: " + str(puntuacionActual) + "p")
    print("| Inventario | Nuevo | Guardar | Cargar | Mapa | Ayuda |")


# Para desplazarse por las distintas habitaciones del mapa.
def moverse(numeroHabitacion):
    global salaJugador, puntuacionActual
    # Buscamos el ID de la sala a la que se sale mediante el ID de la
    # sala actual y la dirección a la que se quiere dirigir el jugador.
    sql = "SELECT idsalasalida FROM salida WHERE salida = %s AND idsala = %s"
    val = (palabras[1], numeroHabitacion)
    cur.execute(sql, val)
    listaSalidas = cur.fetchall()
    # Nos movemos a la nueva sala.
    if len(listaSalidas) > 0:
        for x in listaSalidas:
            salaJugador = x[0]
            # Si no la habíamos visitado antes, la añadimos a la lista y sumamos 100 puntos.
            if x[0] not in habitacionesVisitadas:
                habitacionesVisitadas.append(x[0])
                puntuacionActual += 100
    else:
        # Si la búsqueda no arroja resultados, lo mostramos por pantalla.
        print("No puedes ir al " + palabras[1] + ".")
        print("Sigues en la habitación " + str(salaJugador) + ".")


# Ejecutamos cada frase con su id.
def ejecutar_frase(idFrase):
    global puntuacionActual, monedasOro
    if idFrase == 1:  # Mirar mesa.
        # Buscamos la descripción por el nombre del objeto y la mostramos por pantalla.
        sql = "SELECT descripcion FROM objeto WHERE nombre = 'mesa'"
        cur.execute(sql)
        for x in cur:
            print(x[0])
        # Si todavía no habíamos encontrado el candelabro, ejecutamos su 'evento'.
        if "candelabro" not in listaObjetosVisibles and "candelabro" not in inventario and "candelabro" not in \
                listaObjetosUsados:
            respuesta = input("¡Has encontrado un candelabro! ¿Quieres cogerlo? -> ")
            # Añadimos el candelabro al inventario y +50 puntos.
            if respuesta.lower() == "si":
                print("Candelabro añadido al inventario.")
                inventario.append("candelabro")
                puntuacionActual += 50
            # No lo añadimos al inventario, pero pasa a ser un objeto visible por lo que podremos cogerlo directamente.
            else:
                print("Lo dejas donde está.")
                listaObjetosVisibles.append("candelabro")
    elif idFrase == 2:  # Mirar candelabro.
        # Buscamos la descripción por el nombre del objeto y la mostramos por pantalla.
        if "candelabro" in listaObjetosVisibles:
            sql = "SELECT descripcion FROM objeto WHERE nombre = 'candelabro'"
            cur.execute(sql)
            for x in cur:
                print(x[0])
        else:
            print("No puedes hacer eso.")
    elif idFrase == 3:  # Coger candelabro.
        # Si está visible, lo añadimos al inventario y +50 puntos.
        if "candelabro" in listaObjetosVisibles:
            print("Candelabro añadido al inventario")
            listaObjetosVisibles.remove("candelabro")
            inventario.append("candelabro")
            puntuacionActual += 50
        else:
            print("No puedes hacer eso.")
    elif idFrase == 4:  # Mirar cofre.
        # Buscamos la descripción por el nombre del objeto y la mostramos por pantalla.
        sql = "SELECT descripcion FROM objeto WHERE nombre = 'cofre'"
        cur.execute(sql)
        for x in cur:
            print(x[0])
    elif idFrase == 5:  # Mirar cuadro.
        # Buscamos la descripción por el nombre del objeto y la mostramos por pantalla.
        sql = "SELECT descripcion FROM objeto WHERE nombre = 'cuadro'"
        cur.execute(sql)
        for x in cur:
            print(x[0])
        # Si todavía no habíamos encontrado la llave, ejecutamos su 'evento'.
        if "llave" not in listaObjetosVisibles and "llave" not in inventario and "llave" not in listaObjetosUsados:
            respuesta = input("¡Has encontrado una llave escondida! ¿Quieres cogerla? -> ")
            # Añadimos la llave al inventario y +50 puntos.
            if respuesta.lower() == "si":
                print("Llave añadida al inventario.")
                inventario.append("llave")
                puntuacionActual += 50
            # No la añadimos al inventario, pero pasa a ser un objeto visible por lo que podremos cogerla directamente.
            else:
                print("La dejas donde está.")
                listaObjetosVisibles.append("llave")
    elif idFrase == 6:  # Mirar llave.
        # Buscamos la descripción por el nombre del objeto y la mostramos por pantalla.
        if "llave" in listaObjetosVisibles:
            sql = "SELECT descripcion FROM objeto WHERE nombre = 'llave'"
            cur.execute(sql)
            for x in cur:
                print(x[0])
        else:
            print("No puedes hacer eso.")
    elif idFrase == 7:  # Coger llave.
        # Si está visible, la añadimos al inventario y +50 puntos.
        if "llave" in listaObjetosVisibles:
            print("Llave añadida al inventario.")
            listaObjetosVisibles.remove("llave")
            inventario.append("llave")
            puntuacionActual += 50
        else:
            print("No puedes hacer eso.")
    elif idFrase == 8:  # Abrir cofre con llave.
        # Si tenemos la llave en el inventario, la usamos, y +100 monedas.
        if "llave" in inventario:
            print("Has usado la llave para abrir el cofre pero esta parece haber quedado atascada en la cerradura...")
            print("¡Dentro encuentras 100 monedas de oro y las añades a tu inventario!")
            inventario.remove("llave")
            listaObjetosUsados.append("llave")
            monedasOro += 100
        else:
            print("No puedes hacer eso.")
    elif idFrase == 9:  # Usar llave con cofre.
        # Si tenemos la llave en el inventario, la usamos, y +100 monedas.
        if "llave" in inventario:
            print("Has usado la llave para abrir el cofre pero esta parece haber quedado atascada en la cerradura...")
            print("¡Dentro encuentras 100 monedas de oro y las añades a tu inventario!")
            inventario.remove("llave")
            listaObjetosUsados.append("llave")
            monedasOro += 100
        else:
            print("No puedes hacer eso.")
    elif idFrase == 10:  # Mirar cuchillo.
        # Buscamos la descripción por el nombre del objeto y la mostramos por pantalla.
        sql = "SELECT descripcion FROM objeto WHERE nombre = 'cuchillo'"
        cur.execute(sql)
        for x in cur:
            print(x[0])
    elif idFrase == 11:  # Coger cuchillo.
        # Si está visible lo añadimos al inventario y +50 puntos.
        if "cuchillo" in listaObjetosVisibles:
            print("Cuchillo añadido al inventario")
            listaObjetosVisibles.remove("cuchillo")
            inventario.append("cuchillo")
            puntuacionActual += 50
        else:
            print("No puedes hacer eso.")
    elif idFrase == 12:  # Hablar con guerrero.
        # Si no le hemos atacado dirá una frase.
        if "cuchillo" not in listaObjetosUsados:
            sql = "SELECT frase1 FROM personaje WHERE nombre = 'guerrero'"
            cur.execute(sql)
            for x in cur:
                print(x[0])
        # Si le hemos atacado dirá otra y nos ofrecerá el escudo solo en caso de que no lo tengamos ya en el inventario.
        else:
            sql = "SELECT frase2 FROM personaje WHERE nombre = 'guerrero'"
            cur.execute(sql)
            for x in cur:
                print(x[0])
            if "escudo" not in inventario:
                respuesta = input("El guerrero te ofrece su escudo... ¿Quieres llevártelo? -> ")
                # Escudo añadido al ionventario y +50 puntos.
                if respuesta.lower() == "si":
                    print("Escudo añadido al inventario.")
                    inventario.append("escudo")
                    puntuacionActual += 50
                else:
                    print("Lo rechazas.")
    elif idFrase == 13:  # Empujar guerrero con cuchillo.
        # Usamos el cuchillo para atacar al guerrero.
        if "cuchillo" in inventario:
            print("Atacas al guerrero con el cuchillo y lo dejas malherido... Por desgracia el cuchillo se rompe a "
                  "consecuencia de tus estocadas.")
            inventario.remove("cuchillo")
            listaObjetosUsados.append("cuchillo")
        else:
            print("No puedes hacer eso.")
    elif idFrase == 14:  # Usar cuchillo con guerrero.
        # Usamos el cuchillo para atacar al guerrero.
        if "cuchillo" in inventario:
            print("Atacas al guerrero con el cuchillo y lo dejas malherido... Por desgracia el cuchillo se rompe a "
                  "consecuencia de tus estocadas.")
            inventario.remove("cuchillo")
            listaObjetosUsados.append("cuchillo")
        else:
            print("No puedes hacer eso.")
    elif idFrase == 15:  # Hablar con tendero.
        # Si no le hemos comprado dirá una frase.
        if "palanca" not in inventario and "palanca" not in listaObjetosUsados:
            sql = "SELECT frase1 FROM personaje WHERE nombre = 'tendero'"
            cur.execute(sql)
            for x in cur:
                print(x[0])
        # Si ya le hemos comprado dirá otra.
        else:
            sql = "SELECT frase2 FROM personaje WHERE nombre = 'tendero'"
            cur.execute(sql)
            for x in cur:
                print(x[0])
    elif idFrase == 16:  # Comprar palanca.
        # Si no la tenemos en inventario ni la hemos usado, la añadimos al inventario a cambio de 90 monedas y
        # +75 puntos.
        if "palanca" not in inventario and "palanca" not in listaObjetosUsados:
            if monedasOro >= 90:
                print("Compras la palanca al tendero a cambio de 90 monedas de oro y la añades a tu inventario.")
                inventario.append("palanca")
                monedasOro -= 90
                puntuacionActual += 75
            else:
                print("No tienes dinero suficiente...")
        else:
            print("No puedes hacer eso.")
    elif idFrase == 17:  # Vender candelabro.
        # Si tenemos el candelabro en inventario lo vendemos por 50 monedas.
        if "candelabro" in inventario:
            print("Vendes el valioso candelabro a cambio de 50 monedas de oro.")
            inventario.remove("candelabro")
            listaObjetosUsados.append("candelabro")
            monedasOro += 50
    elif idFrase == 18:  # Mirar puerta.
        # Buscamos la descripción por el nombre del objeto y la mostramos por pantalla.
        sql = "SELECT descripcion FROM objeto WHERE nombre = 'puerta'"
        cur.execute(sql)
        for x in cur:
            print(x[0])
    elif idFrase == 19:  # Abrir puerta con palanca.
        # Si tenemos la palanca en inventario, abrimos la puerta y desbloqueamos ir al este en la sala 5.
        if "palanca" in inventario:
            print("Colocas la palanca y la empujas consiguiendo así abrir la puerta...")
            inventario.remove("palanca")
            listaObjetosUsados.append("palanca")
    elif idFrase == 20:  # Usar palanca con puerta.
        # Si tenemos la palanca en inventario, abrimos la puerta y desbloqueamos ir al este en la sala 5.
        if "palanca" in inventario:
            print("Colocas la palanca y la empujas consiguiendo así abrir la puerta...")
            inventario.remove("palanca")
            listaObjetosUsados.append("palanca")


# Para comprobar el ID de la frase escrita y ejecutar la consecuencia correcta.
def comprueba_id_frase(numeroHabitacion):
    idFrase = 0
    sql = "SELECT idfrase FROM frases WHERE idsala = %s AND texto = %s"
    val = (numeroHabitacion, entrada,)
    cur.execute(sql, val)
    for x in cur:
        idFrase = x[0]
    if idFrase == 0:
        print("No puedes hacer eso.")
    else:
        ejecutar_frase(idFrase)


# Guardamos un registro de cada partida finalizada almacenando nombre y puntuación.
def guardar_registro():
    sql = "INSERT INTO puntuaciones (nombre, puntuacion) VALUES (%s, %s);"
    val = (nombreJugador, puntuacionActual,)
    cur.execute(sql, val)
    con.commit()


# En caso de que la puntuación obtenida sea mayor al récord la modificamos en su tabla.
def modificar_record():
    if puntuacionActual > recordPuntuacion:
        print("¡NUEVO RÉCORD DE PUNTUACIÓN!")
        if recordPuntuacion != 0:
            sql = "UPDATE record SET nombre = %s, puntuacion = %s WHERE id = 1"
            val = (nombreJugador, puntuacionActual,)
            cur.execute(sql, val)
            con.commit()
        else:
            sql = "INSERT INTO record (id ,nombre, puntuacion) VALUES (1,%s,%s);"
            val = (nombreJugador, puntuacionActual,)
            cur.execute(sql, val)
            con.commit()


# Devolvemos todas las variables del juego a su valor por defecto para reiniciar la partida.
def nuevo_juego():
    global salaJugador, puntuacionActual, monedasOro, listaObjetosVisibles, listaObjetosUsados, habitacionesVisitadas, \
        inventario, nombreJugador
    salaJugador = 1
    puntuacionActual = 100
    monedasOro = 0
    listaObjetosVisibles = ["mesa", "cuchillo", "cofre", "cuadro", "puerta"]
    listaObjetosUsados = []
    habitacionesVisitadas = [1]
    inventario = []
    print("Cargando nueva partida...")
    nombreJugador = input("Introduce tu nombre: ")
    cargar_record()


# Lógica del juego tras verificar la expresión introducida.
def juego():
    global salaJugador, puntuacionActual, monedasOro, listaObjetosVisibles, listaObjetosUsados, habitacionesVisitadas, \
        inventario, nombreJugador
    # Comprobamos si la expresión es un comando.
    if tokens[0] == "comando":
        # Muestra los objetos en inventario y las monedas.
        if palabras[0] == "inventario":
            print("////////////////////")
            print("Monedas de oro: " + str(monedasOro))
            for x in inventario:
                print("-" + x.capitalize())
            print("////////////////////")
        # Reinicia la partida.
        elif palabras[0] == "nuevo":
            respuesta = input("¿Quieres reiniciar la partida? (Se perderán todos los progresos no guardados...) -> ")
            if respuesta.lower() == "si":
                nuevo_juego()
            else:
                print("Reinicio cancelado.")
        # Almacena en la tabla 'partida' los datos de la partida actual.
        elif palabras[0] == "guardar":
            print("Guardando partida...")
            # Con el fin de facilitar el almacenamiento de los datos, pasamos la lista de habitacionesVisitadas a otra
            # lista de Strings en este caso.
            habitaciones = []
            for x in habitacionesVisitadas:
                habitaciones.append(str(x))
            sql = "INSERT INTO partida (nombre, sala, puntuacion, monedas, visibles, usados, visitadas, inventario)" \
                  " VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"
            val = (nombreJugador, salaJugador, puntuacionActual, monedasOro, ' '.join(listaObjetosVisibles),
                   ' '.join(listaObjetosUsados), ' '.join(habitaciones), ' '.join(inventario),)
            cur.execute(sql, val)
            con.commit()
        # Seleccionamos los datos de todas las partidas guardadas, las mostramos en una prettytable y pedimos al jugador
        # elegir la que quiere cargar. Una vez cargada, asignamos esos datos a nuestras variables de juego.
        elif palabras[0] == "cargar":
            listaPartidas = []
            sql = "SELECT * FROM partida"
            cur.execute(sql)
            for x in cur:
                listaPartidas.append(x)
            if len(listaPartidas) > 0:
                tabla = PrettyTable()
                tabla.field_names = ["ID", "Nombre jugador", "Sala", "Puntuación", "Monedas"]
                for x in listaPartidas:
                    tabla.add_row([x[0], x[1], x[2], x[3], x[4]])
                print(tabla)
                # Comprobamos que el ID introducido es válido y que es un entero.
                ultimoId = listaPartidas[-1][0]
                idPartida = input("Indica el id de la partida que quieres cargar: ")
                if not idPartida.isnumeric():
                    print("ID de partida no válido...")
                elif 0 < int(idPartida) <= ultimoId:
                    print("Cargando partida...")
                    sql = "SELECT * FROM partida WHERE idpartida = %s"
                    val = (idPartida,)
                    cur.execute(sql, val)
                    habitaciones = []
                    for x in cur:
                        nombreJugador = x[1]
                        salaJugador = x[2]
                        puntuacionActual = int(x[3])
                        monedasOro = int(x[4])
                        listaObjetosVisibles = x[5].split()
                        listaObjetosUsados = x[6].split()
                        habitaciones = x[7].split()
                        inventario = x[8].split()
                    habitacionesVisitadas.clear()
                    for x in habitaciones:
                        habitacionesVisitadas.append(int(x))
                else:
                    print("ID de partida no válido...")
            else:
                print("No hay partidas guardadas.")
        # Mostramos un dibujo del mapa con la posición del jugador actualizada.
        elif palabras[0] == "mapa":
            print("_____________________________________")
            print("|1		    |2		     |5		    |")
            print("|		    |		     |		    |")
            if salaJugador == 1:
                print("|	  X                           ")
            elif salaJugador == 2:
                print("|	              X              ")
            elif salaJugador == 5:
                print("|	                          X  ")
            else:
                print("|		     		      		     ")
            print("|		    |		     |		    |")
            print("| 		    |		     |		    |")
            print("|____   ____|____   _____|__________|")
            print("|3		    |4		     |")
            print("|		    |		     |")
            if salaJugador == 3:
                print("|     X     |            |")
            elif salaJugador == 4:
                print("|           |     X      |")
            else:
                print("|		    |		     |")
            print("|		    |		     |")
            print("|___________|____________|")
        # Mostramos diferentes pistas teniendo en cuenta distintos eventos durante el desarrollo de la partida.
        elif palabras[0] == "ayuda":
            sql = "SELECT texto FROM pista where id = %s"
            val = (0,)
            if "palanca" not in inventario and "palanca" not in listaObjetosUsados and 4 not in habitacionesVisitadas:
                val = (1,)
            elif "cuchillo" in listaObjetosUsados and "escudo" not in inventario:
                val = (2,)
            elif "palanca" not in inventario and "palanca" not in listaObjetosUsados and 4 in habitacionesVisitadas \
                    and monedasOro > 90:
                val = (3,)
            elif "palanca" not in inventario and "palanca" not in listaObjetosUsados and 4 in habitacionesVisitadas \
                    and monedasOro < 90:
                val = (4,)
            elif "palanca" in inventario or "palanca" in listaObjetosUsados:
                val = (5,)
            cur.execute(sql, val)
            for x in cur:
                print(x[0])
    # En caso de no ser un comando lo tratamos como una expresión 'normal'. Diferenciamos entre
    # moverse o frase de acción comprobando antes la sala del jugador, ya que la 5 funciona de forma especial.
    elif salaJugador == 5:
        if tokens[0] == "verboIr":
            if palabras[1] != "este":
                moverse(salaJugador)
            else:
                # Gestionamos el final de la partida.
                if "palanca" not in listaObjetosUsados:
                    print("No puedes salir porque la puerta está cerrada.")
                else:
                    # Si tenemos el escudo se gana y +1000 puntos.
                    if "escudo" in inventario:
                        print("Sales triunfante del castillo con la sensación de que todo lo ocurrido no fue más que "
                              "una pesadilla.")
                        print("De repente sientes una especie de escozor en todo tu cuerpo... ¡Radiación! Sigues tu "
                              "instinto y sacas el escudo que recogiste del guerrero que resulta tener poderes mágicos "
                              "que te permiten protegerte de la radiación... Huyes de la zona a toda velocidad.")
                        print("////////¡ENHORABUENA, HAS VENCIDO!////////")
                        puntuacionActual += 1000
                    # Si no, se pierde.
                    else:
                        print("Sales triunfante del castillo con la sensación de que todo lo ocurrido no fue más que "
                              "una pesadilla.")
                        print("De repente sientes una especie de escozor en todo tu cuerpo... ¡Radiación! "
                              "inmediatamente te arrepientes de no haber buscado algo que pudiera ayudarte dentro "
                              "del castillo mientras las quemaduras te consumen...")
                        print("////////HAS MUERTO////////")
                    # Finalmente, mostramos puntuación obtenida, récord, guardamos el registro de la partida y
                    # gestionamos nuevo récord si se diese el caso.
                    print("PUNTUACIÓN TOTAL: " + str(puntuacionActual))
                    print("RÉCORD: " + str(recordPuntuacion))
                    guardar_registro()
                    modificar_record()
                    # Damos la opción de empezar de nuevo o salir.
                    respuesta = input("¿Otra partida? -> ")
                    if respuesta.lower() == "si":
                        nuevo_juego()
                    else:
                        print("¡Adiós cobarde!")
                        exit()
        elif tokens[0] == "verboNormal":
            comprueba_id_frase(salaJugador)
    elif tokens[0] == "verboIr":
        moverse(salaJugador)
    else:
        comprueba_id_frase(salaJugador)


# Función principal con el bucle del juego.
def main():
    global nombreJugador
    print("Bienvenido/a a CastleManiac")
    print("By: Javier Tomé")
    print("En el juego puedes mirar/coger/usar objetos, hablar con personajes, ir norte/sur/este/oeste y"
          " tu objetivo es escapar con vida del castillo. ¡Buena suerte!")
    nombreJugador = input("Introduce tu nombre: ")
    cargar_record()
    while True:
        print("----------------------------------------------------------------------")
        describe_habitacion(salaJugador)
        enumera_personajes(salaJugador)
        enumera_objetos(salaJugador)
        estado_puntuacion()
        if introduce_expresion():
            juego()
        print("----------------------------------------------------------------------\n")


# Ejecutamos el programa
main()
