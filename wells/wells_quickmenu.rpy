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
        hbox:
            spacing 2
            xalign 0.5 ypos 5

            imagebutton:
                xysize (100, 40)
                idle "wells/gui/imgbutton/gatilho_idle.png"
                hover "wells/gui/imgbutton/gatilho-hover.png"
                action [Show("quick_menu2"), Hide("quick_menu1")]
                alt "Abrir Atalhos"

            imagebutton:
                xysize (100, 40)
                idle "wells/gui/imgbutton/rollback_idle.png"
                hover "wells/gui/imgbutton/rollback_hover.png"
                action Rollback()
                alt "Rollback"

            imagebutton:
                xysize (100, 40)
                idle "wells/gui/imgbutton/skip_idle.png"
                hover "wells/gui/imgbutton/skip_hover.png"
                action Skip()
                alternate Skip(fast=True, confirm=True)
                alt "Skip"

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
                xalign 0.5
                idle "wells/gui/imgbutton/save_idle.png"
                hover "wells/gui/imgbutton/save_hover.png"
                action [Show("wells_custom_save"), Hide("quick_menu2")]
                alt "Save"

            imagebutton:
                xysize (120, 40)
                xalign 0.5
                idle "wells/gui/imgbutton/load_idle.png"
                hover "wells/gui/imgbutton/load_hover.png"
                action [Show("wells_custom_load"), Hide("quick_menu2")]
                alt "Load"

            imagebutton:
                xysize (120, 40)
                xalign 0.5
                idle "wells/gui/imgbutton/config_idle.png"
                hover "wells/gui/imgbutton/config_hover.png"
                action ShowMenu("preferences")
                alt "Configs"

            imagebutton:
                xysize (120, 40)
                xalign 0.5
                idle "wells/gui/imgbutton/wells_idle.png"
                hover "wells/gui/imgbutton/wells_hover.png"
                action [Show("wells_menu_language"), Hide("quick_menu2")]
                alt "Wells menu"
