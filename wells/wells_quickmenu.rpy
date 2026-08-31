################################################################################
## wells_quickmenu.rpy
################################################################################

init 999 python:
    if "quick_menu1" not in config.overlay_screens:
        config.overlay_screens.append("quick_menu1")

screen quick_menu():
    variant ("small", "medium", "large")
    tag quick_menu
    pass

screen quick_menu1():
    zorder 198
    modal False
    if quick_menu:
        imagebutton:
            xalign 0.5 ypos 0
            xysize (120, 40)
            idle "wells/gui/gatilho_idle.png"
            hover "wells/gui/gatilho-hover.png"
            action Show("quick_menu2")
            alt "Abrir Atalhos"
screen quick_menu2():
    zorder 199
    modal False

    button:
        action Hide("quick_menu2")
        background None
        xsize 1.0 ysize 1.0

    frame:
        xalign 0.5 ypos 0
        background Frame("wells/gui/base_nova.png", 3, 3)
        padding (14, 8, 12, 8)

        hbox:
            spacing 10
            yalign 0.5

            imagebutton:
                xysize (120, 40)
                idle "wells/gui/imgbutton/menu_idle.png"
                hover "wells/gui/imgbutton/menu_hover.png"
                action [Show("quick_menu3"), Hide("quick_menu2")]
                alt "Menu"

            imagebutton:
                xysize (120, 40)
                idle "wells/gui/imgbutton/rollback_idle.png"
                hover "wells/gui/imgbutton/rollback_hover.png"
                action [Rollback(), Hide("quick_menu2")]
                alt "Rollback"

            imagebutton:
                xysize (120, 40)
                idle "wells/gui/imgbutton/skip_idle.png"
                hover "wells/gui/imgbutton/skip_hover.png"
                action [Skip(), Hide("quick_menu2")]
                alternate Skip(fast=True, confirm=True)
                alt "Skip"
screen quick_menu3():
    zorder 199
    modal False

    frame:
        style "empty"
        background Solid("#00000060")
        xsize 1.0 ysize 1.0

        button:
            action Hide("quick_menu3")
            background None
            xsize 1.0 ysize 1.0

    frame:
        xalign 0.5 yalign 0.5
        style "empty"
        background Frame("wells/gui/quickbox.png", 20, 20)
        xsize 340 ysize 600
        padding (35, 45, 35, 5)

        vbox:
            spacing 24
            xalign 0.5 yalign 0.5

            imagebutton:
                xysize (180, 34)
                xalign 0.5
                idle "wells/gui/imgbutton/close_idle.png"
                hover "wells/gui/imgbutton/close_hover.png"
                action Hide("quick_menu3")
                alt "Close"

            imagebutton:
                xysize (180, 34)
                xalign 0.5
                idle "wells/gui/imgbutton/save_idle.png"
                hover "wells/gui/imgbutton/save_hover.png"
                action [Show("wells_custom_save"), Hide("quick_menu3")]
                alt "Save"

            imagebutton:
                xysize (180, 34)
                xalign 0.5
                idle "wells/gui/imgbutton/load_idle.png"
                hover "wells/gui/imgbutton/load_hover.png"
                action [Show("wells_custom_load"), Hide("quick_menu3")]
                alt "Load"

            imagebutton:
                xysize (180, 34)
                xalign 0.5
                idle "wells/gui/imgbutton/config_idle.png"
                hover "wells/gui/imgbutton/config_hover.png"
                action [Show("preferences"), Hide("quick_menu3")]
                alt "Configs"

            imagebutton:
                xysize (180, 34)
                xalign 0.5
                idle "wells/gui/imgbutton/wells_idle.png"
                hover "wells/gui/imgbutton/wells_hover.png"
                action [Show("wells_menu_language"), Hide("quick_menu3")]
                alt "Wells menu"

            imagebutton:
                xysize (180, 34)
                xalign 0.5
                idle "wells/gui/imgbutton/main_idle.png"
                hover "wells/gui/imgbutton/main_hover.png"
                action MainMenu()
                alt "Main menu"
