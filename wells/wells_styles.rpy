################################################################################
## MODULE: wells_styles.rpy
################################################################################

init -1 style wells_menu_slider_label is pref_label
init -1 style wells_menu_slider_label_text is label_text
init -1 style wells_menu_slider_slider is gui_slider
init -1 style wells_menu_slider_button is gui_button
init -1 style wells_menu_slider_button_text is gui_button_text
init -1 style wells_menu_slider_pref_vbox is pref_vbox
init -1 style wells_menu_check_button_text is button_text
init -1 style wells_menu_radio_button_text is button_text

init -1 style say_wells_1280_window is default
init -1 style say_wells_1280_label is default
init -1 style say_wells_1280_dialogue is default
init -1 style say_wells_1280_thought is say_wells_1280_dialogue
init -1 style namebox_wells_1280 is default
init -1 style namebox_wells_1280_label is say_wells_1280_label

# --- Definições de Estilos Visuais ---
init -1 style wells_menu_quick_button:
    padding (10, 4, 10, 4)

init -1 style wells_menu_quick_button_text:
    size 22
    color "#FFFFFF"
    outlines [(1, "#000000", 0, 0)]
    hover_color "#2bff00"

init -1 style wells_menu_quick_text is wells_menu_quick_button_text:
    size 22

if not renpy.variant("small"):
    init -1 style wells_menu_slider_label_text:
        size 28
    init -1 style wells_menu_check_button_text:
        size 28
    init -1 style wells_menu_radio_button_text:
        size 28
    init -1 style wells_menu_slider_slider:
        xsize 400
    init -1 style wells_menu_slider_button:
        yalign 0.5
        left_margin 15
    init -1 style wells_menu_slider_button_text:
        size 18
        font "fonts/Roboto-Regular.ttf"
    init -1 style wells_menu_slider_vbox:
        xsize 675

init -1 style say_wells_1280:
    xalign 0.5
    xfill True
    yalign 1.0
    ysize 195
    background Image("wells/gui/textbox1280.png", xalign=0.5, yalign=1.0)

init -1 style namebox_wells_1280:
    xpos 240
    xanchor 0.5
    xsize None
    ypos 0
    ysize None
    background Frame("wells/gui/namebox1280.png", wells_namebox_borders, tile=False, xalign=0.0)
    padding wells_namebox_borders.padding

init -1 style say_wells_1280_label:
    outlines [ (absolute(2), "#000000", absolute(0), absolute(10)) ]
    xalign 0.0
    yalign 1.5

init -1 style say_wells_1280_dialogue:
    outlines [ (absolute(5), "#000000", absolute(0), absolute(0)) ]
    xpos 268
    xsize 1100
    ypos 50

# --- SEÇÃO 1920 ---
init -1 style say_wells_1920_window is default
init -1 style say_wells_1920_label is default
init -1 style say_wells_1920_dialogue is default
init -1 style say_wells_1920_thought is say_wells_1920_dialogue
init -1 style namebox_wells_1920 is default
init -1 style namebox_wells_1920_label is say_wells_1920_label

init -1 style say_wells_1920:
    xalign 0.5
    xfill True
    yalign 1.0
    ysize 195
    background Image("wells/gui/textbox1920.png", xalign=0.5, yalign=1.0)

init -1 style namebox_wells_1920:
    xpos 355
    xsize None
    ypos -105
    ysize None
    background Frame("wells/gui/namebox1920.png", wells_namebox_borders, tile=False, xalign=0.0)
    padding wells_namebox_borders.padding

init -1 style say_wells_1920_label:
    outlines [ (absolute(2), "#000000", absolute(0), absolute(0)) ]
    xalign 0.5
    yalign 1.5

init -1 style say_wells_1920_dialogue:
    outlines [ (absolute(5), "#000000", absolute(0), absolute(0)) ]
    xpos 268
    xsize 1100
    ypos 50

init -1 style say_multiple_wells_1920 is multiple_say_window:
    xalign 0.5
    xfill True
    yalign 1.0
    ysize 195
    # Força de forma absoluta a sua nova imagem do Photoshop como fundo da caixa mãe
    background Image("wells/gui/textbox_multiple_frame.png", xalign=0.5, yalign=1.0)

init -1 style namebox_multiple_wells_1920:
    xpos 400
    xanchor 0.5
    xsize None
    ypos -80
    ysize None
    # Força a sua nova namebox personalizada
    background Frame("wells/gui/namebox_multiple.png", wells_namebox_borders, tile=False, xalign=0.0)
    padding wells_namebox_borders.padding

init -1 style game_menu_outer_frame:
    bottom_padding 30
    top_padding 120
    background Image("wells/gui/frame.png")

init -501 screen input(prompt):
    style_prefix "input"
    window:
        if renpy.variant("small"):
            yalign 0.2
        text prompt style "input_prompt"
        input id "input"

init -1 style input_prompt is default
