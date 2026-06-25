import soko
import clase
import os
from flask import Flask, jsonify, request, send_from_directory

frontend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'frontend', 'src'))
app = Flask(__name__, static_folder=frontend_dir, static_url_path='/static')

# Ajustar el directorio de trabajo
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def niveles():
    # from main.py
    resultado = {}
    nivel = 1
    try:
        with open(os.path.join('data', 'niveles.txt')) as archivo:
            lineas = archivo.readlines()
            for linea in lineas:
                if linea == '\n':
                    resultado[nivel] = soko.crear_grilla(resultado[nivel])
                    nivel += 1
                else:    
                    linea = linea.rstrip()
                    if linea.startswith(' ') or linea.startswith('#'):
                        resultado[nivel] = resultado.get(nivel, [])
                        resultado[nivel].append(linea)         
    except FileNotFoundError:
        print('El archivo "data/niveles.txt" no se ha encontrado')
    return resultado

def _inicializar_guardados(nivel, juego):
    diccionario_actual = {}
    diccionario_actual['nivel'] = nivel
    diccionario_actual['grilla'] = juego
    diccionario_actual['deshacer'] = clase.Pila()
    diccionario_actual['rehacer'] = clase.Pila()
    diccionario_actual['pistas'] = clase.Pila()
    diccionario_actual['deshacer'].apilar(juego)
    return diccionario_actual

# Global state for MVP
STATE = {
    'diccionario_niveles': {},
    'diccionario_actual': None,
    'nivel_actual': 1,
    'ganado': False
}

def _revisar(diccionario_actual): 
    juego = diccionario_actual['grilla']
    d = diccionario_actual['deshacer']
    r = diccionario_actual['rehacer']
    p = diccionario_actual['pistas']
    if d.esta_vacia():
        d.apilar(juego)
    if d.ver_tope() == juego:
        return diccionario_actual
    if d.ver_tope() != juego:
        d.apilar(juego)
    if not r.esta_vacia():
        diccionario_actual['rehacer'] = clase.Pila()
    if not p.esta_vacia():
        diccionario_actual['pistas'] = clase.Pila()
    return diccionario_actual

def deshacer(diccionario_actual):
    juego = diccionario_actual['grilla']
    d = diccionario_actual['deshacer']

    if diccionario_actual['rehacer'].esta_vacia():
        diccionario_actual['rehacer'].apilar(juego)
    if d.esta_vacia():
        return diccionario_actual
    else:
        if juego == d.ver_tope():
            d.desapilar()
            if not d.esta_vacia():
                juego = d.desapilar()    
        else:
            juego = d.desapilar()

        diccionario_actual['rehacer'].apilar(juego)

    diccionario_actual['grilla'] = juego
    return diccionario_actual

def rehacer(diccionario_actual):
    rehacer = diccionario_actual['rehacer']
    juego = diccionario_actual['grilla']
    if diccionario_actual['deshacer'].esta_vacia():
        diccionario_actual['deshacer'].apilar(juego)

    if rehacer.esta_vacia():
        return diccionario_actual
    else:
        if not rehacer.esta_vacia():
            if rehacer.ver_tope() == juego:
                    rehacer.desapilar()
                    if not rehacer.esta_vacia():
                        juego = rehacer.desapilar()
            else: 
                juego = rehacer.desapilar()

            diccionario_actual['grilla'] = juego
            diccionario_actual['deshacer'].apilar(juego)
            return diccionario_actual

def _buscar_solucion(estado_inicial, diccionario_actual):
    visitados = set() 
    return _backtrack(estado_inicial, visitados, diccionario_actual)

def _estado_inmutable(estado): 
    resultado = ()
    for fila in estado:
        linea = ''.join(fila)
        resultado += (linea,)
    return resultado

def _agregar(visitados, estado):
    nuevo = _estado_inmutable(estado)
    visitados.add(nuevo)

def _pertenece(visitados, nuevo_estado):
    buscar = _estado_inmutable(nuevo_estado)
    if buscar in visitados:
        return True

