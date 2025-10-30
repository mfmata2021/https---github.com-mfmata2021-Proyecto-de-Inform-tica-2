#!/usr/bin/env python3
"""Interfaz por consola para la PlataformaMusical (parte 1)."""
from musica_platafoma import PlataformaMusical

def pedir_int(a):
 
 #Bucle para gestionar valores inválidos a la hora de entrar a los menús 
    while True: 
        try: 
            valor = int(input(a))
            break
        except ValueError:
            print("Valor inválido. Intente de nuevo")
    return valor

# -----------------------------------------------------------------------------------
# ----------------------    Menú de gestión de canciones.   -------------------------
# -----------------------------------------------------------------------------------

def menu_canciones(plataforma: PlataformaMusical):

    while True:
        print("\n-- Gestión de canciones --")
        print("1) Añadir canción")
        print("2) Modificar canción")
        print("3) Eliminar canción")
        print("4) Listar canciones")
        print("0) Volver")
        opc = pedir_int("> ")

        # Para añadir una canción
        if opc == 1:
            print("\n-- Añadir canción --")
            titulo = input("Título: ")
            artista = input("Artista: ")

            # Esto es un bucle para comprobar que el valor de duración es un número entero
            while True: 
                try:
                    duracion = int(input("Duración (segundos): "))
                    break
                except ValueError: #El except tiene que incluir el ValueError para que funcione 
                    print("El valor introducido debe ser un número. Inténtelo de nuevo.")

            genero = input("Género: ")
            ruta = input("Ruta a archivo MP3: ")
            if plataforma.registrar_cancion(titulo, artista, duracion, genero, ruta): #Si todo es correcto esto es un TRUE
                print("Canción añadida")
            else: #Si no es un FALSE
                print("No se pudo añadir la canción. Ya existe.")

        # Para modificar una canción
        elif opc == 2:
            print("\n-- Modificar canción --\n")
            if len(plataforma.canciones) != 0:
                print("Canciones disponibles: ")
                for canciones in plataforma.canciones:
                    print(f"{canciones.id}) {canciones.titulo} - {canciones.artista} ({canciones.duracion} segundos)")

                # Para que el usuario, de la lista de canciones disponibles escoja cual quiere modificar
                try:
                    id_cancion = int(input("\nIntroduce el número de la canción que quieras modificar: "))
                except ValueError:
                    print("El valor introducido debe ser un número. Inténtelo de nuevo.")

                # Para comprobar que el valor introducido no es menor que 0 ni mayor que el num de id en la lista
                if (id_cancion < 1) or (id_cancion > len(plataforma.canciones)):
                    print("Número fuera de rango.")

                else:
                    cancion = plataforma.canciones[id_cancion - 1] #IMPORTANTE el -1 es porque las listas empiezan desde 0 y nuestros Id en 1, por lo que si escojo la cancion con id 1, sería la cancion en la posocion 0

                nuevo_titulo = input("Nuevo título (enter para dejar igual): ") or cancion.titulo
                nuevo_artista = input("Nuevo artista (enter para dejar igual): ") or cancion.artista

                # CONTROL DE ERRORES PARA DURACIÓN

                nueva_duracion_str = input("Nueva duración (enter para dejar igual): ")
                if nueva_duracion_str == "":
                    nueva_duracion = cancion.duracion
                else:
                    try:
                        nueva_duracion = int(nueva_duracion_str)
                    except ValueError:
                        print("Duración no válida. Se mantiene la anterior.")
                        nueva_duracion = cancion.duracion

                nuevo_genero = input("Nuevo género (enter para dejar igual): ") or cancion.genero
                nueva_ruta = input("Nueva ruta (enter para dejar igual): ") or cancion.archivo_mp3

                plataforma.editar_cancion(id_cancion, nuevo_titulo, nuevo_artista, nueva_duracion, nuevo_genero, nueva_ruta)

                # REVISAR! En algunas pruebas me aparecía esto doble, una donde aparecia "segundos" y otra donde no
                print(" Lista de canciones actulizada: ")
                for canciones in plataforma.canciones:
                    print(f"{canciones.id}) {canciones.titulo} - {canciones.artista} ({canciones.duracion} segundos)")

            else:
                print("Lo sentimos. Actualmente no hay canciones disponibles.")

        # Para eliminar una canción
        elif opc == 3:
            print("\n-- Eliminar canción --")
            if len(plataforma.canciones) != 0:
                print("Canciones disponibles: ")
                for canciones in plataforma.canciones:
                    print(f"{canciones.id}) {canciones.titulo} - {canciones.artista} ({canciones.duracion} segundos)")

                # Preguntar !! Lo del 0, no entiendo exactamente a donde habría que volver
                # Esto es un bucle para comprobar que el valor de duración es un número entero
                while True:
                    try:
                        cancion_eliminada = int(input("\nSelecciona el id de la canción que quieras eliminar: "))
                        if (cancion_eliminada < 1) or cancion_eliminada > len(plataforma.canciones):
                            print("No hay ninguna canción con ese ID. Intente de nuevo")
                        else:
                            if plataforma.eliminar_cancion(cancion_eliminada):
                                print("Canción eliminada")
                            else:
                                print("No se pudo eliminar la canción escogida")
                            break
                    except ValueError:  # El except tiene que incluir el ValueError para que funcione
                        print(
                            "El valor introducido debe ser un número. Inténtelo de nuevo."
                        )
            else:
                print("Lo sentimos. Actualmente no hay canciones disponibles.")

        # Para mostrar las canciones que están en la lista
        elif opc == 4:
            print("\n-- Listar canciones --")

            if len(plataforma.canciones) != 0:
                for canciones in plataforma.canciones:
                    print(f"{canciones.id}) {canciones.titulo} - {canciones.artista} ({canciones.duracion} segundos) [{canciones.genero}] --> {canciones.archivo_mp3}")
            else:
                print("Actualmente no hay canciones disponibles\n")
        # Para volver al menú principal
        elif opc == 0:
            break

        else:
            print("Opción inválida")

