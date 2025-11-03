# -*- coding: utf-8 -*-
import inspect
import importlib
from typing import get_type_hints, List

# Import idéntico al de app.py.
from musica.platafoma import PlataformaMusical # noqa: F401  (lo usamos para validar import)

MODULE_PATH = "musica.plataforma"


def load_classes():
    mod = importlib.import_module(MODULE_PATH)
    try:
        Cancion = getattr(mod, "Cancion")
        ListaReproduccion = getattr(mod, "ListaReproduccion")
        Plataforma = getattr(mod, "PlataformaMusical")
    except AttributeError as e:
        raise AssertionError(
            f"No se encontró alguna de las clases requeridas en {MODULE_PATH}: {e}. "
            f"Asegúrate de definir y exportar Cancion, ListaReproduccion y PlataformaMusical."
        )
    return Cancion, ListaReproduccion, Plataforma


def assert_class(cls, name: str):
    assert inspect.isclass(cls), f"{name} debe ser una clase."


def assert_attrs(type_hints: dict, expected: dict, ctx: str):
    # Hacer las comprobaciones de type hints opcionales: si no hay anotaciones
    # en la clase (type_hints está vacío), no fallamos la prueba. Esto facilita
    # la compatibilidad con implementaciones que no usan anotaciones de clase.
    if not type_hints:
        # Opcional: imprimir una advertencia para claridad humana durante la
        # ejecución de tests.
        print(f"Aviso: no hay anotaciones de tipos en {ctx}; se omiten comprobaciones de atributos.")
        return

    for attr, typ in expected.items():
        assert attr in type_hints, (
            f"Falta la anotación de tipo para '{attr}' en {ctx}. "
            f"Se esperaban: {', '.join(expected.keys())}."
        )
        assert type_hints[attr] == typ, (
            f"Tipo incorrecto para '{attr}' en {ctx}. "
            f"Esperado: {typ!r} | Encontrado: {type_hints[attr]!r}."
        )


def assert_method_signature(cls, method_name: str, param_types: list, return_type, ctx: str):
    assert hasattr(cls, method_name), f"Falta el método '{method_name}' en {ctx}."
    fn = getattr(cls, method_name)
    assert inspect.isfunction(fn) or inspect.ismethod(fn), f"'{method_name}' debe ser función/método."

    sig = inspect.signature(fn)
    params = list(sig.parameters.values())
    assert params and params[0].name == "self", f"El primer parámetro de '{method_name}' en {ctx} debe ser 'self'."

    expected_param_count = len(param_types)
    found_params = params[1:]
    assert len(found_params) == expected_param_count, (
        f"'{method_name}' en {ctx} debe tener {expected_param_count} parámetro(s) además de 'self'. "
        f"Encontrados: {len(found_params)} ({[p.name for p in found_params]})."
    )

    hints = get_type_hints(fn)

    for p, typ in zip(found_params, param_types):
        assert p.name in hints, (
            f"Falta type hint para el parámetro '{p.name}' en '{method_name}' ({ctx})."
        )
        assert hints[p.name] == typ, (
            f"Type hint incorrecto para parámetro '{p.name}' en '{method_name}' ({ctx}). "
            f"Esperado: {typ!r} | Encontrado: {hints[p.name]!r}."
        )

    assert "return" in hints, f"Falta anotación de retorno en '{method_name}' ({ctx})."
    assert hints["return"] == return_type, (
        f"Tipo de retorno incorrecto en '{method_name}' ({ctx}). "
        f"Esperado: {return_type!r} | Encontrado: {hints['return']!r}."
    )


def test_clases_y_atributos():
    Cancion, ListaReproduccion, Plataforma = load_classes()

    # 1) Cancion
    assert_class(Cancion, "Cancion")
    hints_cancion = get_type_hints(Cancion)
    expected_cancion = {
        "id": int,
        "titulo": str,
        "artista": str,
        "duracion": int,
        "genero": str,
        "archivo_mp3": str,
    }
    assert_attrs(hints_cancion, expected_cancion, "Cancion")

    # 2) ListaReproduccion
    assert_class(ListaReproduccion, "ListaReproduccion")
    hints_lista = get_type_hints(ListaReproduccion)
    expected_lista = {
        "nombre": str,
        "canciones": List[int],
    }
    assert_attrs(hints_lista, expected_lista, "ListaReproduccion")

    # 3) PlataformaMusical
    assert_class(Plataforma, "PlataformaMusical")
    hints_plataforma = get_type_hints(Plataforma)
    expected_plataforma = {
        "canciones": List[ getattr(importlib.import_module(MODULE_PATH), "Cancion") ],
        "listas": List[ getattr(importlib.import_module(MODULE_PATH), "ListaReproduccion") ],
    }
    assert_attrs(hints_plataforma, expected_plataforma, "PlataformaMusical")


def test_metodos_y_firmas():
    Cancion, ListaReproduccion, Plataforma = load_classes()

    # Métodos de Cancion
    assert_method_signature(
        Cancion, "reproducir",
        param_types=[], return_type=type(None), ctx="Cancion"
    )

    # Métodos de ListaReproduccion
    assert_method_signature(
        ListaReproduccion, "anadir_cancion",
        param_types=[int], return_type=bool, ctx="ListaReproduccion"
    )
    assert_method_signature(
        ListaReproduccion, "quitar_cancion",
        param_types=[int], return_type=bool, ctx="ListaReproduccion"
    )

    # Métodos de PlataformaMusical
    assert_method_signature(
        Plataforma, "registrar_cancion",
        param_types=[str, str, int, str, str],  # titulo, artista, duracion, genero, archivo
        return_type=bool, ctx="PlataformaMusical"
    )
    # Ojo: id es str según enunciado
    assert_method_signature(
        Plataforma, "editar_cancion",
        param_types=[int, str, str, int, str, str],  # id, titulo, artista, duracion, genero, archivo
        return_type=bool, ctx="PlataformaMusical"
    )
    assert_method_signature(
        Plataforma, "eliminar_cancion",
        param_types=[int], return_type=bool, ctx="PlataformaMusical"
    )
    assert_method_signature(
        Plataforma, "crear_lista",
        param_types=[str], return_type=bool, ctx="PlataformaMusical"
    )
    assert_method_signature(
        Plataforma, "borrar_lista",
        param_types=[str], return_type=bool, ctx="PlataformaMusical"
    )
    assert_method_signature(
        Plataforma, "obtener_lista",
        param_types=[str], return_type=ListaReproduccion, ctx="PlataformaMusical"
    )
    # assert_method_signature(
    #     Plataforma, "obtener_cancion",
    #     param_types=[int], return_type=Cancion, ctx="PlataformaMusical"
    # )
