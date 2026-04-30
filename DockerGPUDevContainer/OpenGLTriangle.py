#!/usr/bin/env -S uv run --script

"""
A template for creating a PySide6 application with an OpenGL viewport using py-ngl.

This script sets up a basic window, initializes an OpenGL context, and provides
standard mouse and keyboard controls for interacting with a 3D scene (rotate, pan, zoom).
It is designed to be a starting point for more complex OpenGL applications.
"""

import ctypes
import sys
import traceback

import numpy as np
import OpenGL.GL as gl
from PySide6.QtCore import Qt
from PySide6.QtGui import QSurfaceFormat
from PySide6.QtOpenGL import QOpenGLWindow
from PySide6.QtWidgets import QApplication

VERTEX_SHADER = """#version 400 core

layout (location = 0) in vec3  inPosition;
layout (location = 1) in vec3 inColour;
out vec3 vertColour;
void main()
{
  gl_Position = vec4(inPosition, 1.0);
  vertColour = inColour;
}"""

FRAGMENT_SHADER = """#version 400 core
in vec3 vertColour;
out vec4 fragColour;
void main()
{
  fragColour = vec4(vertColour,1.0);
}
"""


class MainWindow(QOpenGLWindow):
    """
    The main window for the OpenGL application.

    Inherits from QOpenGLWindow to provide a canvas for OpenGL rendering within a PySide6 GUI.
    It handles user input (mouse, keyboard) for camera control and manages the OpenGL context.
    """

    def __init__(self, parent: object = None) -> None:
        """
        Initializes the main window and sets up default scene parameters.
        """
        super().__init__()
        # --- Camera and Transformation Attributes ---
        self.setTitle("First Triangle OpenGL (Core Profile)")

    def initializeGL(self) -> None:
        """
        Called once when the OpenGL context is first created.
        This is the place to set up global OpenGL state, load shaders, and create geometry.
        """
        self.makeCurrent()  # Make the OpenGL context current in this thread
        # Set the background colour to a dark grey
        gl.glClearColor(0.4, 0.4, 0.4, 1.0)
        # Enable depth testing, which ensures that objects closer to the camera obscure those further away
        gl.glEnable(gl.GL_DEPTH_TEST)
        # Enable multisampling for anti-aliasing, which smooths jagged edges
        gl.glEnable(gl.GL_MULTISAMPLE)
        self._create_triangle(0.5)
        self._load_shader_from_strings(VERTEX_SHADER, FRAGMENT_SHADER)

    def _create_triangle(self, size):
        # fmt: off
        VERTEX_DATA = np.array([
            -0.75, -0.75,0.0,1.0, 0.0, 0.0,  # Bottom-left vertex (red)
            0.0,  0.75,0.0, 0.0, 1.0,  0.0,  # Top vertex (green)
            0.75,  -0.75,0.0, 0.0,  0.0, 1.0,  # Bottom-right vertex (blue)
            ],dtype=np.float32)
        # fmt: on
        # allocate a VertexArray
        self.vao_id = gl.glGenVertexArrays(1)
        # now bind a vertex array object for our verts
        gl.glBindVertexArray(self.vao_id)

        vbo_id = gl.glGenBuffers(1)
        #  now bind this to the VBO buffer
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, vbo_id)
        #  allocate the buffer data
        gl.glBufferData(gl.GL_ARRAY_BUFFER, VERTEX_DATA, gl.GL_STATIC_DRAW)
        #  now fix this to the attribute buffer 0
        gl.glVertexAttribPointer(0, 3, gl.GL_FLOAT, gl.GL_FALSE, VERTEX_DATA.itemsize * 6, ctypes.c_void_p(0))
        #  enable and bind this attribute (will be inPosition in the shader)
        gl.glEnableVertexAttribArray(0)
        #  now fix this to the attribute buffer 0
        gl.glVertexAttribPointer(
            1,
            3,
            gl.GL_FLOAT,
            gl.GL_FALSE,
            VERTEX_DATA.itemsize * 6,
            ctypes.c_void_p(VERTEX_DATA.itemsize * 3),
        )
        #  enable and bind this attribute (will be inPosition in the shader)
        gl.glEnableVertexAttribArray(1)
        gl.glBindVertexArray(0)

    def _load_shader_from_strings(self, vertex, fragment):
        # here we create a program
        self.shader_id = gl.glCreateProgram()

        # create a Vertex shader object
        vertex_id = gl.glCreateShader(gl.GL_VERTEX_SHADER)
        # attatch the shader source we need to convert to GL format

        gl.glShaderSource(vertex_id, vertex)
        # now compile the shader
        gl.glCompileShader(vertex_id)

        def check_shader_compilation_status(shader_id):
            if not gl.glGetShaderiv(shader_id, gl.GL_COMPILE_STATUS):
                print(gl.glGetShaderInfoLog(shader_id))
                raise RuntimeError("Shader compilation failed")

        check_shader_compilation_status(vertex_id)

        # now create a fragment shader
        fragment_id = gl.glCreateShader(gl.GL_FRAGMENT_SHADER)
        # attatch the shader source
        gl.glShaderSource(fragment_id, fragment)
        # compile the shader
        gl.glCompileShader(fragment_id)
        check_shader_compilation_status(fragment_id)
        # now attach to the program object
        gl.glAttachShader(self.shader_id, vertex_id)
        gl.glAttachShader(self.shader_id, fragment_id)

        # link the program
        gl.glLinkProgram(self.shader_id)
        # and enable it for use
        gl.glUseProgram(self.shader_id)
        # now tidy up the shaders as we don't need them
        gl.glDeleteShader(vertex_id)
        gl.glDeleteShader(fragment_id)

    def paintGL(self) -> None:
        """
        Called every time the window needs to be redrawn.
        This is the main rendering loop where all drawing commands are issued.
        """
        self.makeCurrent()
        # Set the viewport to cover the entire window
        gl.glViewport(0, 0, self.width(), self.height())
        # Clear the colour and depth buffers from the previous frame
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        gl.glBindVertexArray(self.vao_id)
        gl.glDrawArrays(gl.GL_TRIANGLES, 0, 3)

    def resizeGL(self, w: int, h: int) -> None:
        """
        Called whenever the window is resized.
        It's crucial to update the viewport and projection matrix here.

        Args:
            w: The new width of the window.
            h: The new height of the window.
        """
        # Update the stored width and height, considering high-DPI displays
        # self.devicePixelRatio() will give the pixel ratio of the screen the window is on
        ratio = self.devicePixelRatio()
        self.window_width = int(w * ratio)
        self.window_height = int(h * ratio)

    def keyPressEvent(self, event) -> None:
        """
        Handles keyboard press events.

        Args:
            event: The QKeyEvent object containing information about the key press.
        """
        key = event.key()
        if key == Qt.Key_Escape:
            self.close()  # Exit the application
        elif key == Qt.Key_W:
            gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_LINE)  # Switch to wireframe rendering
        elif key == Qt.Key_S:
            gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_FILL)  # Switch to solid fill rendering
        # Trigger a redraw to apply changes
        self.update()
        # Call the base class implementation for any unhandled events
        super().keyPressEvent(event)


