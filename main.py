import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import sys


WINDOW_TITLE = "Ola 3D – Juliane Correa" 

def inicializa_opengl():
    glClearColor(0.1, 0.1, 0.1, 1.0) 
    glEnable(GL_DEPTH_TEST)          

    
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, 800.0 / 600.0, 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)

def redimensiona_janela(window, width, height):
    if height == 0: height = 1
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, width / height, 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)

def main():
    if not glfw.init():
        sys.exit()

    
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 2)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 1)

    window = glfw.create_window(800, 600, WINDOW_TITLE, None, None)
    if not window:
        glfw.terminate()
        sys.exit()

    glfw.make_context_current(window)
    glfw.set_framebuffer_size_callback(window, redimensiona_janela)
    
    inicializa_opengl()

    
    while not glfw.window_should_close(window):
        glfw.poll_events()
        
       
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        
        
        gluLookAt(0.0, 0.0, 5.0,  0.0, 0.0, 0.0,  0.0, 1.0, 0.0)

        
        glBegin(GL_TRIANGLES)
        glColor3f(1.0, 0.0, 0.0) 
        glVertex3f(-1.0, -1.0, 0.0) 
        
        glColor3f(0.0, 1.0, 0.0) 
        glVertex3f(1.0, -1.0, 0.0)  
        
        glColor3f(0.0, 0.0, 1.0) 
        glVertex3f(0.0, 1.0, 0.0)   
        glEnd()
       
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()