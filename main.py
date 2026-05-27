"""
PARTE 1 - Hello 3D
Triângulo colorido estático
Compatível com OpenGL 3.3 (GeForce G210)
Autor: Juliane Correa
"""

import glfw
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import numpy as np
import ctypes

# =====================================================
# CONFIGURAÇÕES DA JANELA
# =====================================================
LARGURA = 800
ALTURA = 600
TITULO = "Ola 3D - Juliane Correa"

# =====================================================
# VÉRTICES DO TRIÂNGULO (posição x,y,z + cor r,g,b)
# =====================================================
vertices = np.array([
    # Vértice 1: Inferior esquerdo (VERMELHO)
    -0.5, -0.5, 0.0,  1.0, 0.0, 0.0,
    # Vértice 2: Inferior direito (VERDE)
     0.5, -0.5, 0.0,  0.0, 1.0, 0.0,
    # Vértice 3: Topo (AZUL)
     0.0,  0.5, 0.0,  0.0, 0.0, 1.0,
], dtype=np.float32)

# =====================================================
# SHADERS (versão 330 core - compatível)
# =====================================================
VERTEX_SHADER_SRC = """
#version 330 core
in vec3 aPos;
in vec3 aColor;
out vec3 Color;
void main() {
    gl_Position = vec4(aPos, 1.0);
    Color = aColor;
}
"""

FRAGMENT_SHADER_SRC = """
#version 330 core
in vec3 Color;
out vec4 FragColor;
void main() {
    FragColor = vec4(Color, 1.0);
}
"""

# =====================================================
# FUNÇÃO PRINCIPAL
# =====================================================
def main():
    # Inicializar GLFW
    glfw.default_window_hints()
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    
    if not glfw.init():
        print("Erro ao inicializar GLFW")
        return -1
    
    # Criar janela
    window = glfw.create_window(LARGURA, ALTURA, TITULO, None, None)
    if not window:
        print("Erro ao criar janela")
        glfw.terminate()
        return -1
    
    glfw.make_context_current(window)
    glfw.set_framebuffer_size_callback(window, framebuffer_size_callback)
    
    # Informações do sistema
    print(f"OpenGL: {glGetString(GL_VERSION).decode()}")
    print(f"Renderer: {glGetString(GL_RENDERER).decode()}")
    print(f"\n=== {TITULO} ===")
    print("Triângulo colorido estático")
    print("Pressione ESC para sair\n")
    
    # Compilar shaders
    vs = compileShader(VERTEX_SHADER_SRC, GL_VERTEX_SHADER)
    fs = compileShader(FRAGMENT_SHADER_SRC, GL_FRAGMENT_SHADER)
    shader = compileProgram(vs, fs)
    
    # Criar buffers
    VAO = glGenVertexArrays(1)
    VBO = glGenBuffers(1)
    
    glBindVertexArray(VAO)
    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
    
    # Atributo posição (location = 0)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 6 * sizeof(GLfloat), ctypes.c_void_p(0))
    glEnableVertexAttribArray(0)
    
    # Atributo cor (location = 1)
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 6 * sizeof(GLfloat), ctypes.c_void_p(3 * sizeof(GLfloat)))
    glEnableVertexAttribArray(1)
    
    # Configuração de renderização
    glClearColor(0.1, 0.1, 0.2, 1.0)
    
    # Loop principal
    while not glfw.window_should_close(window):
        # Verificar tecla ESC
        if glfw.get_key(window, glfw.KEY_ESCAPE) == glfw.PRESS:
            glfw.set_window_should_close(window, True)
        
        # Limpar tela
        glClear(GL_COLOR_BUFFER_BIT)
        
        # Desenhar triângulo
        glUseProgram(shader)
        glBindVertexArray(VAO)
        glDrawArrays(GL_TRIANGLES, 0, 3)
        
        # Trocar buffers
        glfw.swap_buffers(window)
        glfw.poll_events()
    
    # Limpeza
    glDeleteVertexArrays(1, [VAO])
    glDeleteBuffers(1, [VBO])
    glDeleteProgram(shader)
    glfw.terminate()
    return 0

def framebuffer_size_callback(window, width, height):
    glViewport(0, 0, width, height)

if __name__ == "__main__":
    main()