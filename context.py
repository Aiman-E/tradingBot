import glfw
import OpenGL.GL as gl
import imgui
import sys
from imgui.integrations.glfw import GlfwRenderer


class Context():
  window = None
  imple = None
  
  def __init__(self) -> None:
    #Init imgui
    imgui.create_context()

    #Init glfw
    width, height = 1000, 700
    window_name = ""

    if not glfw.init():
        print("Could not initialize OpenGL context")
        sys.exit(1)

    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, gl.GL_TRUE)

    self.window = glfw.create_window(int(width), int(height), window_name, None, None)
    glfw.make_context_current(self.window)

    if not self.window:
        glfw.terminate()
        print("Could not initialize Window")
        sys.exit(1)
    self.impl = GlfwRenderer(self.window)

  def terminate(self):
    self.impl.shutdown()
    glfw.terminate()

  def render(self, externalImgui=None, *args, **kwargs) -> None:
    glfw.poll_events()
    self.impl.process_inputs()
    imgui.new_frame()

    gl.glClearColor(0.1, 0.1, 0.1, 1)
    gl.glClear(gl.GL_COLOR_BUFFER_BIT)

    if externalImgui:
      externalImgui(args, kwargs)

    imgui.render()
    self.impl.render(imgui.get_draw_data())

    glfw.swap_buffers(self.window)

  def shouldClose(self):
    return glfw.window_should_close(self.window)


def imguiCommands():  
    from imguiCommands import imguiTrade
    imgui.show_demo_window()




if __name__ == '__main__':
  from trade import Trade
  from bingxapi import ORDER_CONFIG
  
  context = Context()
  while not context.shouldClose():  
    context.render(imguiCommands)