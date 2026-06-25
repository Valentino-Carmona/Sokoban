import pytest
import soko

@pytest.fixture
def grilla_basica():
    desc = [
        '#####',
        '#.$ #',
        '#@  #',
        '#####'
    ]
    return soko.crear_grilla(desc)

def test_crear_grilla():
    desc = ['###', '#@#', '###']
    grilla = soko.crear_grilla(desc)
    assert grilla == [['#', '#', '#'], ['#', '@', '#'], ['#', '#', '#']]

def test_dimensiones(grilla_basica):
    columnas, filas = soko.dimensiones(grilla_basica)
    assert filas == 4
    assert columnas == 5

def test_hay_elementos(grilla_basica):
    assert soko.hay_pared(grilla_basica, 0, 0)
    assert not soko.hay_pared(grilla_basica, 1, 1)
    
    assert soko.hay_objetivo(grilla_basica, 1, 1) # '.'
    assert not soko.hay_objetivo(grilla_basica, 2, 1) # '$'
    
    assert soko.hay_caja(grilla_basica, 2, 1)
    assert not soko.hay_caja(grilla_basica, 1, 1)
    
    assert soko.hay_jugador(grilla_basica, 1, 2)
    assert not soko.hay_jugador(grilla_basica, 1, 1)

def test_juego_ganado():
    ganado = soko.crear_grilla(['###', '#*#', '###']) # '*' = CAJA_EN_PUNTO
    assert soko.juego_ganado(ganado)
    
    no_ganado = soko.crear_grilla(['###', '#$#', '#.#', '###'])
    assert not soko.juego_ganado(no_ganado)

def test_mover_basico(grilla_basica):
    # Jugador en (1, 2). Mover ESTE -> (2, 2)
    nueva = soko.mover(grilla_basica, 'ESTE')
    assert soko.hay_jugador(nueva, 2, 2)
    assert not soko.hay_jugador(nueva, 1, 2)
    
    # Mover OESTE desde (1,2) choca pared (0,2)
    nueva2 = soko.mover(grilla_basica, 'OESTE')
    assert soko.hay_jugador(nueva2, 1, 2) # No se movió

def test_mover_caja(grilla_basica):
    # Caja en (2,1), jugador en (1,2) - no puede empujarla desde abajo porque arriba hay pared
    nueva = soko.mover(grilla_basica, 'NORTE')
    assert soko.hay_jugador(nueva, 1, 1) # Entra al objetivo (PJ_EN_PUNTO)
    
    # Probemos una caja empujable
    empujable = soko.crear_grilla([
        '######',
        '# .  #',
        '#  $ #',
        '#  @ #',
        '######'
    ])
    nueva = soko.mover(empujable, 'NORTE') # empuja caja de (3,2) a (3,1), jugador a (3,2)
    assert soko.hay_jugador(nueva, 3, 2)
    assert soko.hay_caja(nueva, 3, 1)
    
    # Ahora la empujamos al oeste (hacia el objetivo en 2,1)
    # Jugador debería moverse a (3,1) y caja a (2,1)
    # Ah, el jugador está en (3,2). Necesitamos moverlo a (4,1) y luego OESTE
    # Mejor creamos otra situación
    empujable2 = soko.crear_grilla([
        '######',
        '# . $@#',
        '######'
    ])
    nueva2 = soko.mover(empujable2, 'OESTE')
    assert soko.hay_jugador(nueva2, 4, 1)
    assert soko.hay_caja(nueva2, 3, 1) # Ahora está en (3,1)
    
    nueva3 = soko.mover(nueva2, 'OESTE')
    assert soko.hay_jugador(nueva3, 3, 1)
    assert soko.hay_caja(nueva3, 2, 1)
    assert soko.hay_objetivo(nueva3, 2, 1) # Ahora es CAJA_EN_PUNTO '*'
    assert nueva3[1][2] == '*'
