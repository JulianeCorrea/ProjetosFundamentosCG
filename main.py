import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
from cubo import Cubo, desenhar_cubo

cena_objetos = [Cubo(), Cubo()]
objeto_selecionado_idx = 0


cena_objetos[1].posicao = [2.0, 0.0, -2.0]

def processa_teclado(window, key, scancode, action, mods):
    global objeto_selecionado_idx
    if action == glfw.PRESS or action == glfw.REPEAT:
        obj = cena_objetos[objeto_selecionado_idx]
        
       
        if key == glfw.KEY_TAB and action == glfw.PRESS:
            objeto_selecionado_idx = (objeto_selecionado_idx + 1) % len(cena_objetos)
            print(f"Objeto selecionado ativo: Índice {objeto_selecionado_idx}")

        
        if key == glfw.KEY_D: obj.posicao[0] += 0.1   # +X
        if key == glfw.KEY_A: obj.posicao[0] -= 0.1   # -X
        if key == glfw.KEY_I: obj.posicao[1] += 0.1   # +Y
        if key == glfw.KEY_J: obj.posicao[1] -= 0.1   # -Y
        if key == glfw.KEY_W: obj.posicao[2] -= 0.1   # -Z
        if key == glfw.KEY_S: obj.posicao[2] += 0.1   # +Z

        
        if key == glfw.KEY_X: obj.rotacao[0] += 5.0
        if key == glfw.KEY_Y: obj.rotacao[1] += 5.0
        if key == glfw.KEY_Z: obj.rotacao[2] += 5.0

        
        if key == glfw.KEY_RIGHT_BRACKET: 
            obj.escala = [e + 0.05 for e in obj.escala]
        if key == glfw.KEY_LEFT_BRACKET: 
            obj.escala = [max(0.01, e - 0.05) for e in obj.escala]

def main():
    if not glfw.init(): return
    window = glfw.create_window(800, 600, "Visualizador de Cenas 3D - Juliane Correa", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    glfw.set_key_callback(window, processa_teclado)
    
    #
    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)
    gluPerspective(45.0, 800.0 / 600.0, 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)

    while not glfw.window_should_close(window):
        glfw.poll_events()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        
       
        gluLookAt(3.0, 3.0, 7.0,  0.0, 0.0, 0.0,  0.0, 1.0, 0.0)

        for cubo in cena_objetos:
            desenhar_cubo(cubo)

        glfw.swap_buffers(window)
    glfw.terminate()

if __name__ == "__main__":
    main()