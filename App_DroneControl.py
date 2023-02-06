import os
import sys
# ---------------------------------------------------------------------------------------------------
# - Screensize management                                                               -   START   -
# ---------------------------------------------------------------------------------------------------
from kivy import Config
# # setting Config screen data:
SCREENSIZE = (200, 200)

Config.set('graphics', 'width', str(SCREENSIZE[0]))
Config.set('graphics', 'height', str(SCREENSIZE[1]))
#
# setting kivy content size to max, and fullscreen to titlebared version
Config.set('graphics', 'fullscreen', 0)
Config.set('graphics', 'window_state', 'visible')  # hidden, visible, maximized
#
# # writing general kivy environment
Config.write()

from kivy.app import App  # necessary for the App class
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import AsyncImage
from kivy.uix.video import Video
from kivy.uix.videoplayer import VideoPlayer
from kivy.uix.camera import Camera, CoreCamera

# Window.maximize()

######################################################################
# Camera needs: opencv-python
# Video needs: ffpyplayer
######################################################################

class SalletScreenManager(ScreenManager):
    def __init__(self, **kwargs):
        super(SalletScreenManager, self).__init__(**kwargs)
        self.statedict = {
            "screen_main":  {
                "seq": 1,
                'inst': 'button_nav_main',
                'down': ['button_nav_main'],
                'normal': ["button_nav_intro"]},
            "screen_intro": {
                "seq": 0,
                'inst': 'button_nav_intro',
                'down': ['button_nav_intro'],
                'normal': ["button_nav_main"]}
            }


class NavBar(BoxLayout):
    """=== Class name: NavBar ==========================================================================================
    This Layout can be used across all screens. Class handles complications of now yet drawn instances.
    It sets appearance for instances only appearing on screen.
    ============================================================================================== by Sziller ==="""

    @ staticmethod
    def on_release_navbar(inst):
        """=== Method name: on_toggle_navbar ===========================================================================
        Method manages multiple screen selection by Toggle button set.
        All Toggle Buttons call this same function. Their Class names are stored in the <buttons> list.
        Only one button of the entire set is down at a given time. Function is extendable.
        Once a given button is 'down', it becomes inactive, all other buttons are activated and set to "normal" state.
        The reason of the logic is as follows:
        Screen manager is the unit taking care of actual screen swaps, also it stores actually shown screen name.
        However, at the itme of instantiation of the Screen Manager's ids are still not accessible.
        So we refer to ScreenManager's id's only on user action.
        :var inst: - the instance (button) activating the Method.
        ========================================================================================== by Sziller ==="""
        old_seq: int = 0
        for k, v in App.get_running_app().root.statedict.items():
            if k == App.get_running_app().root.current_screen.name:
                old_seq = v["seq"]
                break
        new_seq = App.get_running_app().root.statedict[inst.target]["seq"]

        App.get_running_app().change_screen(screen_name=inst.target, screen_direction={True: "left", False: "right"}
        [old_seq - new_seq < 0])
        for buttinst in App.get_running_app().root.current_screen.ids.navbar.ids:
            if buttinst in App.get_running_app().root.statedict[inst.target]['down']:
                App.get_running_app().root.current_screen.ids.navbar.ids[buttinst].disabled = True
                App.get_running_app().root.current_screen.ids.navbar.ids[buttinst].state = "normal"
            if buttinst in App.get_running_app().root.statedict[inst.target]['normal']:
                App.get_running_app().root.current_screen.ids.navbar.ids[buttinst].disabled = False
                App.get_running_app().root.current_screen.ids.navbar.ids[buttinst].state = "normal"

class OperationAreaBox(BoxLayout):
    pass


class OpAreaMain(OperationAreaBox):



    def on_press_dn_yaw(self, inst):
        print("yaw: <{:>8}>: {:>2}".format("pressed", inst.dir))

    def on_state_dn_yaw(self, inst):
        print("yaw      : <{:>8}>: {}".format("state:" + inst.state, inst.dir))

    def on_release_dn_yaw(self, inst):
        print("yaw      : <{:>8}>: {}".format("released", inst.dir))

    def on_press_dn_pitch(self, inst):
        print("pitch    : <{:>8}>: {:>2}".format("pressed", inst.dir))

    def on_state_dn_pitch(self, inst):
        print("pitch    : <{:>8}>: {}".format("state:" + inst.state, inst.dir))

    def on_release_dn_pitch(self, inst):
        print("pitch    : <{:>8}>: {}".format("released", inst.dir))

    def on_press_dn_roll(self, inst):
        print("roll     : <{:>8}>: {:>2}".format("pressed", inst.dir))

    def on_state_dn_roll(self, inst):
        print("roll     : <{:>8}>: {}".format("state:" + inst.state, inst.dir))

    def on_release_dn_roll(self, inst):
        print("roll     : <{:>8}>: {}".format("released", inst.dir))

    def on_press_dn_throttle(self, inst):
        print("throttle : <{:>8}>: {:>2}".format("pressed", inst.dir))

    def on_state_dn_throttle(self, inst):
        print("throttle : <{:>8}>: {}".format("state:" + inst.state, inst.dir))

    def on_release_dn_throttle(self, inst):
        print("throttle : <{:>8}>: {}".format("released", inst.dir))

class player(VideoPlayer):
    pass

class DroneControl(App):
    """=== Class name: CayMan ========================================================================================
    Child of built in class: App
    This is the Parent application for the Sealed of Kex manager project.
    Instantiation should - contrary to what is used on the net - happen by assigning it to a variable name.
    :param window_content:
    ============================================================================================== by Sziller ==="""
    def __init__(self, window_content: str, csm: float = 1.0):
        super(DroneControl, self).__init__()
        self.window_content = window_content
        self.content_size_multiplier = csm
        self.title = "DroneControl"

    def change_screen(self, screen_name, screen_direction="left"):
        """=== Method name: change_screen ==============================================================================
        Use this screenchanger instead of the built-in method for more customizability and to enable further
        actions before changing the screen.
        Also, if screenchanging first needs to be validated, use this method!
        ========================================================================================== by Sziller ==="""
        smng = self.root  # 'root' refers to the only one root instance in your App. Here it is the actual ROOT
        smng.current = screen_name
        smng.transition.direction = screen_direction

    def build(self):
        # vid = VideoPlayer(source = "./video/shoes2.mov")
        # vid.state = "play"
        # vid.options = {'eos': 'loop'}
        # vid.allow_stretch = True
        # return vid
        return self.window_content
        #return Camera(play=True)

class testcam(BoxLayout):
    def __init__(self, **kwargs):
        super(testcam, self).__init__(**kwargs)
        pass

if __name__ == "__main__":
    from kivy.lang import Builder  # to freely pick kivy files

    display_settings = {0: {'fullscreen': False, 'run': Window.maximize},
                        1: {'fullscreen': False, 'size': (600, 1000)},
                        2: {'fullscreen': False, 'size': (600, 400)},
                        3: {'fullscreen': False, 'size': (1000, 500)}}

    style_code = 3

    Window.fullscreen = display_settings[style_code]['fullscreen']
    if 'size' in display_settings[style_code].keys(): Window.size = display_settings[style_code]['size']
    if 'run' in display_settings[style_code].keys(): display_settings[style_code]['run']()

    try:
        content = Builder.load_file(str(sys.argv[1]))
    except IndexError:
        content = Builder.load_file("kivy_dronecontrol.kv")

    application = DroneControl(window_content=content, csm=1)
    application.run()