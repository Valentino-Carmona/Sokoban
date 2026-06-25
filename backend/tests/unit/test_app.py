import pytest
import json
from app import app, STATE

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index(client):
    response = client.get('/')
    assert response.status_code == 200

def test_start_game(client):
    response = client.post('/api/start')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'grilla' in data
    assert 'nivel' in data
    assert data['nivel'] == 1
    assert not data['ganado']
    
    # State should be updated
    assert STATE['nivel_actual'] == 1
    assert STATE['diccionario_actual'] is not None

def test_move_action(client):
    client.post('/api/start')
    
    # Move NORTE (Assuming player is placed such that NORTE is a valid move)
    # Actually, in level 1 of typical Sokoban, there might be a wall or not, 
    # but the API should at least return 200 and the grid state.
    response = client.post('/api/move', json={'accion': 'NORTE'})
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'grilla' in data
    assert not data['ganado']

def test_move_invalid_action(client):
    client.post('/api/start')
    response = client.post('/api/move', json={'accion': 'ACCION_INVALIDA'})
    assert response.status_code == 200
    data = json.loads(response.data)
    # The grid shouldn't change, but it should return normally
    assert 'grilla' in data

def test_move_special_actions(client):
    client.post('/api/start')
    
    # Test Deshacer / Rehacer
    client.post('/api/move', json={'accion': 'NORTE'})
    client.post('/api/move', json={'accion': 'DESHACER'})
    client.post('/api/move', json={'accion': 'REHACER'})
    
    # Test Backtracking (won't solve in 1 move, but shouldn't crash)
    response = client.post('/api/move', json={'accion': 'BACKTRACKING'})
    assert response.status_code == 200
    
    # Test Reiniciar
    response = client.post('/api/move', json={'accion': 'REINICIAR'})
    assert response.status_code == 200
    
def test_move_without_start(client):
    # Reset state manually
    STATE['diccionario_actual'] = None
    response = client.post('/api/move', json={'accion': 'NORTE'})
    data = json.loads(response.data)
    assert 'error' in data
