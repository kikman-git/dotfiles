""" Kikman qtile config
"""

import os
import re
import socket
import subprocess
import psutil

from libqtile.config import (
    KeyChord,
    Key,
    Screen,
    Group,
    Drag,
    Click,
    ScratchPad,
    DropDown,
    Match,
)
from libqtile.command import lazy
from libqtile import layout, bar, widget, hook
from libqtile.lazy import lazy
from libqtile import qtile
from typing import List  # noqa: F401
from custom.bsp import Bsp as CustomBsp
# from custom.windowname import WindowName as CustomWindowName

mod = "mod4"
terminal = "alacritty"

## Resize functions for bsp layout
def resize(qtile, direction):
    layout = qtile.current_layout
    child = layout.current
    parent = child.parent

    while parent:
        if child in parent.children:
            layout_all = False

            if (direction == "left" and parent.split_horizontal) or (
                direction == "up" and not parent.split_horizontal
            ):
                parent.split_ratio = max(5, parent.split_ratio - layout.grow_amount)
                layout_all = True
            elif (direction == "right" and parent.split_horizontal) or (
                direction == "down" and not parent.split_horizontal
            ):
                parent.split_ratio = min(95, parent.split_ratio + layout.grow_amount)
                layout_all = True

            if layout_all:
                layout.group.layout_all()
                break

        child = parent
        parent = child.parent


@lazy.function
def resize_left(qtile):
    resize(qtile, "left")


@lazy.function
def resize_right(qtile):
    resize(qtile, "right")


@lazy.function
def resize_up(qtile):
    resize(qtile, "up")


@lazy.function
def resize_down(qtile):
    resize(qtile, "down")


