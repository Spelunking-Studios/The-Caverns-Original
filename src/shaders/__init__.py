import moderngl
import stgs

class ShaderPass:
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

    def __init__(self, game, frag_path="swizzle.frag", vert_path=False):
        self.game = game

        if vert_path:
            pass

        frag_shader_passes = {
                # "exposure": 1,
                # "bloomStrength": 1.5
        }
        self.frag_shader = ""

        with open(frag_path, "r") as file:
            self.frag_shader = file.read()
        
        self.program = ctx.program(vertex_shader=self.vert_shader, fragment_shader=self.frag_shader)
        self.fbo = ctx.framebuffer(color_attachments=[ctx.texture((800, 600), 4)])
        self.render_object = ctx.vertex_array(self.program, [(quad_buffer, '2f 2f', 'vert', 'texcoord')])



    def update(self, t=0):
        self.program["time"] = t