def _backtrack(estado, visitados, diccionario_actual):
    _agregar(visitados, estado)                            
    
    if soko.juego_ganado(estado): 
        return True, ()
    
    for a in ('NORTE', 'SUR', 'ESTE', 'OESTE'):          
        nuevo_estado = soko.mover(estado, a)

        if _pertenece(visitados, nuevo_estado):            
            continue

        solución_encontrada, acciones = _backtrack(nuevo_estado, visitados, diccionario_actual)

        if solución_encontrada:
            return True, acciones + (a,)                

    return False, ()

def devolver_pistas(diccionario_actual):
    p = diccionario_actual['pistas']
    juego = diccionario_actual['grilla']

    if p.esta_vacia():
        booleano, solucion_acciones = _buscar_solucion(juego, diccionario_actual)
        
        for i in range(len(solucion_acciones)):
            p.apilar(solucion_acciones[i])
    
    if not p.esta_vacia():
        return soko.mover(juego, p.desapilar())
    return juego

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/img/<path:filename>')
def serve_img(filename):
    return send_from_directory(os.path.join(frontend_dir, 'img'), filename)

@app.route('/api/start', methods=['POST', 'GET'])
def start_game():
    STATE['diccionario_niveles'] = niveles()
    STATE['nivel_actual'] = 1
    if 1 not in STATE['diccionario_niveles']:
        return jsonify({'error': 'No se encontraron niveles'})
    juego = STATE['diccionario_niveles'][1]
    STATE['diccionario_actual'] = _inicializar_guardados(1, juego)
    STATE['ganado'] = False
    
    return jsonify({
        'grilla': STATE['diccionario_actual']['grilla'],
        'nivel': STATE['nivel_actual'],
        'ganado': STATE['ganado']
    })

@app.route('/api/move', methods=['POST'])
def move():
    data = request.json
    accion = data.get('accion') # 'NORTE', 'SUR', 'ESTE', 'OESTE', 'REINICIAR', 'DESHACER', 'REHACER'
    
    if STATE['diccionario_actual'] is None:
        return jsonify({'error': 'Juego no iniciado'})

    diccionario_actual = STATE['diccionario_actual']
    
    if accion == 'REINICIAR':
        juego = STATE['diccionario_niveles'][STATE['nivel_actual']]
        STATE['diccionario_actual'] = _inicializar_guardados(STATE['nivel_actual'], juego)
        STATE['ganado'] = False
    
    elif accion == 'DESHACER':
        STATE['diccionario_actual'] = deshacer(diccionario_actual)
    
    elif accion == 'REHACER':
        STATE['diccionario_actual'] = rehacer(diccionario_actual)
        
    elif accion == 'BACKTRACKING':
        diccionario_actual = _revisar(diccionario_actual)
        juego = devolver_pistas(diccionario_actual)
        diccionario_actual['grilla'] = juego
        diccionario_actual['deshacer'].apilar(juego)
        diccionario_actual = _revisar(diccionario_actual)
        STATE['diccionario_actual'] = diccionario_actual
    
    elif accion in ('NORTE', 'SUR', 'ESTE', 'OESTE'):
        if not STATE['ganado']:
            juego = diccionario_actual['grilla']
            diccionario_actual = _revisar(diccionario_actual)
            diccionario_actual['grilla'] = soko.mover(juego, accion)
            diccionario_actual = _revisar(diccionario_actual)
            STATE['diccionario_actual'] = diccionario_actual
    
    # Check win condition
    STATE['ganado'] = soko.juego_ganado(STATE['diccionario_actual']['grilla'])
    completado = False
    
    if STATE['ganado']:
        next_nivel = STATE['nivel_actual'] + 1
        if next_nivel in STATE['diccionario_niveles']:
            STATE['nivel_actual'] = next_nivel
            juego = STATE['diccionario_niveles'][next_nivel]
            STATE['diccionario_actual'] = _inicializar_guardados(next_nivel, juego)
            STATE['ganado'] = False
        else:
            completado = True # Fin del juego completo
            
    return jsonify({
        'grilla': STATE['diccionario_actual']['grilla'],
        'nivel': STATE['nivel_actual'],
        'ganado': STATE['ganado'],
        'completado': completado
    })

if __name__ == '__main__':
    host = os.environ.get('FLASK_HOST', '127.0.0.1')
    port = int(os.environ.get('FLASK_PORT', 5000))
    app.run(host=host, port=port, debug=True)