# -----------------------------------------------------------------------------------
# --------------------------- Menú de gestión de listas -----------------------------
# -----------------------------------------------------------------------------------

def menu_listas(plataforma: PlataformaMusical):

    while True:
        print("\n-- Gestión de listas --")
        print("1) Crear lista")
        print("2) Eliminar lista")
        print("3) Ver contenido de lista")
        print("4) Añadir canciones a lista")
        print("5) Eliminar canción de lista")
        print("0) Volver")
        opc = pedir_int("> ")

        if opc == 1:
            print("\n--- Crear lista ---")
            nombre_lista = input("Nombre de la lista: ")
            if plataforma.crear_lista(nombre_lista, canciones=0): #Esto inicializa la lista con 0 canciones 
                print("Creada")
            else:
                print("Lo siento. No se ha podido crear la lista, escoge otro nombre")

        if opc == 2:
            print("\n--- Eliminar lista ---")
            if len(plataforma.listas) != 0:
                print("Listas disponibles: ")
                idx = 1
                for listas in plataforma.listas:
                    print(f"{idx}) {listas.nombre} ({listas.canciones} canciones)")
                    idx += 1

                # Preguntar !! Lo del 0, no entiendo exactamente a donde habría que volver
                lista_eliminada = input("\nSelecciona el nombre de la lista que quieras eliminar: ")
                plataforma.borrar_lista(lista_eliminada)
                print("Lista eliminada")
            else:
                print("Lo sentimos. Actualmente no hay listas disponibles.")

        if opc == 3:
            print("\n--- Ver contenidos de listas ----")
            
            if len(plataforma.listas) != 0:
                print(f"Listas disponibles: ")
                for idx, listas in enumerate(plataforma.listas, start=1):
                    print(f"{idx}) {listas.nombre} ({listas.canciones} canciones)")



                #Bucle para asegurarnos que el usurio introduce un nombre válido de lista 
                while True:
                    ver_contenido = input("\nIndica el nombre de la lista que quieres visualizar: ")

                    lista_encontrada = plataforma.obtener_lista(ver_contenido)  #Aquí se devuelve el objeto LisaReproducción

                    if lista_encontrada:
                        print(f"\n--- Contenido de '{lista_encontrada.nombre}' ---")
                        if len(lista_encontrada.canciones) == 0:
                            print("Esta lista no tiene canciones.")
                        else:
                            for idx, cancion in enumerate(lista_encontrada.canciones, start=1):
                                print(f"{idx}. {cancion}")
                        break  # salimos del while

                    else:
                        print("No existe una lista con ese nombre. Intenta de nuevo.")

            else: 
                print("No tienes listas para mostrar")

        
        if opc == 4:
            print("-- Añadir canciones a lista --")

        if opc == 5:
            print("-- Eliminar canción de lista --")


        if opc == 0:
            break 

# -----------------------------------------------------------------------------------
# --------------------------- Menú de gestión de reproducción  -----------------------------
# -----------------------------------------------------------------------------------
def menu_reproduccion(plataforma: PlataformaMusical):
    pass

def main():
    plataforma = PlataformaMusical()
    while True:
        print('\n=== Plataforma Musical ===')
        print('1) Gestionar canciones')
        print('2) Gestionar listas')
        print('3) Reproducción')
        print('0) Salir')
        opc = pedir_int('> ')
        if opc == 1:
            menu_canciones(plataforma)
        elif opc == 2:
            menu_listas(plataforma)
        elif opc == 3:
            menu_reproduccion(plataforma)
        elif opc == 0:
            print('Hasta luego')
            break
        else:
            print('Opción inválida')


if __name__ == '__main__':
    main()