class DebugApplication(QApplication):
    """
    A custom QApplication subclass for improved debugging.

    By default, Qt's event loop can suppress exceptions that occur within event handlers
    (like paintGL or mouseMoveEvent), making it very difficult to debug as the application
    may simply crash or freeze without any error message. This class overrides the `notify`
    method to catch these exceptions, print a full traceback to the console, and then
    re-raise the exception to halt the program, making the error immediately visible.
    """

    def __init__(self, argv):
        super().__init__(argv)

    def notify(self, receiver, event):
        """
        Overrides the central event handler to catch and report exceptions.
        """
        try:
            # Attempt to process the event as usual
            return super().notify(receiver, event)
        except Exception:
            # If an exception occurs, print the full traceback
            traceback.print_exc()
            # Re-raise the exception to stop the application
            raise


if __name__ == "__main__":
    # Create a QSurfaceFormat object to request a specific OpenGL context
    format: QSurfaceFormat = QSurfaceFormat()
    # Request 4x multisampling for anti-aliasing
    format.setSamples(4)
    # Request OpenGL version 4.1 as this is the highest supported on macOS
    format.setMajorVersion(4)
    format.setMinorVersion(1)
    # Request a Core Profile context, which removes deprecated, fixed-function pipeline features
    format.setProfile(QSurfaceFormat.CoreProfile)
    # Request a 24-bit depth buffer for proper 3D sorting
    format.setDepthBufferSize(24)
    # Set default format for all new OpenGL contexts
    QSurfaceFormat.setDefaultFormat(format)

    # Check for a "--debug" command-line argument to run the DebugApplication
    if len(sys.argv) > 1 and "--debug" in sys.argv:
        app = DebugApplication(sys.argv)
    else:
        app = QApplication(sys.argv)

    # Create the main window
    window = MainWindow()
    window.resize(800, 600)
    # Show the window
    window.show()
    # Start the application's event loop
    sys.exit(app.exec())
