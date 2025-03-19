import pygame
import moderngl
from src.shaders import ShaderManager, Shader
from src.stgs import *

class Display:

    def __init__(self):
        self.resolution = pygame.display.list_modes()[0]
        # self.display = pygame.display.set_mode(self.resolution)
        self.display = pygame.display.set_mode((winWidth, winHeight), winFlags)
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(pygame.image.load(iconPath))
        self.display.convert(32, pygame.RLEACCEL) 
        self.fullScreen = False
        self.last_pressed_fullscreen = 0

        # Set up shader target
        self.ctx = moderngl.create_context()
        self.shaderManager = ShaderManager(self, [
            Shader(self, "blank.frag"),
            # Shader(self, "lightning.frag", {"time": 0})
        ])

    def getFullScreen(self):
        keys = pygame.key.get_pressed()
        if now() - self.last_pressed_fullscreen > 200 and keys[keySet['fullScreen']]:
            self.last_pressed_fullscreen = now()
            if self.fullScreen:
                self.display = pygame.display.set_mode((winWidth, winHeight), winFlags)
                self.fullScreen = False
            else:
                self.display = pygame.display.set_mode((winWidth, winHeight), winFlags | pygame.FULLSCREEN)
                self.fullScreen = True
            pygame.display.set_icon(pygame.image.load(iconPath))
            #pygame.display.toggle_fullscreen()
    
    def update(self, window):
        # See if the player toggles fullscreen
        self.getFullScreen()

        self.display.blit(window, (0, 0)) 
        frame_texture = self.get_frame() # Convert display to shader texture
        self.shaderManager.apply(frame_texture)

        self.ctx.screen.use()
        self.ctx.clear()
        self.shaderManager.render()

        pygame.display.flip()
        frame_texture.release()

    # Blit passthrough
    def blit(self, img, rect):
        self.display.blit(img, rect)
    
    def get_size(self):
        return self.display.get_size()

    def get_frame(self, surf=None):
        if not surf:
            surf = self.display

        tex = self.ctx.texture(surf.get_size(), 4)
        tex.filter = (moderngl.NEAREST, moderngl.NEAREST)
        tex.swizzle = 'BGRA'
        tex.write(surf.get_view('1'))
        return tex
    
    def render_pass(shader_pass, texture):
        """Render a pass using the given framebuffer, input texture, and shader program"""
        shader_pass.fbo.use()
        self.ctx.clear()
        texture.use(0)
        shader_pass.program['tex'] = 0
        shader_pass.render_object.render(mode=moderngl.TRIANGLE_STRIP)

