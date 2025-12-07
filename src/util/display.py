import pygame
import pygame_light2d as pl2d
from pygame_light2d import LightingEngine, PointLight
from src.stgs import winFlags, keySet, now, asset, TITLE, CURSOR, iconPath, DEBUG


class Display:
    def __init__(self, game):
        self.game = game
        self.resolution = self.get_modes()[0]
        # self.display = pygame.display.set_mode(self.resolution, winFlags)
        pygame.display.set_caption(TITLE)
        # pygame.display.set_icon(pygame.image.load(iconPath))
        # self.display.convert(32, pygame.RLEACCEL)
        self.fullScreen = False
        self.last_pressed_fullscreen = 0
        self.light_engine = LightingEngine(self.resolution, self.resolution, (320, 180))
        self.light_engine.set_ambient(10, 10, 10)


        self.cursor = pygame.image.load(CURSOR) if CURSOR else False
        self.cursor_tex = None
        self.cursor = pygame.transform.scale(self.cursor, (16, 16))
        if CURSOR:
            pygame.mouse.set_visible(False)
            self.cursor_tex = self.light_engine.surface_to_texture(self.cursor)

        if DEBUG:
            print(
                pygame.display.get_wm_info(),
                self.resolution,
                pygame.display.get_desktop_sizes()
            )


    def add_shader(self, vert, frag):
        """Takes vertex and fragment shader paths

           Currently doesn't do anything since shaders need to be passed to texture renderings"""

        return self.light_engine.graphics.load_shader_from_path(vert, frag)
    
    def add_light(self, light):
        self.light_engine.lights.append(light)

    def remove_light(self, light):
        self.light_engine.lights.remove(light)

    def get_fullscreen(self):
        keys = pygame.key.get_pressed()
        if now() - self.last_pressed_fullscreen > 200 and keys[keySet['fullScreen']]:
            self.last_pressed_fullscreen = now()
            self.toggle_fullscreen()

    def toggle_fullscreen(self):
            if self.fullScreen:
                self.fullScreen = False
            else:
                self.fullScreen = True
            pygame.display.toggle_fullscreen()
            pygame.display.set_icon(pygame.image.load(iconPath))
    
    def update(self, bg, fg=None):
        # See if the player toggles fullscreen
        self.get_fullscreen()
        self.light_engine.clear(0, 0, 0)

        if bg:
            bg_tex = self.light_engine.surface_to_texture(bg)
            self.light_engine.render_texture(
                bg_tex, pl2d.BACKGROUND,
                pygame.Rect(0, 0, *self.resolution),
                pygame.Rect(0, 0, bg_tex.width, bg_tex.height))
            bg_tex.release()

        if fg:
            fg_tex = self.light_engine.surface_to_texture(fg)
            self.light_engine.render_texture(
                fg_tex, pl2d.FOREGROUND,
                pygame.Rect(0, 0, *self.resolution),
                pygame.Rect(0, 0, fg_tex.width, fg_tex.height))
            fg_tex.release()

        if self.cursor:
            x, y = pygame.mouse.get_pos()
            cursor_rect = pygame.Rect(x, y, *self.cursor.get_size())
            self.light_engine.render_texture(self.cursor_tex, 
                pl2d.FOREGROUND,
                cursor_rect, 
                cursor_rect.move_to(topleft=(0,0)))
        self.light_engine.render()

        pygame.display.flip()


    def get_size(self):
        return self.resolution

    def get_offset(self):
        # offset =  pygame.Vector2((self.get_size()[0]-self.game.width())/2, (self.get_size()[1]-self.game.height())/2)
        offset = (0, 0)
        return offset

    def get_modes(self):
        return pygame.display.get_desktop_sizes()

    def get_mode(self):
        return self.resolution

    def set_mode(self, mode):
        print(mode)
        self.resolution = mode
        # self.display = pygame.display.set_mode(self.resolution, winFlags)
        self.game.win = pygame.Surface(self.resolution)

