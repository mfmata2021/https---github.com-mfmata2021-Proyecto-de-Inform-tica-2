# -*- coding: utf-8 -*-
import ast
import inspect
import importlib
from typing import List
import pytest

MODULE_PATH = "musica.plataforma"

def load_module_and_classes():
    mod = importlib.import_module(MODULE_PATH)
    Cancion = getattr(mod, "Cancion")
    ListaReproduccion = getattr(mod, "ListaReproduccion")
    PlataformaMusical = getattr(mod, "PlataformaMusical")
    return mod, Cancion, ListaReproduccion, PlataformaMusical


# ---------------------------
# 1) Evitar input() en métodos
# ---------------------------
def test_no_input_calls_in_methods():
    mod, *_ = load_module_and_classes()
    src = inspect.getsource(mod)
    tree = ast.parse(src)

    # Clases objetivo
    target_classes = {"Cancion", "ListaReproduccion", "PlataformaMusical"}
    offenders = []

    class MethodInputVisitor(ast.NodeVisitor):
        def __init__(self):
            self.in_method = False
            self.class_name = None
            self.method_name = None

        def visit_ClassDef(self, node: ast.ClassDef):
            if node.name in target_classes:
                self.class_name = node.name
                for b in node.body:
                    if isinstance(b, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        # Consideramos cualquier método de instancia o clase
                        prev_in_method = self.in_method
                        prev_method = self.method_name
                        self.in_method = True
                        self.method_name = b.name
                        self.visit(b)
                        self.in_method = prev_in_method
                        self.method_name = prev_method
                self.class_name = None
            # Continuar recorriendo
            self.generic_visit(node)

        def visit_Call(self, node: ast.Call):
            # input(...) como Name
            is_input_name = isinstance(node.func, ast.Name) and node.func.id == "input"
            # o como atributo (poco habitual, pero por si acaso)
            is_input_attr = isinstance(node.func, ast.Attribute) and node.func.attr == "input"
            if self.in_method and (is_input_name or is_input_attr):
                offenders.append((self.class_name, self.method_name, node.lineno))
            self.generic_visit(node)

    visitor = MethodInputVisitor()
    visitor.visit(tree)

    assert not offenders, (
        "No se permite usar 'input()' dentro de métodos de las clases requeridas.\n"
        + "\n".join(f"  - {cls}.{m} en línea {lineno}" for cls, m, lineno in offenders)
    )


# ---------------------------
# 2) Inicializaciones seguras en __init__
#    - Si se puede instanciar:
#        * 'canciones' y 'listas' en PlataformaMusical son listas (no None)
#        * No comparten la misma lista entre instancias
#        * En ListaReproduccion, 'canciones' es lista no None y no compartida
# ---------------------------
def try_instantiate(cls, suggested_args=()):
    """Intenta instanciar con 0 args; si falla, prueba con suggested_args; si falla, devuelve None."""
    try:
        return cls()
    except TypeError:
        try:
            return cls(*suggested_args)
        except Exception:
            return None

def test_init_lists_plataforma_y_lista():
    mod, Cancion, ListaReproduccion, PlataformaMusical = load_module_and_classes()

    # PlataformaMusical: intentamos instanciar sin args
    p1 = try_instantiate(PlataformaMusical)
    if p1 is None:
        pytest.skip("PlataformaMusical no admite constructor sin argumentos; se omite esta verificación.")

    # Debe tener atributos y ser listas
    assert hasattr(p1, "canciones"), "PlataformaMusical debe tener atributo 'canciones'."
    assert hasattr(p1, "listas"), "PlataformaMusical debe tener atributo 'listas'."
    assert isinstance(p1.canciones, list), "'canciones' debe ser list en la instancia de PlataformaMusical."
    assert isinstance(p1.listas, list), "'listas' debe ser list en la instancia de PlataformaMusical."
    assert p1.canciones is not None, "'canciones' no debe ser None."
    assert p1.listas is not None, "'listas' no debe ser None."

    # No compartir listas entre instancias
    p2 = try_instantiate(PlataformaMusical)
    assert p2 is not None, "No se pudo instanciar una segunda PlataformaMusical para comprobar mutabilidad."
    assert id(p1.canciones) != id(p2.canciones), "Cada instancia debe tener su propia lista 'canciones'."
    assert id(p1.listas) != id(p2.listas), "Cada instancia debe tener su propia lista 'listas'."

    # ListaReproduccion:
    # Intentamos deducir si requiere 'nombre' como único parámetro
    # Si no podemos instanciar, saltamos con skip (no fallamos el test del alumnado).
    lr = try_instantiate(ListaReproduccion, suggested_args=("Mi Lista",))
    if lr is None:
        pytest.skip("ListaReproduccion no se puede instanciar (p. ej., falta 'nombre' o firma distinta); se omite esta verificación.")

    assert hasattr(lr, "canciones"), "ListaReproduccion debe tener atributo 'canciones'."
    assert isinstance(lr.canciones, list), "'canciones' debe ser list en la instancia de ListaReproduccion."
    assert lr.canciones is not None, "'canciones' no debe ser None."

    lr2 = try_instantiate(ListaReproduccion, suggested_args=("Otra Lista",))
    assert lr2 is not None, "No se pudo instanciar una segunda ListaReproduccion para comprobar mutabilidad."
    assert id(lr.canciones) != id(lr2.canciones), "Cada ListaReproduccion debe tener su propia lista 'canciones'."
