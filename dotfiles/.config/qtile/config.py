# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import subprocess
from time import time
from pathlib import Path
from typing import List  # noqa: F401

from libqtile import bar, layout, widget, hook
from libqtile.config import Click, Drag, Group, Key, Screen
from libqtile.lazy import lazy

mod = "mod4"
terminal = "alacritty"
my_home = os.path.expanduser('~/')
my_config = my_home + ".config/qtile/"

def screenshot(save=True, copy=True, mode="full"):
    def f(qtile):
        path = Path.home() / 'Imagens'
        path /= f'screenshot_{str(int(time() * 100))}.png'
        
        if mode == "full":
            shot = subprocess.run(['maim'], stdout=subprocess.PIPE)
        elif mode == 'select':
            shot = subprocess.run(['maim', '-s'], stdout=subprocess.PIPE)
        elif mode == 'window':
            window = subprocess.run(['xdotool', 'getactivewindow'], stdout=subprocess.PIPE)
            shot = subprocess.run(['maim', '-i', window.stdout], stdout=subprocess.PIPE)

        if save:
            with open(path, 'wb') as sc:
                sc.write(shot.stdout)

        if copy:
            subprocess.run(['xclip', '-selection', 'clipboard', '-t', 'image/png'], input=shot.stdout)

    return f

keys = [
    Key([mod], "k", lazy.layout.down(),
        desc="Move focus down in stack pane"),
    Key([mod], "j", lazy.layout.up(),
        desc="Move focus up in stack pane"),
    Key([mod, "control"], "k", lazy.layout.shuffle_down(),
        desc="Move window down in current stack "),
    Key([mod, "control"], "j", lazy.layout.shuffle_up(),
        desc="Move window up in current stack "),
    Key([mod], "space", lazy.layout.next(),
        desc="Switch window focus to other pane(s) of stack"),
    Key([mod, "shift"], "space", lazy.layout.rotate(),
        desc="Swap panes of split stack"),
    Key([mod, "shift"], "Return", lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack"),
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod, "shift"], "Tab", lazy.prev_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "control"], "r", lazy.restart(), desc="Restart qtile"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown qtile"),
    Key([mod], "r", lazy.spawncmd(),
        desc="Spawn a command using a prompt widget"),

    ### MY KEYS ###
    Key([mod], "m", lazy.window.toggle_floating(), desc="Floating window"),
    
    Key([], "Print", lazy.function(screenshot())),
    Key([mod], "Print", lazy.function(screenshot(mode='select'))),
    Key([mod, "shift"], "Print", lazy.function(screenshot(mode='window'))),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    Key([mod, "shift"], "Return", lazy.spawn(terminal + " -t=float"), desc="Launch terminal"),
    Key([mod], "d", lazy.spawn("rofi -show drun"), desc="Launch rofi"),
    Key([mod], "g", lazy.spawn("google-chrome-stable"), desc="Launch Google Chrome"),
    Key([mod], "t", lazy.spawn("telegram-desktop"), desc="Launch Telegram"),
    Key([mod], "v", lazy.spawn("vscodium"), desc="Launch Vscodium"),
    Key([mod], "f", lazy.spawn("thunar"), desc="Launch Thunar"),
    Key([mod], "s", lazy.spawn("spotify"), desc="Launch Spotify"),
]

colors = [
    '#000000', #  0
    '#05FFB8', #  1
    '#05F2AF', #  2
    '#04D99D', #  3
    '#04BF8A', #  4
    '#03A678', #  5
    '#038C65', #  6
    '#027353', #  7
    '#025940', #  8
    '#FFFFFF', #  9
    '#F2CD5C', # 10
    '#037F8C', # 11
    '#8563A6', # 12
    '#FA00AF', # 13
    '#FB0DA8', # 14
    '#FB0097', # 15
    '#FB0D90', # 16
    '#FB007E', # 17
    '#FB0D78', # 18
    '#FB0064', # 19
    '#FB0D60', # 20
]

