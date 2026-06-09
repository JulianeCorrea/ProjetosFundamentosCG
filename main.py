import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image
import os

from objeto import ObjetoCarregado3D
from camera import Camera

objetos_cena = []
idx_selecionado = 0
modo_atual = 'T'

camera_fps = Camera(posicao=[0.0, 1.0, 6.0])

luz_principal_ativa = True
luz_preenchimento_ativa = True
luz_fundo_ativa = True


teclas_pressionadas = {}

def carregar_textura(objeto):
    nome_imagem = objeto.arquivo_textura if objeto.arquivo_textura else "suzanne.png"
    pasta_modelo = os.path.dirname(objeto.caminho_obj)
    caminho_imagem = os.path.join(pasta_modelo, nome_imagem)
    
    if not os.path.exists(caminho_imagem):
        return None
    try:
        img = Image.open(caminho_imagem).transpose(Image.FLIP_TOP_BOTTOM)
        img_data = img.convert("RGBA").tobytes()
        largura, altura = img.size
        id_textura = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, id_textura)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, largura, altura, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
        return id_textura
    except Exception as e:
        print(f"[ERRO] Falha na textura: {e}")
        return None

def atualizar_iluminacao_3pontos():
    global objetos_cena, idx_selecionado
    global luz_principal_ativa, luz_preenchimento_ativa, luz_fundo_ativa

    if not objetos_cena: return
    obj_foco = objetos_cena[idx_selecionado]
    px, py, pz = obj_foco.posicao
    distancia = 4.0

    glEnable(GL_LIGHTING)

    if luz_principal_ativa:
        glEnable(GL_LIGHT0)
        glLightfv(GL_LIGHT0, GL_POSITION, [px + distancia, py + distancia, pz + distancia, 1.0])
        glLightfv(GL_LIGHT0, GL_AMBIENT, [0.1, 0.1, 0.1, 1.0])
        glLightfv(GL_LIGHT0, GL_DIFFUSE, [1.0, 0.95, 0.9, 1.0])
        glLightfv(GL_LIGHT0, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])
    else:
        glDisable(GL_LIGHT0)

    if luz_preenchimento_ativa:
        glEnable(GL_LIGHT1)
        glLightfv(GL_LIGHT1, GL_POSITION, [px - distancia, py + 1.0, pz + distancia, 1.0])
        glLightfv(GL_LIGHT1, GL_AMBIENT, [0.05, 0.05, 0.05, 1.0])
        glLightfv(GL_LIGHT1, GL_DIFFUSE, [0.4, 0.4, 0.5, 1.0])
        glLightfv(GL_LIGHT1, GL_SPECULAR, [0.2, 0.2, 0.2, 1.0])
    else:
        glDisable(GL_LIGHT1)

    if luz_fundo_ativa:
        glEnable(GL_LIGHT2)
        glLightfv(GL_LIGHT2, GL_POSITION, [px, py + distancia, pz - distancia, 1.0])
        glLightfv(GL_LIGHT2, GL_AMBIENT, [0.0, 0.0, 0.0, 1.0])
        glLightfv(GL_LIGHT2, GL_DIFFUSE, [0.6, 0.6, 0.6, 1.0])
        glLightfv(GL_LIGHT2, GL_SPECULAR, [0.7, 0.7, 0.7, 1.0])
    else:
        glDisable(GL_LIGHT2)

