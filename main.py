import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
from objeto import ObjetoCarregado3D, desenhar_objeto_malha
import sys

WINDOW_TITLE = "Visualizador OBJ - Juliane Correa"
objetos_cena = []
idx_selecionado = 0
modo_atual = 'T' 

def inicializa_opengl():
    glClearColor(0.1, 0.1, 0.1, 1.0)
    glEnable(GL_DEPTH_TEST)
    
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, 800.0 / 600.0, 0.1, 100.0)
    
    glMatrixMode(GL_MODELVIEW)
    posicao_luz = [0.0, 5.0, 5.0, 1.0]
    glLightfv(GL_LIGHT0, GL_POSITION, posicao_luz)

def processa_teclado(window, key, scancode, action, mods):
    global idx_selecionado, modo_atual
    
    if action == glfw.PRESS or action == glfw.REPEAT:
        if not objetos_cena: return
        obj = objetos_cena[idx_selecionado]

        if key == glfw.KEY_TAB and action == glfw.PRESS:
            idx_selecionado = (idx_selecionado + 1) % len(objetos_cena)
            print(f"\n[INFO] Selecao alterada para o objeto: {idx_selecionado}")
            return

        if key == glfw.KEY_T: modo_atual = 'T'; print("[MODO] TRANSLACAO ativa. (Setas / IJ)")
        elif key == glfw.KEY_R: modo_atual = 'R'; print("[MODO] ROTACAO ativa. (Setas)")
        elif key == glfw.KEY_S: modo_atual = 'S'; print("[MODO] ESCALA ativa. ([ e ])")

        if modo_atual == 'T':
            if key == glfw.KEY_RIGHT: obj.posicao[0] += 0.1
            if key == glfw.KEY_LEFT:  obj.posicao[0] -= 0.1
            if key == glfw.KEY_UP:    obj.posicao[1] += 0.1
            if key == glfw.KEY_DOWN:  obj.posicao[1] -= 0.1
            if key == glfw.KEY_I:     obj.posicao[2] -= 0.1
            if key == glfw.KEY_J:     obj.posicao[2] += 0.1

        elif modo_atual == 'R':
            if key == glfw.KEY_UP:    obj.rotacao[0] += 5.0
            if key == glfw.KEY_DOWN:  obj.rotacao[0] -= 5.0
            if key == glfw.KEY_LEFT:  obj.rotacao[1] -= 5.0
            if key == glfw.KEY_RIGHT: obj.rotacao[1] += 5.0

        elif modo_atual == 'S':
            if key == glfw.KEY_RIGHT_BRACKET: 
                obj.escala = [e + 0.05 for e in obj.escala]
            if key == glfw.KEY_LEFT_BRACKET:  
                obj.escala = [max(0.01, e - 0.05) for e in obj.escala]

def main():
    global objetos_cena
    if not glfw.init(): 
        sys.exit()

    window = glfw.create_window(800, 600, WINDOW_TITLE, None, None)
    if not window:
        glfw.terminate()
        sys.exit()

    glfw.make_context_current(window)
    glfw.set_key_callback(window, processa_teclado)
    inicializa_opengl()

    # Caminho mapeado de acordo com a sua estrutura de pastas do clone
    caminho_suzanne = "assets/CGCCHibrido/assets/Modelos3D/suzanne.obj"
    
    # Criando instâncias limpas usando a classe correta
    obj1 = ObjetoCarregado3D(caminho_suzanne)
    obj1.posicao = [-1.5, 0.0, 0.0]
    obj1.escala = [0.6, 0.6, 0.6]
    
    obj2 = ObjetoCarregado3D(caminho_suzanne)
    obj2.posicao = [1.5, 0.0, 0.0]
    obj2.escala = [0.6, 0.6, 0.6]
    
    objetos_cena.extend([obj1, obj2])

    print("="*50)
    print(f"DEBUG: Procurando arquivo em: {caminho_suzanne}")
    print(f"DEBUG: Vertices carregados: {len(obj1.vertices)}")
    print(f"DEBUG: Faces carregadas: {len(obj1.faces)}")
    print("="*50)

    while not glfw.window_should_close(window):
        glfw.poll_events()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        
        gluLookAt(0.0, 0.0, 6.0,  0.0, 0.0, 0.0,  0.0, 1.0, 0.0)

        for i, obj in enumerate(objetos_cena):
            desenhar_objeto_malha(obj, selecionado=(i == idx_selecionado))

        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()