import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image  
import os


from objeto import ObjetoCarregado3D


objetos_cena = []
idx_selecionado = 0
modo_atual = 'T'  

def carregar_textura(objeto):
    """Abre a imagem do objeto usando a Pillow e gera uma ID de Textura no OpenGL"""
    nome_imagem = objeto.arquivo_textura if objeto.arquivo_textura else "suzanne.png"
    
    pasta_modelo = os.path.dirname(objeto.caminho_obj)
    caminho_imagem = os.path.join(pasta_modelo, nome_imagem)
    
    if not os.path.exists(caminho_imagem):
        print(f"[AVISO] Imagem de textura nao encontrada em: {caminho_imagem}")
        print(" -> Certifique-se de colocar a imagem (.png/.jpg) na mesma pasta do .obj!")
        return None

    try:
        
        img = Image.open(caminho_imagem).transpose(Image.FLIP_TOP_BOTTOM)
        img_data = img.convert("RGBA").tobytes()
        largura, altura = img.size

        id_textura = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, id_textura)

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)

        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, largura, altura, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
        
        print(f"[TEXTURA OK] Carregada com sucesso: {nome_imagem} ({largura}x{altura})")
        return id_textura

    except Exception as e:
        print(f"[ERRO] Falha ao processar a textura: {e}")
        return None

def processa_teclado(window, key, scancode, action, mods):
    global idx_selecionado, modo_atual
    
    if action == glfw.PRESS or action == glfw.REPEAT:
        if not objetos_cena: return
        obj = objetos_cena[idx_selecionado]

        if key == glfw.KEY_TAB and action == glfw.PRESS:
            idx_selecionado = (idx_selecionado + 1) % len(objetos_cena)
            print(f"\n[INFO] Objeto selecionado alterado para o índice: {idx_selecionado}")
            return

        if key == glfw.KEY_T: 
            modo_atual = 'T'
            print("\n[MODO] TRANSLACAO ATIVA nos eixos X, Y e Z (Use W, A, S, D, Q, E)")
        elif key == glfw.KEY_R: 
            modo_atual = 'R'
            print("\n[MODO] ROTACAO ATIVA nos eixos X, Y e Z (Use W, A, S, D, Q, E)")
        elif key == glfw.KEY_S: 
            modo_atual = 'S'
            print("\n[MODO] ESCALA ATIVA nos eixos X, Y e Z (Use W, A, S, D, Q, E ou + / -)")

        # --- EXECUÇÃO DAS TRANSFORMAÇÕES ---
        if modo_atual == 'T':
            if key == glfw.KEY_D: obj.posicao[0] += 0.1
            if key == glfw.KEY_A: obj.posicao[0] -= 0.1
            if key == glfw.KEY_W: obj.posicao[1] += 0.1
            if key == glfw.KEY_S: obj.posicao[1] -= 0.1
            if key == glfw.KEY_E: obj.posicao[2] += 0.1
            if key == glfw.KEY_Q: obj.posicao[2] -= 0.1

        elif modo_atual == 'R':
            if key == glfw.KEY_W: obj.rotacao[0] += 5.0
            if key == glfw.KEY_S: obj.rotacao[0] -= 5.0
            if key == glfw.KEY_D: obj.rotacao[1] += 5.0
            if key == glfw.KEY_A: obj.rotacao[1] -= 5.0
            if key == glfw.KEY_E: obj.rotacao[2] += 5.0
            if key == glfw.KEY_Q: obj.rotacao[2] -= 5.0

        elif modo_atual == 'S':
            if key == glfw.KEY_D: obj.escala[0] += 0.05
            if key == glfw.KEY_A: obj.escala[0] = max(0.01, obj.escala[0] - 0.05)
            if key == glfw.KEY_W: obj.escala[1] += 0.05
            if key == glfw.KEY_S: obj.escala[1] = max(0.01, obj.escala[1] - 0.05)
            if key == glfw.KEY_E: obj.escala[2] += 0.05
            if key == glfw.KEY_Q: obj.escala[2] = max(0.01, obj.escala[2] - 0.05)
            
            if key in [glfw.KEY_KP_ADD, glfw.KEY_EQUAL]: 
                obj.escala = [e + 0.05 for e in obj.escala]
            if key in [glfw.KEY_KP_SUBTRACT, glfw.KEY_MINUS]:  
                obj.escala = [max(0.01, e - 0.05) for e in obj.escala]

def inicializa_opengl():
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    
    posicao_luz = [0.0, 5.0, 5.0, 1.0]
    cor_luz = [1.0, 1.0, 1.0, 1.0]
    luz_ambiente = [0.2, 0.2, 0.2, 1.0]
    
    glLightfv(GL_LIGHT0, GL_POSITION, posicao_luz)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, cor_luz)
    glLightfv(GL_LIGHT0, GL_AMBIENT, luz_ambiente)
    
    
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)

def main():
    global objetos_cena
    
    print("[INFO] Iniciando o verificador de execucao...")
    caminho_suzanne = "assets/CGCCHibrido/assets/Modelos3D/suzanne.obj"
    
    if not os.path.exists(caminho_suzanne):
        print(f"[ERRO CRÍTICO] O arquivo '{caminho_suzanne}' NAO foi encontrado!")
        return

    if not glfw.init():
        print("[ERRO CRÍTICO] Nao foi possivel inicializar o GLFW!")
        return

    window = glfw.create_window(800, 600, "Visualizador 3D Texturizado - Juliane", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    glfw.set_key_callback(window, processa_teclado)
    
    inicializa_opengl()

    
    obj1 = ObjetoCarregado3D(caminho_suzanne)
    obj1.posicao = [-1.5, 0.0, 0.0]
    obj1.escala = [0.6, 0.6, 0.6]
    obj1.id_textura = carregar_textura(obj1)

    obj2 = ObjetoCarregado3D(caminho_suzanne)
    obj2.posicao = [1.5, 0.0, 0.0]
    obj2.escala = [0.6, 0.6, 0.6]
    obj2.id_textura = carregar_textura(obj2)

    objetos_cena = [obj1, obj2]

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, 800/600, 0.1, 50.0)
    glMatrixMode(GL_MODELVIEW)

    print("\n[START] Janela aberta! Pressione T, R ou S para interagir.")

    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        
        gluLookAt(0.0, 0.0, 5.0,  0.0, 0.0, 0.0,  0.0, 1.0, 0.0)

        for obj in objetos_cena:
            obj.desenhar()

        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    main()