import random
import sys
import xbmc
import xbmcaddon
import xbmcgui

addon = xbmcaddon.Addon()
monitor = xbmc.Monitor()


class screensaver(xbmcgui.WindowXMLDialog):
    def __init__(self, *args, **kwargs):
        self.corner = 0
        self.side_walls = 0
        self.top_bottom = 0
        self.exit = False
        self.width_direction = True
        self.height_direction = True
        self.display_logo = addon.getSetting("display_logo")
        self.speed = int(addon.getSetting("speed"))
        self.speed /= 100
        if "DVD" in self.display_logo:
            self.actual_logo = "dvd.png"
        if "Blu-ray" in self.display_logo:
            self.actual_logo = "blu_ray.png"
        if "3D Blu-ray" in self.display_logo:
            self.actual_logo = "3d_blu_ray.png"
        if "Evolve" in self.display_logo:
            self.actual_logo = "splash_blue_ico.png"
        if "Custom" in self.display_logo:
            self.actual_logo = addon.getSetting("custom_logo")

    def onInit(self):
        self.logo = self.getControl(50)
        self.logo_width = int(self.logo.getWidth())
        self.logo_height = int(self.logo.getHeight())
        self.logo.setImage(self.actual_logo, False)
        # self.logo.setLabel("JENNA")
        self.screen_width = self.getWidth()
        self.screen_height = self.getHeight()
        self.width = random.randint(1, self.screen_width)
        self.height = random.randint(1, self.screen_height)
        self.logo.setPosition(int(self.width), int(self.height))
        self.exit_monitor = self.MonitorExit(self.exit_screen)
        while not self.exit:
            self.movement()
            monitor.waitForAbort(.032)

    def random_color(self):
        def r(): return random.randint(0, 255)
        return '0xC0%02X%02X%02X' % (r(), r(), r())

    def change_color(self):
        self.logo.setColorDiffuse(self.random_color())

    def hit_corner(self):
        self.logo.setColorDiffuse('0xC0FF00FF')

    def movement(self):
        if self.width_direction:
            if self.width > (self.screen_width-self.logo_width):
                self.change_color()
                self.width_direction = False
                self.width = self.screen_width-self.logo_width
                self.side_walls += 1
            else:
                self.width += self.speed
        else:
            if self.width < 0:
                self.change_color()
                self.width_direction = True
                self.width = 0
                self.side_walls += 1
            else:
                self.width -= self.speed
        if self.height_direction:
            if self.height > (self.screen_height-self.logo_height):
                self.change_color()
                self.height_direction = False
                self.height = self.screen_height-self.logo_height
                self.top_bottom += 1
            else:
                self.height += self.speed
        else:
            if self.height < 0:
                self.change_color()
                self.height_direction = True
                self.height = 0
                self.top_bottom += 1
            else:
                self.height -= self.speed
        if self.width == 0 or self.width == (self.screen_width-self.logo_width):
            if self.height == 0:
                self.corner += 1
                self.hit_corner()
            elif self.height == (self.screen_height-self.logo_height):
                self.corner += 1
                self.hit_corner()
        self.logo.setPosition(self.width, self.height)

    def exit_screen(self):
        print("EXITING COMPLETE")
        self.exit = True
        self.close()

    class MonitorExit(xbmc.Monitor):
        def __init__(self, exit):
            self.exit = exit

        def onScreensaverDeactivated(self):
            self.exit()

    # def onAction(self, action):
    #     self.run=False
        # log = utls.log(name="screensaver_status")
        # log.notice("Corner Hits: {}".format(self.corner))
        # log.notice("Wall Hits: {}".format(self.side_walls))
        # log.notice("Top and Bottom Hits: {}".format(self.top_bottom))
        # self.close()


if __name__ == '__main__':
    screensaver = screensaver('evolve_screensaver.xml',
                              addon.getAddonInfo("path").decode("utf-8"),
                              'default',
                              '1080i')
    screensaver.doModal()
    del screensaver
    sys.modules.clear()
