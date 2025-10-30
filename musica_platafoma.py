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

    def __init__(self):
        self.nombre: str
        self.canciones: list[int]


    def anadir_cancion(id_cancion: int) -> bool:

        pass

    def quitar_cancion(id_cancion: int) -> bool:

    
        pass

class PlataformaMusical: 

    def __init__(self):

        # NOTA: Esto no crea los atributos, solo los anota con tipos!! ":" define el tipo y "=" los crea
        self.canciones: list[Cancion] = []  # lista vacía inicial
        self.listas: list[ListaReproduccion] = []  # lista vacía inicial

    # -- Menú de gestión de canciones --

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
        pass

    def eliminar_cancion(self, id: int) -> bool:
        pass

    # -- Menú de gestión de listas --

    def crear_lista(self, nombre: str) -> bool:
        pass

    def borrar_lista(self, nombre: str) -> bool:
        pass

    def obtener_lista(self, nombre: str) -> ListaReproduccion:
        pass
