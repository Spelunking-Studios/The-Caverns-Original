from array import array
from stgs import asset

class Shader:
    vert_shader = '''
    #version 330 core

    in vec2 vert;
    in vec2 texcoord;
    out vec2 uvs;

    void main() {
        uvs = texcoord;
        gl_Position = vec4(vert, 0.0, 1.0);
    }
    '''

    def __init__(self, display, frag_path="swizzle.frag", properties = {}):
        self.display = display
        self.properties = properties
        self.active = True
        self.frag_path = frag_path
        self.load(self.display.ctx)

    def load(self, ctx):
        quad_buffer = ctx.buffer(data=array('f', [
            # position (x, y), uv coords (x, y)
            -1.0, 1.0, 0.0, 0.0,  # topleft
            1.0, 1.0, 1.0, 0.0,   # topright
            -1.0, -1.0, 0.0, 1.0, # bottomleft
            1.0, -1.0, 1.0, 1.0,  # bottomright
        ]))

        with open( asset("shaders/" + self.frag_path) , "r") as file:
            self.frag_shader = file.read()
        
        self.program = ctx.program(vertex_shader=self.vert_shader, fragment_shader=self.frag_shader)
        self.fbo = ctx.framebuffer(color_attachments=[ctx.texture(self.display.get_size(), 4)])
        self.render_object = ctx.vertex_array(self.program, [(quad_buffer, '2f 2f', 'vert', 'texcoord')])

    def update(self, t=0):
        # Update time if necessary
        if "time" in self.properties:
            self.properties["time"] = t

        # Load our properties into the shader
        for k,v in self.properties.items():
            self.program[k] = v