d_colors = [
    ['#413646','#413646'], #  0
    ['#3B4A69','#3B4A69'], #  1
    ['#847089','#847089'], #  2
    ['#FB0097','#FB0097'], #  3
    ['#FF00BF','#FF00BF'], #  4
    ['#B38F8F','#B38F8F'], #  5
    ['#826B5B','#826B5B'], #  6
    ['#A0906F','#A0906F'], #  7
    ['#ECB95D','#ECB95D'], #  8
    ['#FFD09C','#FFD09C'], #  9
    ['#FDF46B','#FDF46B'], # 10
    ['#05FFB8','#05FFB8'], # 11
]

my_fonts = [
    'JetBrainsMono Nerd Font',
    'JetBrainsMono Nerd Font Mono',
    'Terminus',
    'TerminessTTF Nerd Font',
    'TerminessTTF Nerd Font Mono',
    'Font Awesome 5 Free',
    'Font Awesome 5 Free Solid',
]

groups = [
    Group("1",label="\uf120",layout="bsp"),
    Group("2",label="\uf121",layout="tile"),
    Group("3",label="\uf268",layout="max"),
    Group("4",label="\uf075",layout="bsp"),
    Group("5",label="\uf1bc",layout="tile"),
    Group("6",label="\uf4b8",layout="tile"),
    Group("7",label="\uf86d",layout="tile"),
    Group("8",label="\uf21b",layout="bsp"),
]

for i in groups:
    keys.extend([
        Key([mod], i.name, lazy.group[i.name].toscreen(),
            desc="Switch to group {}".format(i.name)),
        Key([mod, "shift"], i.name, lazy.window.togroup(i.name, switch_group=False),
            desc="Switch to & move focused window to group {}".format(i.name)),
    ])

layout_theme = {
    "border_focus": "05FFB8",
    "border_normal": "038C65",
    "border_width": 3,
    "margin": 3,
}