keys = [
    ### The essentials
    Key([mod], "Return", lazy.spawn(terminal), desc="Launches My Terminal"),
    
    Key([mod, "control"], "r", lazy.restart(), desc="Restart Qtile"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
        Key([mod], "r", lazy.spawncmd(),
        desc="Spawn a command using a prompt widget"),
    Key(
        [mod],
        'Escape',
        lazy.spawn("./.config/rofi/launchers/colorful/launcher.sh"),
        # lazy.spawn("rofi -display-drun '' -show drun -drun-show-actions"),
        desc="Rofi app launcher",
    ),
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle through layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill active window"),
    Key(
        [mod, "shift"],
        "e",
        lazy.spawn("./.config/rofi/powermenu/powermenu.sh"),
        desc="Power Menu",
    ),
    Key(
        [mod, "shift"],
        "a",
        lazy.spawn("code /home/kikman/.config/qtile/config.py"),
        desc="Config qtile",
    ),
    ### Window controls
    Key(
        [mod], "Down", lazy.layout.down(), desc="Move focus down in current stack pane"
    ),
    Key([mod], "Up", lazy.layout.up(), desc="Move focus up in current stack pane"),
    Key(
        [mod],
        "Left",
        lazy.layout.left(),
        lazy.layout.next(),
        desc="Move focus left in current stack pane",
    ),
    Key(
        [mod],
        "Right",
        lazy.layout.right(),
        lazy.layout.previous(),
        desc="Move focus right in current stack pane",
    ),
    Key(
        [mod, "shift"],
        "Down",
        lazy.layout.shuffle_down(),
        desc="Move windows down in current stack",
    ),
    Key(
        [mod, "shift"],
        "Up",
        lazy.layout.shuffle_up(),
        desc="Move windows up in current stack",
    ),
    Key(
        [mod, "shift"],
        "Left",
        lazy.layout.shuffle_left(),
        lazy.layout.swap_left(),
        lazy.layout.client_to_previous(),
        desc="Move windows left in current stack",
    ),
    Key(
        [mod, "shift"],
        "Right",
        lazy.layout.shuffle_right(),
        lazy.layout.swap_right(),
        lazy.layout.client_to_next(),
        desc="Move windows right in the current stack",
    ),
    Key([mod, "control"], "Down", lazy.layout.flip_down(), desc="Flip layout down"),
    Key([mod, "control"], "Up", lazy.layout.flip_up(), desc="Flip layout up"),
    Key([mod, "control"], "Left", lazy.layout.flip_left(), desc="Flip layout left"),
    Key([mod, "control"], "Right", lazy.layout.flip_right(), desc="Flip layout right"),
    Key(
        [mod, "mod1"],
        "Left",
        resize_left,
        desc="Resize window left",
    ),
    Key(
        [mod, "mod1"],
        "Right",
        resize_right,
        desc="Resize window Right",
    ),
    Key([mod, "mod1"], "Up", resize_up, desc="Resize windows upward"),
    Key([mod, "mod1"], "Down", resize_down, desc="Resize windows downward"),
    Key([mod], "n", lazy.layout.normalize(), desc="Normalize window size ratios"),
    Key(
        [mod],
        "m",
        lazy.window.toggle_maximize(),
        desc="Toggle window between minimum and maximum sizes",
    ),
    Key([mod, "shift"], "f", lazy.window.toggle_fullscreen(), desc="Toggle fullscreen"),
    Key(
        [mod],
        "t",
        lazy.window.toggle_floating(),
        desc="Toggle floating on focused window",
    ),
    Key(
        [mod],
        "h",
        lazy.window.toggle_minimize(),
        desc="Toggle minimization on focused window",
    ),
    Key(
        [mod, "shift"],
        "h",
        lazy.group.unminimize_all(),
        desc="Unminimize all windows on current group",
    ),
    Key(
        [mod],
        "b",
        lazy.spawn("./.config/qtile/toggle_eww.sh"),
        desc="Toggle bottom eww bar visibility",
    ),
    Key(
        [mod, "mod1"],
        "space",
        lazy.spawn("./.config/sxhkd/old_scripts/rofi-task"),
        desc="Rofi taskwarrior",
    ),
    Key(
        [mod, "control"],
        "w",
        lazy.spawn("nc_flash_window"),
        desc="Flash currently focused window",
    ),
    Key(
        [mod],
        "space",
        lazy.spawn("./.config/sxhkd/old_scripts/rofi_notes.sh"),
        desc="Rofi quick notes",
    ),
    Key(
        [],
        "Print",
        lazy.spawn("./.config/sxhkd/prtscr"),
        desc="Print Screen",
    ),
    Key(
        [mod],
        "Print",
        lazy.spawn("./.config/sxhkd/prtregion -d"),
        desc="Print region of screen",
    ),
    Key(
        [mod, "shift"],
        "Print",
        lazy.spawn("./.config/sxhkd/prtregion -c"),
        desc="Print region of screen to clipboard",
    ),
    # Key(
    #    [mod],
    #    "F10",
    #    lazy.spawn("./.config/qtile/eww_bright.sh up"),
    #    desc="Increase brightness",
    # ),
    # Key(
    #    [mod],
    #    "F9",
    #    lazy.spawn("./.config/qtile/eww_bright.sh down"),
    #    desc="Decrease brightness",
    # ),
    Key(
        [],
        "XF86AudioRaiseVolume",
        lazy.spawn("./.config/qtile/eww_vol.sh up"),
        desc="Increase volume",
    ),
    Key(
        [],
        "XF86AudioLowerVolume",
        lazy.spawn("./.config/qtile/eww_vol.sh down"),
        desc="Decrease volume",
    ),
    Key(
        [],
        "XF86AudioMute",
        lazy.spawn("./.config/qtile/eww_vol.sh mute"),
        desc="Toggle mute",
    ),
    Key(
        [mod, "shift"],
        "p",
        lazy.spawn("./.config/sxhkd/togglepicom"),
        desc="Toggle picom",
    ),

    Key(
        [mod, "control"],
        "c",
        lazy.spawn("./.config/sxhkd/old_scripts/toggledunst"),
        desc="Toggle dunst",
    ),

    Key(
        [],
        "XF86Calculator",
        lazy.spawn("gnome-calculator"),
        desc="Launch calculator",
    ),
    Key(
        [mod],
        "z",
        lazy.spawn("firefox"),
        desc="Launch Firefox",
    ),
    Key(
        [mod],
        "x",
        lazy.spawn("code"),
        desc="Launch VsCode",
    ),
    Key(
        [mod],
        "c",
        lazy.spawn("nautilus"),
        desc="Launch Nautilus",
    ),
    Key(
        ["mod1"],
        "F4",
        lazy.spawn("./.config/rofi/bin/powermenu"),
        desc="Launch Nautilus",
    ),
    
]


def show_keys():
    key_help = ""
    for k in keys:
        mods = ""

        for m in k.modifiers:
            if m == "mod4":
                mods += "Super + "
            else:
                mods += m.capitalize() + " + "

        if len(k.key) > 1:
            mods += k.key.capitalize()
        else:
            mods += k.key

        key_help += "{:<30} {}".format(mods, k.desc + "\n")

    return key_help


keys.extend(
    [
        Key(
            [mod],
            "a",
            lazy.spawn(
                "sh -c 'echo \""
                + show_keys()
                + '" | rofi -dmenu -theme ~/.config/rofi/configTall.rasi -i -p "?"\''
            ),
            desc="Print keyboard bindings",
        ),
    ]
)

workspaces = [
    {"name": "", "key": "1", "matches": [Match(wm_class="firefox")]},
    {"name": "", "key": "2", "matches": [Match(wm_class="code")]},
    {
        "name": "",
        "key": "3",
        "matches": [
            Match(wm_class="joplin"),
            Match(wm_class="libreoffice"),
            Match(wm_class="org.pwmt.zathura"),
        ],
    },
    {
        "name": "",
        "key": "4",
        "matches": [
            Match(wm_class="Thunderbird"),
            Match(wm_class="com.github.jmoerman.go-for-it"),
            Match(wm_class="gnome-calendar"),
        ],
    },
    {"name": "", "key": "5", "matches": []},
    {
        "name": "",
        "key": "6",
        "matches": [
            Match(wm_class="slack"),
            Match(wm_class="lightcord"),
            Match(wm_class="polari"),
        ],
    },
    {"name": "", "key": "7", "matches": [Match(wm_class="spotify")]},
    {"name": "", "key": "8", "matches": [Match(wm_class="gimp")]},
    {"name": "", "key": "9", "matches": []},
    {
        "name": "",
        "key": "0",
        "matches": [
            Match(wm_class="lxappearance"),
            Match(wm_class="pavucontrol"),
            Match(wm_class="connman-gtk"),
        ],
    },
]

groups = [
    ScratchPad(
        "scratchpad",
        [
            # define a drop down terminal.
            # it is placed in the upper third of screen by default.
            DropDown(
                "term",
                "alacritty --class dropdown -e tmux_startup.sh",
                height=0.6,
                on_focus_lost_hide=False,
                opacity=1,
                warp_pointer=False,
            ),
        ],
    ),
]

for workspace in workspaces:
    matches = workspace["matches"] if "matches" in workspace else None
    groups.append(Group(workspace["name"], matches=matches, layout="bsp"))
    keys.append(
        Key(
            [mod],
            workspace["key"],
            lazy.group[workspace["name"]].toscreen(),
            desc="Focus this desktop",
        )
    )
    keys.append(
        Key(
            [mod, "shift"],
            workspace["key"],
            lazy.window.togroup(workspace["name"]),
            desc="Move focused window to another group",
        )
    )

# Define colors

colors = [
    ["#2e3440", "#2e3440"],  # background
    ["#d8dee9", "#d8dee9"],  # foreground
    ["#3b4252", "#3b4252"],  # background lighter
    ["#bf616a", "#bf616a"],  # red
    ["#a3be8c", "#a3be8c"],  # green
    ["#ebcb8b", "#ebcb8b"],  # yellow
    ["#81a1c1", "#81a1c1"],  # blue
    ["#b48ead", "#b48ead"],  # magenta
    ["#88c0d0", "#88c0d0"],  # cyan
    ["#e5e9f0", "#e5e9f0"],  # white
    ["#4c566a", "#4c566a"],  # grey
    ["#d08770", "#d08770"],  # orange
    ["#8fbcbb", "#8fbcbb"],  # super cyan
    ["#5e81ac", "#5e81ac"],  # super blue
    ["#242831", "#242831"],  # super dark background
    ["#06060b", "#06060b"],  # pure black
    ["#000000","#000000"], # transparent
]

layout_theme = {
    # "border_width": ,
    "margin": 5,
    "border_focus": "3b4252",
    "border_normal": "3b4252",
    "font": "FiraCode Nerd Font",
    "grow_amount": 2,
}

layouts = [
    # layout.MonadWide(**layout_theme),
    CustomBsp(**layout_theme, fair=False),
    # layout.MonadTall(**layout_theme),
    # layout.Max(**layout_theme),
    # layout.Tile(shift_windows=True, **layout_theme),
    # layout.Stack(num_stacks=2, **layout_theme),
    layout.Floating(**layout_theme, fullscreen_border_width=3, max_border_width=3),
]

# Define functions for bar
def taskwarrior():
    return (
        subprocess.check_output(["./.config/qtile/task_polybar.sh"])
        .decode("utf-8")
        .strip()
    )


### Mouse_callback functions
def open_launcher():
    qtile.cmd_spawn("./.config/rofi/launchers/colorful/launcher.sh")


def finish_task():
    qtile.cmd_spawn('task "$((`cat /tmp/tw_polybar_id`))" done')


def kill_window():
    qtile.cmd_spawn("xdotool getwindowfocus windowkill")


def update():
    qtile.cmd_spawn(terminal + "-e yay")


def open_pavu():
    qtile.cmd_spawn("pavucontrol")


def toggle_bluetooth():
    qtile.cmd_spawn("./.config/qtile/system-bluetooth-bluetoothctl.sh --toggle")


def open_bt_menu():
    qtile.cmd_spawn("blueberry")


def open_battery():
    qtile.cmd_spawn("./.config/rofi/bin/applet_battery")


def todays_date():
    qtile.cmd_spawn("./.config/qtile/calendar.sh")


def open_powermenu():
    qtile.cmd_spawn("./.config/rofi/powermenu/powermenu.sh")

# def launch_htop():
#     qtile.cmd_spawn("alacritty -e htop")
# Setup bar
widget_defaults = dict(
    font="FiraCode Bold", fontsize=14, padding = 0, background=colors[16], foreground=colors[9],
)
extension_defaults = widget_defaults.copy()

group_box_settings = {
    "padding": 5,
    "borderwidth": 1,
    "active": colors[9],
    "inactive": colors[15],
    "disable_drag": True,
    "rounded": True,
    "highlight_color": colors[9],
    "block_highlight_text_color": colors[9],
    # "highlight_method": "block",
    "this_current_screen_border": colors[9],
    "this_screen_border": colors[7],
    "other_current_screen_border": colors[14],
    "other_screen_border": colors[14],
    "foreground": colors[1],
    "background": colors[15],
    "urgent_border": colors[3],
}

screens = [
    Screen(
        # wallpaper="~/Pictures/dnord4k_dark.png",
        # wallpaper_mode="fill",
        top=bar.Bar(
            [
                widget.Prompt(),
                widget.TextBox(
                    text="cat",
                    foreground=colors[9],
                    font="Font Awesome 5 Free Solid",
                    fontsize=24,
                    padding=10,
                    mouse_callbacks={"Button1": open_launcher},
                ),
                widget.GroupBox(
                    font="Font Awesome 5 Brands",
                    visible_groups=[""],
                    **group_box_settings,
                ),
                widget.GroupBox(
                    font="Font Awesome 5 Free Solid",
                    visible_groups=["", "", "", "", ""],
                    **group_box_settings,
                ),
                widget.GroupBox(
                    font="Font Awesome 5 Brands",
                    visible_groups=[""],
                    **group_box_settings,
                ),
                widget.GroupBox(
                    font="Font Awesome 5 Free Solid",
                    visible_groups=["", "", ""],
                    **group_box_settings,
                ),
                widget.Spacer(),
                widget.TextBox(
                    text=" ",
                    font="Font Awesome 5 Free Solid",
                    # foreground=colors[4],  
                    # fontsize=14
                ),
                widget.Clock(
                    format="%I:%M %p",
                    fontsize= 14,
                    # foreground=colors[4],
                    mouse_callbacks={"Button1": todays_date},
                ),
                widget.Sep(
                    linewidth=1,
                    foreground=colors[9],
                    padding=10,
                    size_percent=40,
                ),
                widget.Clock(
                    format="%a,%b %d",
                ),
                widget.Spacer(),
                widget.Memory(
                    measure_mem = "G", 
                    format = '(:{MemUsed:.1f}{mm}/{MemTotal:.1f}{mm})',
                    # mouse_callbacks={"Button2": launch_htop},
                ),
                widget.CPU(format = '(:{freq_current}GHz/{load_percent}%)  '),
                # widget.BatteryIcon(theme_path = 'home/kikman/Rice/BatteryIcons/'),
                widget.Battery(
                    # foreground=colors[4],
                    charge_char = '',
                    discharge_char = '',
                    empty_char = '',
                    full_char = '',
                    low_foreground = colors[3],
                    show_short_text = False,
                    # font="Font Awesome 5 Free Solid",
                    format = '{char}{percent:2.0%}',
                    notify_below = 10,
                    mouse_callbacks={"Button3": open_battery},
                ),
                widget.Systray(icon_size=18, padding=10),
            ],
            28,
            opacity = 0
            # margin=[0, 0, 0, 0],
        ),
        # bottom=bar.Gap(18),
        # left=bar.Gap(18),
        # right=bar.Gap(18),
    ),
]

# Drag floating layouts.
mouse = [
    Drag(
        [mod],
        "Button1",
        lazy.window.set_position_floating(),
        start=lazy.window.get_position(),
    ),
    Drag(
        [mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()
    ),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
main = None  # WARNING: this is deprecated and will be removed soon
follow_mouse_focus = True
bring_front_click = "floating_only"
cursor_warp = False
floating_layout = layout.Floating(
    **layout_theme,
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        Match(wm_type="utility"),
        Match(wm_type="notification"),
        Match(wm_type="toolbar"),
        Match(wm_type="splash"),
        Match(wm_type="dialog"),
        Match(wm_class="confirm"),
        Match(wm_class="dialog"),
        Match(wm_class="download"),
        Match(wm_class="error"),
        Match(wm_class="file_progress"),
        Match(wm_class="notification"),
        Match(wm_class="splash"),
        Match(wm_class="toolbar"),
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(wm_class="pomotroid"),
        Match(wm_class="cmatrixterm"),
        Match(title="Farge"),
        Match(wm_class="org.gnome.Nautilus"),
        Match(wm_class="feh"),
        Match(wm_class="gnome-calculator"),
        Match(wm_class="blueberry"),
    ],
)
auto_fullscreen = True
focus_on_window_activation = "focus"

# Startup scripts
@hook.subscribe.startup_once
def start_once():
    home = os.path.expanduser("~")
    subprocess.call([home + "/.config/qtile/autostart.sh"])


# Window swallowing ;)
# @hook.subscribe.client_new
# def _swallow(window):
#     pid = window.window.get_net_wm_pid()
#     ppid = psutil.Process(pid).ppid()
#     cpids = {
#         c.window.get_net_wm_pid(): wid for wid, c in window.qtile.windows_map.items()
#     }
#     for i in range(5):
#         if not ppid:
#             return
#         if ppid in cpids:
#             parent = window.qtile.windows_map.get(cpids[ppid])
#             parent.minimized = True
#             window.parent = parent
#             return
#         ppid = psutil.Process(ppid).ppid()


@hook.subscribe.client_killed
def _unswallow(window):
    if hasattr(window, "parent"):
        window.parent.minimized = False


# Go to group when app opens on matched group
@hook.subscribe.client_new
def modify_window(client):
    # if (client.window.get_wm_transient_for() or client.window.get_wm_type() in floating_types):
    #    client.floating = True

    for group in groups:  # follow on auto-move
        match = next((m for m in group.matches if m.compare(client)), None)
        if match:
            targetgroup = client.qtile.groups_map[
                group.name
            ]  # there can be multiple instances of a group
            targetgroup.cmd_toscreen(toggle=False)
            break


# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "qtile"
