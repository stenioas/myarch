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
from typing import List  # noqa: F401

from libqtile import bar, layout, widget, hook
from libqtile.config import Click, Drag, Group, Key, Screen
from libqtile.lazy import lazy

mod = "mod4"
terminal = "xfce4-terminal"

keys = [
    # Switch between windows in current stack pane
    Key([mod], "k", lazy.layout.down(),
        desc="Move focus down in stack pane"),
    Key([mod], "j", lazy.layout.up(),
        desc="Move focus up in stack pane"),

    # Move windows up or down in current stack
    Key([mod, "control"], "k", lazy.layout.shuffle_down(),
        desc="Move window down in current stack "),
    Key([mod, "control"], "j", lazy.layout.shuffle_up(),
        desc="Move window up in current stack "),

    # Switch window focus to other pane(s) of stack
    Key([mod], "space", lazy.layout.next(),
        desc="Switch window focus to other pane(s) of stack"),

    # Swap panes of split stack
    Key([mod, "shift"], "space", lazy.layout.rotate(),
        desc="Swap panes of split stack"),

    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key([mod, "shift"], "Return", lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack"),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),

    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),

    Key([mod, "control"], "r", lazy.restart(), desc="Restart qtile"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown qtile"),
    Key([mod], "r", lazy.spawncmd(),
        desc="Spawn a command using a prompt widget"),

    ### MY KEYS ###
    Key([mod], "g", lazy.spawn("google-chrome-stable"), desc="Launch Google Chrome"),
    Key([mod], "t", lazy.spawn("telegram-desktop"), desc="Launch Telegram"),
    Key([mod], "v", lazy.spawn("vscodium"), desc="Launch Vscodium"),
    Key([mod], "f", lazy.spawn("thunar"), desc="Launch Thunar"),
    Key([mod], "s", lazy.spawn("spotify"), desc="Launch Spotify"),
]

colors = [
    ['#000000','#000000'], #  0
    ['#05FFB8','#05FFB8'], #  1
    ['#05F2AF','#05F2AF'], #  2
    ['#04D99D','#04D99D'], #  3
    ['#04BF8A','#04BF8A'], #  4
    ['#03A678','#03A678'], #  5
    ['#038C65','#038C65'], #  6
    ['#027353','#027353'], #  7
    ['#025940','#025940'], #  8
    ['#FFFFFF','#FFFFFF'], #  9
    ['#F2CD5C','#F2CD5C'], # 10
    ['#037F8C','#037F8C'], # 11
    ['#8563A6','#8563A6'], # 12
    ['#F25C69','#F25C69'], # 13
]

groups = [
    Group("1",label="\uf120",layout="bsp"),
    Group("2",label="\uf121",layout="tile"),
    Group("3",label="\uf268",layout="tile"),
    Group("4",label="\uf3fe",layout="bsp"),
    Group("5",label="\uf58f",layout="tile"),
    Group("6",label="\uf4b8",layout="tile"),
    Group("7",label="\uf86d",layout="tile"),
    Group("8",label="\uf5fc",layout="tile"),
]

for i in groups:
    keys.extend([
        # mod1 + letter of group = switch to group
        Key([mod], i.name, lazy.group[i.name].toscreen(),
            desc="Switch to group {}".format(i.name)),

        # mod1 + shift + letter of group = switch to & move focused window to group
        Key([mod, "shift"], i.name, lazy.window.togroup(i.name, switch_group=True),
            desc="Switch to & move focused window to group {}".format(i.name)),
        # Or, use below if you prefer not to switch to that group.
        # # mod1 + shift + letter of group = move focused window to group
        # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
        #     desc="move focused window to group {}".format(i.name)),
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
    layout.MonadTall(
        **layout_theme,
    ),
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
    font='Terminus',
    fontsize=16,
    padding=3,
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.TextBox(
                    font = 'TerminessTTF Nerd Font',
                    fontsize = 18,
                    padding = 10,
                    text='\uf303',
                    foreground = colors[1],
                    #mouse_callbacks = {'Button1': lambda qtile: qtile.cmd_spawn('dmenu')},
                ),
                widget.GroupBox(
                    font = 'Font Awesome 5 Free Solid',
                    rounded = True,
                    borderwidth = 0,
                    highlight_method = 'line',
                    highlight_color = colors[1],
                    block_highlight_text_color = colors[0],
                    active = colors[1],
                    padding = 5,
                ),
                widget.Prompt(
                    foreground = colors[1],
                    prompt = '> ',
                ),
                widget.Sep(
                    foreground = colors[0],
                    linewidth = 1,
                ),
                widget.WindowName(
                    empty_group_string = 'No focus',
                    foreground = colors[2],
                    show_state = False,
                ),
                widget.Chord(
                    chords_colors={
                        'launch': ("#ff0000", "#ffffff"),
                    },
                    name_transform=lambda name: name.upper(),
                ),
                widget.Systray(),
                widget.Sep( # DISK USAGE
                    foreground = colors[0],
                    linewidth = 1,
                ),
                widget.TextBox(
                    font = 'Font Awesome 5 Free Solid',
                    fontsize = 18,
                    padding = 0,
                    text='\ue0b2',
                    foreground = colors[8],
                ),
                widget.TextBox(
                    font = 'Font Awesome 5 Free Solid',
                    text='\uf0a0',
                    background = colors[8],
                    foreground = colors[1],
                ),
                widget.DF(
                    background = colors[8],
                    foreground = colors[1],
                    measure = 'G',
                    partition = '/',
                    format = '{r:.0f}%',
                    visible_on_warn = False,
                ),
                widget.TextBox(
                    font = 'Font Awesome 5 Free Solid',
                    fontsize = 18,
                    padding = 0,
                    text='\ue0b2',
                    background = colors[8],
                    foreground = colors[7],
                ),
                widget.TextBox(
                    font = 'Font Awesome 5 Free',
                    text='\uf2db',
                    background = colors[7],
                    foreground = colors[1],
                ),
                widget.CPU(
                    background = colors[7],
                    foreground = colors[1],
                    format = '{load_percent}%',
                ),
                widget.TextBox(
                    font = 'Font Awesome 5 Free',
                    text='\uf76b',
                    background = colors[7],
                    foreground = colors[1],
                ),
                widget.ThermalSensor(
                    background = colors[7],
                    foreground = colors[1],
                ),
                widget.TextBox(
                    font = 'Font Awesome 5 Free Solid',
                    fontsize = 18,
                    padding = 0,
                    text='\ue0b2',
                    background = colors[7],
                    foreground = colors[6],
                ),
                widget.TextBox(
                    font = 'Font Awesome 5 Free Solid',
                    text='\uf538',
                    background = colors[6],
                    foreground = colors[1],
                ),
                widget.Memory(
                    background = colors[6],
                    foreground = colors[1],
                    format = '{MemUsed}MB',
                ),
                widget.TextBox(
                    font = 'Font Awesome 5 Free',
                    text='\uf76b',
                    background = colors[6],
                    foreground = colors[1],
                ),
                widget.ThermalSensor(
                    background = colors[6],
                    foreground = colors[1],
                    tag_sensor = 'temp1',
                ),
                #widget.Sep( # KEYBOARD
                #    foreground = colors[0],
                #    linewidth = 1,
                #),
                #widget.TextBox(
                #    font = 'Font Awesome 5 Free Solid',
                #    text='\uf11c',
                #    background = colors[1],
                #    foreground = colors[0],
                #),
                #widget.KeyboardLayout(
                #    background = colors[1],
                #    foreground = colors[0],
                #    configured_keyboards = ['br', 'us'],
                #),
                widget.TextBox(
                    font = 'Font Awesome 5 Free Solid',
                    fontsize = 18,
                    padding = 0,
                    text='\ue0b2',
                    background = colors[6],
                    foreground = colors[5],
                ),
                widget.TextBox(
                    font = 'Font Awesome 5 Free Solid',
                    text='\uf1eb',
                    background = colors[5],
                    foreground = colors[8],
                ),
                widget.Wlan(
                    background = colors[5],
                    foreground = colors[8],
                    interface = 'wlp2s0',
                    format = '{essid} {percent:2.0%}',
                    mouse_callbacks = {'Button1': lambda qtile: qtile.cmd_spawn(terminal + ' -T=float -e=nmtui')},
                ),
                widget.TextBox( # NET USAGE
                    font = 'Font Awesome 5 Free',
                    text='\uf381',
                    background = colors[5],
                    foreground = colors[8],
                ),
                widget.Net(
                    background = colors[5],
                    foreground = colors[8],
                    format = '{down}',
                    update_interval = 2,
                ),
                widget.TextBox(
                    font = 'Font Awesome 5 Free Solid',
                    fontsize = 18,
                    padding = 0,
                    text='\ue0b2',
                    background = colors[5],
                    foreground = colors[4],
                ),
                widget.TextBox(
                    font = 'Font Awesome 5 Free Solid',
                    text='\uf028',
                    background = colors[4],
                    foreground = colors[8],
                ),
                widget.PulseVolume(
                    background = colors[4],
                    foreground = colors[8],
                ),
                widget.TextBox(
                    font = 'Font Awesome 5 Free Solid',
                    fontsize = 18,
                    padding = 0,
                    text='\ue0b2',
                    background = colors[4],
                    foreground = colors[3],
                ),
                widget.TextBox(
                    font = 'Font Awesome 5 Free Solid',
                    text='\uf073',
                    background = colors[3],
                    foreground = colors[8],
                ),
                widget.Clock(
                    background = colors[3],
                    foreground = colors[8],
                    format = '%a.%d.%m',
                ),
                widget.TextBox(
                    font = 'Font Awesome 5 Free Solid',
                    fontsize = 18,
                    padding = 0,
                    text='\ue0b2',
                    background = colors[3],
                    foreground = colors[2],
                ),
                widget.TextBox(
                    font = 'Font Awesome 5 Free Solid',
                    text='\uf017',
                    background = colors[2],
                    foreground = colors[8],
                ),
                widget.Clock(
                    background = colors[2],
                    foreground = colors[8],
                    format = '%H:%M',
                ),
                widget.TextBox(
                    font = 'Font Awesome 5 Free Solid',
                    fontsize = 18,
                    padding = 0,
                    text='\ue0b2',
                    background = colors[2],
                    foreground = colors[1],
                ),
                widget.CurrentLayout(
                    background = colors[1],
                    foreground = colors[8],
                ),
                widget.CurrentLayoutIcon(
                    scale = 0.75,
                ),
                widget.CheckUpdates(
                    colour_have_updates = colors[7],
                    colour_no_updates = colors[0],
                    background = colors[1],
                    foreground = colors[0],
                    mouse_callbacks = {'Button1': lambda qtile: qtile.cmd_spawn(terminal + ' -e sudo pacman -Syu')},
                    distro = 'Arch',
                    display_format = '\uf2f1 {updates}',
                ),
                #widget.QuickExit(
                #    background = colors[1],
                #    foreground = colors[0],
                #    countdown_format = '{}s',
                #    default_text = '\uf011',
                #    padding = 5,
                #),
            ],
            24,
            opacity = 0.85,
            margin = [0,0,3,0],
        ),
        left = bar.Gap(3),
        right = bar.Gap(3),
        bottom = bar.Gap(3),
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
        {'wname': 'float'},  # generic floating windows
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"

#  AUTOSTART #

@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser('~/.config/qtile/autostart.sh')
    subprocess.call([home])
