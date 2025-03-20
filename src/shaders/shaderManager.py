import moderngl
from .shader import Shader
class ShaderManager:
    def __init__(self, display, shaders = []):
        self.display = display
        self.shaders = shaders
        if len(shaders)%2:
            shaders.append(Shader(self.display, "blank.frag"))
        
        self.time = 0

    def render(self, target = 0):
        """ This is unexplainable wizardry. Do not inquire
        """
        last = self.get_active()[-1]
        last.fbo.color_attachments[0].use(target)
        last.render_object.render(mode=moderngl.TRIANGLE_STRIP)

    def get_active(self):
        return [shader for shader in self.shaders if shader.active]

    def add_shader(self, shader):
        self.shaders.append(shader)
        if len(shaders)%2:
            shaders.append(Shader(self.display, "blank.frag"))

    def render_pass(self, shader_pass, texture):
        """Render a pass using the given framebuffer, input texture, and shader program"""
        shader_pass.fbo.use()
        self.display.ctx.clear()
        texture.use(0)
        # if not shader_pass.properties.["no_tex"]:
        #     shader_pass.program['tex'] = 0
        shader_pass.render_object.render(mode=moderngl.TRIANGLE_STRIP)

    def update(self):
        self.time += 1
        for shader in self.get_active():
            shader.update(self.time)

    def apply(self, frame_texture):
        active = self.get_active()

        self.render_pass(active[0], frame_texture)
        for i in range(1, len(active)):
            # Use previous shaders color attachment to stack effects
            self.render_pass(active[i], active[i-1].fbo.color_attachments[0])

    def reload(self):
        for shader in self.shaders:
            shader.load(self.display.ctx)
