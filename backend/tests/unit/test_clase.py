import pytest
from clase import Pila, Cola

def test_pila_vacia():
    pila = Pila()
    assert pila.esta_vacia()
    with pytest.raises(ValueError):
        pila.desapilar()
    with pytest.raises(ValueError):
        pila.ver_tope()

def test_pila_apilar_desapilar():
    pila = Pila()
    pila.apilar(1)
    pila.apilar(2)
    
    assert not pila.esta_vacia()
    assert pila.ver_tope() == 2
    
    assert pila.desapilar() == 2
    assert pila.ver_tope() == 1
    assert pila.desapilar() == 1
    assert pila.esta_vacia()

def test_cola_vacia():
    cola = Cola()
    assert cola.esta_vacia()
    with pytest.raises(ValueError):
        cola.desencolar()
    with pytest.raises(ValueError):
        cola.ver_frente()

def test_cola_encolar_desencolar():
    cola = Cola()
    cola.encolar(1)
    cola.encolar(2)
    
    assert not cola.esta_vacia()
    assert cola.ver_frente() == 1
    
    assert cola.desencolar() == 1
    assert cola.ver_frente() == 2
    assert cola.desencolar() == 2
    assert cola.esta_vacia()

def test_cola_eliminar_contenido():
    cola = Cola()
    cola.encolar(1)
    cola.encolar(2)
    cola.eliminar_contenido()
    assert cola.esta_vacia()