def processa_teclado(window, key, scancode, action, mods):
    global idx_selecionado, modo_atual, camera_fps  
    global luz_principal_ativa, luz_preenchimento_ativa, luz_fundo_ativa
    global teclas_pressionadas
    
    
    if action == glfw.PRESS:
        teclas_pressionadas[key] = True
    elif action == glfw.RELEASE:
        teclas_pressionadas[key] = False

   
    if action == glfw.PRESS:
        if not objetos_cena: return
        obj = objetos_cena[idx_selecionado]

        if key == glfw.KEY_TAB:
            idx_selecionado = (idx_selecionado + 1) % len(objetos_cena)
            return

        if key == glfw.KEY_1: luz_principal_ativa = not luz_principal_ativa
        elif key == glfw.KEY_2: luz_preenchimento_ativa = not luz_preenchimento_ativa
        elif key == glfw.KEY_3: luz_fundo_ativa = not luz_fundo_ativa

        if key == glfw.KEY_T: modo_atual = 'T'
        elif key == glfw.KEY_R: modo_atual = 'R'
        elif key == glfw.KEY_S: modo_atual = 'S'

        
        if modo_atual == 'T':
            if key == glfw.KEY_L: obj.posicao[0] += 0.1
            if key == glfw.KEY_J: obj.posicao[0] -= 0.1
            if key == glfw.KEY_I: obj.posicao[1] += 0.1
            if key == glfw.KEY_K: obj.posicao[1] -= 0.1
        elif modo_atual == 'R':
            if key == glfw.KEY_I: obj.rotacao[0] += 5.0
            if key == glfw.KEY_K: obj.rotacao[0] -= 5.0
            if key == glfw.KEY_L: obj.rotacao[1] += 5.0
            if key == glfw.KEY_J: obj.rotacao[1] -= 5.0
        elif modo_atual == 'S':
            if key == glfw.KEY_L: obj.escala[0] += 0.05
            if key == glfw.KEY_J: obj.escala[0] = max(0.01, obj.escala[0] - 0.05)
            if key == glfw.KEY_I: obj.escala[1] += 0.05
            if key == glfw.KEY_K: obj.escala[1] = max(0.01, obj.escala[1] - 0.05)

def atualizar_movimento_camera():
    """Verifica as teclas seguradas para mover a câmera de forma fluida."""
    global camera_fps, teclas_pressionadas
    global teclas_pressionadas
    
    
    if teclas_pressionadas.get(glfw.KEY_W): camera_fps.mover_frente_tras(1)
    if teclas_pressionadas.get(glfw.KEY_S): camera_fps.mover_frente_tras(-1)
    if teclas_pressionadas.get(glfw.KEY_D): camera_fps.mover_laterais(1)
    if teclas_pressionadas.get(glfw.KEY_A): camera_fps.mover_laterais(-1)
    
   
    if teclas_pressionadas.get(glfw.KEY_RIGHT): camera_fps.rotacionar(2.0, 0.0)
    if teclas_pressionadas.get(glfw.KEY_LEFT):  camera_fps.rotacionar(-2.0, 0.0)
    if teclas_pressionadas.get(glfw.KEY_UP):    camera_fps.rotacionar(0.0, 2.0)
    if teclas_pressionadas.get(glfw.KEY_DOWN):  camera_fps.rotacionar(0.0, -2.0)

def main():
    global objetos_cena, camera_fps
    caminho_suzanne = "assets/CGCCHibrido/assets/Modelos3D/suzanne.obj"
    
    if not glfw.init(): return
    
    window = glfw.create_window(800, 600, "Camera 1a Pessoa  - Juliane Correa", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    glfw.set_key_callback(window, processa_teclado)
    
    glEnable(GL_DEPTH_TEST)

    obj1 = ObjetoCarregado3D(caminho_suzanne)
    obj1.posicao = [-1.5, 0.0, 0.0]
    obj1.escala = [0.7, 0.7, 0.7]
    obj1.id_textura = carregar_textura(obj1)

    obj2 = ObjetoCarregado3D(caminho_suzanne)
    obj2.posicao = [1.5, 0.0, 0.0]
    obj2.escala = [0.7, 0.7, 0.7]
    obj2.id_textura = carregar_textura(obj2)

    objetos_cena = [obj1, obj2]

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, 800/600, 0.1, 50.0)
    glMatrixMode(GL_MODELVIEW)

    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        
        atualizar_movimento_camera()
        
        
        camera_fps.aplicar_view()

        atualizar_iluminacao_3pontos()

        for obj in objetos_cena:
            obj.desenhar()

        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    main()