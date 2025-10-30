#!/usr/bin/env python3
"""Interfaz por consola para la PlataformaMusical (parte 1)."""
from musica_platafoma import PlataformaMusical

def pedir_int(a):
   
    return int(input(a))


# ----------------------    Menú de gestión de canciones.   ---------------------------
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
            
            #Esto es un bucle para comprobar que el valor de duración es un número entero 
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
            print("\n-- Modificar canción --")
            if len(plataforma.canciones) != 0:
                print("Canciones disponibles: ")
                for canciones in plataforma.canciones:
                    print(f"{canciones.id}) {canciones.titulo} - {canciones.artista} ({canciones.duracion} segundos)")

                # REVISAR !!
                nuevo_titulo = input("Nuevo título (enter para dejar): ")
                if nuevo_titulo == "":
                    nuevo_titulo = canciones.titulo

                nuevo_artista = input("Nuevo artista (enter para dejar): ")
                if nuevo_artista == "":
                    nuevo_artista = canciones.artista

                nueva_duracion = int(input("Nueva duración (enter para dejar): "))
                if nueva_duracion == "":
                    nueva_duracion = canciones.duracion

                nuevo_genero = input("Nuevo género (enter para dejar): ")
                if nuevo_genero == "":
                    nuevo_genero = canciones.genero

                nueva_ruta = input("Nueva ruta a archivo MP3 (enter para dejar): ")
                if nueva_ruta == "":
                    nueva_ruta = canciones.archivo_mp3

                plataforma.editar_cancion(nuevo_titulo, nuevo_artista, nueva_duracion, nuevo_genero, nueva_ruta)
                print("Modificado")

            else:
                print("Lo sentimos. Actualmente no hay canciones disponibles.")

        # Para eliminar una canción
        elif opc == 3:
            print("\n-- Eliminar canción --")
            if len(plataforma.canciones) != 0:
                print("Canciones disponibles: ")
                for canciones in plataforma.canciones:
                    print(f"{canciones.id}) {canciones.titulo} - {canciones.artista} ({canciones.duracion})")

                #Preguntar !! Lo del 0, no entiendo exactamente a donde habría que volver 
                cancion_eliminada = int(input("Selecciona número de la canción (0 para cancelar): "))
                plataforma.eliminar_cancion(cancion_eliminada)
                print("Eliminada")
            else:
                print("Lo sentimos. Actualmente no hay canciones disponibles.")

        #Para mostrar las canciones que están en la lista 
        elif opc == 4:
            print("\n-- Listar canciones --")
            for canciones in plataforma.canciones:
                print(f"{canciones.id}) {canciones.titulo} - {canciones.artista} ({canciones.duracion}) [{canciones.genero}] --> {canciones.archivo_mp3}")

        #Para volver al menú principal
        elif opc == 0:
            main()

        else:
            print("Opción inválida")


# --------------------------- Menú de gestión de listas -----------------------------

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
            nombre_lista = input("Nombre de la lista")
            plataforma.crear_lista(nombre_lista)
            print("Creada")

        if opc == 2:
            print("\n--- Eliminar lista ---")
            if len(plataforma.listas) != 0:
                print("Listas disponibles: ")
                idx = 1
                for listas in plataforma.listas:
                    print(f"{idx}) {listas.nombre}")
                    idx += 1

                # Preguntar !! Lo del 0, no entiendo exactamente a donde habría que volver
                lista_eliminada = int(input("Selecciona el número de la lsita que quieras eliminar: "))
                plataforma.borrar_lista(lista_eliminada)
                print("Lista eliminada")
            else:
                print("Lo sentimos. Actualmente no hay canciones disponibles.")

    pass

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