layouts = [
    layout.Tile(
        **layout_theme,
        add_after_last = True,
        ratio = 0.60
    ),
    layout.Max(),
    layout.Bsp(
        **layout_theme,
        ratio = 1,
        fair = False,
    ),
    #layout.MonadTall(
    #    **layout_theme,
    #),
    # layout.Stack(num_stacks=2),
    # layout.Columns(),
    # layout.Matrix(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font = my_fonts[2],
    fontsize = 16,
    foreground = colors[9],
    padding = 6,
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.TextBox(
                    font = my_fonts[1],
                    fontsize = 30,
                    foreground = colors[1],
                    text='\uf303',
                    mouse_callbacks = {'Button1': lambda qtile: qtile.cmd_spawn('rofi -show drun')},
                ),
                widget.CurrentLayout(),
                widget.GroupBox(
                    font = my_fonts[6],
                    fontsize = 18,
                    rounded = False,
                    borderwidth = 0,
                    margin_y = 3,
                    padding_y = 3,
                    this_current_screen_border = d_colors[11],
                    urgent_border = colors[15],
                    highlight_method = 'block',
                    highlight_color = colors[11],
                    block_highlight_text_color = colors[0],
                    active = colors[1],
                    inactive = colors[8],
                    disable_drag = True,
                ),
                widget.TaskList(
                    margin_y = 1,
                    padding_y = 5,
                    rounded = False,
                    border = d_colors[11],
                    unfocused_border = colors[10],
                    foreground = colors[0],
                    highlight_method = 'block',
                    icon_size = 0,
                    title_width_method = 'uniform',
                ),
                #widget.Chord(
                #    chords_colors={
                #        'launch': ("#ff0000", "#ffffff"),
                #    },
                #    font = my_fonts[2],
                #    #fontsize = 20,
                #    fmt = 'TESTE {}',
                #    name_transform=lambda name: name.upper(),
                #),
                widget.Systray(),
                widget.Sep(
                    foreground = colors[0],
                    linewidth = 3,
                ),
                widget.DF( # DISK USAGE
                    #background = d_colors[0],
                    #foreground = colors[9],
                    measure = 'G',
                    partition = '/',
                    fmt = '<span face="' + my_fonts[6] + '" foreground="' + colors[15] + '">\uf0a0</span> {}',
                    format = '{p} {r:.0f}%',
                    visible_on_warn = False,
                    mouse_callbacks = {'Button1': lambda qtile: qtile.cmd_spawn(terminal + ' -t=float -e=ranger')},
                ),
                widget.CPU( # CPU USAGE
                    #background = d_colors[1],
                    #foreground = colors[9],
                    fmt = '<span face="' + my_fonts[6] + '" foreground="' + colors[10] + '">\uf2db</span> {}',
                    format = '{load_percent}%',
                    mouse_callbacks = {'Button1': lambda qtile: qtile.cmd_spawn(terminal + ' -t=float -e=htop')},
                ),
                widget.Memory( # MEMORY USAGE
                    #background = d_colors[2],
                    #foreground = colors[9],
                    fmt = '<span face="' + my_fonts[6] + '" foreground="' + colors[1] + '">\uf538</span> {}',
                    format = '{MemUsed}MB',
                    mouse_callbacks = {'Button1': lambda qtile: qtile.cmd_spawn(terminal + ' -t=float -e=htop')},
                ),
                widget.Wlan( # WLAN
                    #background = d_colors[5],
                    #foreground = colors[9],
                    interface = 'wlp2s0',
                    fmt = '<span face="' + my_fonts[6] + '" foreground="' + colors[20] + '">\uf1eb</span> {}',
                    format = '{essid}',
                    mouse_callbacks = {'Button1': lambda qtile: qtile.cmd_spawn(terminal + ' -t=float -e=nmtui')},
                ),
                widget.PulseVolume( # VOLUME
                    fmt = '<span face="' + my_fonts[6] + '" foreground="' + colors[5] + '">\uf028</span> {}',
                ),
                widget.Clock( # DATE
                    fmt = '<span face="' + my_fonts[6] + '" foreground="' + colors[10] + '">\uf073</span> {}',
                    format = '%a.%d.%m',
                ),
                widget.Clock( # CLOCK
                    fmt = '<span face="' + my_fonts[6] + '" foreground="' + colors[2] + '">\uf017</span> {}',
                    format = '%H:%M',
                ),
                widget.QuickExit( # EXIT
                    font = my_fonts[2],
                    foreground = colors[1],
                    countdown_format = '{}s',
                    default_text = '\uf011',
                ),
                widget.CheckUpdates(
                    colour_have_updates = colors[9],
                    colour_no_updates = colors[9],
                    background = colors[10],
                    foreground = colors[9],
                    mouse_callbacks = {'Button1': lambda qtile: qtile.cmd_spawn(terminal + ' -t=float -e sudo pacman -Syyu')},
                    distro = 'Arch',
                    fmt = '\uf2f1 {}',
                    display_format = '{updates}',
                    no_update_string = '0',
                ),
            ],
            28,
            opacity = 1.0,
            margin = [0,0,0,0],
        ),
        #left = bar.Gap(3),
        #right = bar.Gap(3),
        #bottom = bar.Gap(3),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
main = None  # WARNING: this is deprecated and will be removed soon
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(
    **layout_theme,
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        {'wmclass': 'confirm'},
        {'wmclass': 'dialog'},
        {'wmclass': 'download'},
        {'wmclass': 'error'},
        {'wmclass': 'file_progress'},
        {'wmclass': 'notification'},
        {'wmclass': 'splash'},
        {'wmclass': 'toolbar'},
        {'wmclass': 'confirmreset'},  # gitk
        {'wmclass': 'makebranch'},  # gitk
        {'wmclass': 'maketag'},  # gitk
        {'wname': 'branchdialog'},  # gitk
        {'wname': 'pinentry'},  # GPG key password entry
        {'wmclass': 'ssh-askpass'},  # ssh-askpass
        {'wmclass': 'galculator'},  # galculator
        {'wmclass': 'pamac-manager'},  # pamac
        #{'wmclass': 'Alacritty'},  # alacritty
        {'wname': 'float'},  # generic floating windows
    ]
)
auto_fullscreen = True
focus_on_window_activation = "focus"

### MY FUNCTIONS ###

#  AUTOSTART  #

@hook.subscribe.startup_once
def autostart():
    subprocess.call([my_home + '.config/qtile/autostart.sh'])

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
