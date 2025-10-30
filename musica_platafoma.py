class Cancion:

    def __init__(self,id, titulo, artista,duracion,genero,archivo):
        self.id: int = id
        self.titulo: str = titulo
        self.artista: str = artista
        self.duracion: int = duracion
        self.genero: str = genero
        self.archivo_mp3: str =  archivo

    def reproducir() -> None:
        pass

class ListaReproduccion: 

    def __init__(self, nombre, canciones):
        self.nombre: str = nombre
        self.canciones: list[int] = canciones


    def anadir_cancion(self, id_cancion: int) -> bool:

        pass

    def quitar_cancion(self, id_cancion: int) -> bool:

    
        pass

class PlataformaMusical: 

    def __init__(self):

        # NOTA: Esto no crea los atributos, solo los anota con tipos!! ":" define el tipo y "=" los crea
        self.canciones: list[Cancion] = []  # lista vacía inicial
        self.listas: list[ListaReproduccion] = []  # lista vacía inicial [[],[],[]]

    # -----------------------------------------------------------------------------------
    # ----------------------    Menú de gestión de canciones.   -------------------------
    # -----------------------------------------------------------------------------------

    def registrar_cancion(self, titulo:  str,  artista:  str,  duracion:  int, 
    genero: str, archivo: str) -> bool:

        for c in self.canciones: 
            if c.titulo == titulo:
                return False
        nueva_cancion = Cancion(len(self.canciones) + 1, titulo, artista, duracion, genero, archivo)
        self.canciones.append(nueva_cancion)
        return True

    def editar_cancion(self, id:  int,  titulo:  str,  artista:  str,  duracion: 
    int, genero: str, archivo: str) -> bool:

        for c in self.canciones:
            if c.id == id:
                c.titulo = titulo
                c.artista = artista
                c.duracion = duracion
                c.genero = genero
                c.archivo_mp3 = archivo
                return True
        return False

    # Aquí necesito eliminar la canción del ID correspondiente y además gestionar que el resto de canciones que queden en la lista actualicen sus ID's
    def eliminar_cancion(self, id: int) -> bool:

        for c in self.canciones: 
            if c.id == id:
                self.canciones.remove(c)

                # Para reacomodar los ID's de las canciones despues de eliminar la canción
                nuevo_id = 1
                for ca in self.canciones:
                    ca.id = nuevo_id #Recorre la lista de canciones y reasigna de primera a última los ID
                    nuevo_id += 1
                return True

        return False

    # -----------------------------------------------------------------------------------
    # --------------------------- Menú de gestión de listas -----------------------------
    # -----------------------------------------------------------------------------------

    def crear_lista(self, nombre: str, canciones) -> bool:

        for l in self.listas:
            if l.nombre == nombre:
                return False #Esto no permite que haya dos listas con el mismo nombre 
        
        nueva_lista = ListaReproduccion(nombre, canciones)
        self.listas.append(nueva_lista)
        return True

    def borrar_lista(self, nombre: str) -> bool:

        for l in self.listas:
            if l.nombre == nombre:
                self.listas.remove(l)
                return True
        return False

    def obtener_lista(self, nombre: str) -> ListaReproduccion:

        for l in self.listas:
            if l.nombre == nombre:
                return  l 
        return None
