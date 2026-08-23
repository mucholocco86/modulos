################################################################################
## DEVELOPER CONFIG
################################################################################
init 999 python:
    config.language = "brazil"
    config.default_language = "brazil"
    config.developer = True
    config.console = True
    config.hard_rollback_limit = 128
    config.rollback_length = 128

################################################################################
## 1. DEFINIÇÃO DINÂMICA DAS FONTES E ESTILOS GERAIS
################################################################################

define 999 gui.text_font = 'wells/fonts/Roboto-Regular.ttf'
define 999 gui.name_text_font = 'wells/fonts/Roboto-Regular.ttf'
define 999 gui.interface_text_font = 'wells/fonts/Roboto-Regular.ttf'
define wells_namebox_borders = Borders(5, 5, 5, 5)
define wells_text_size = 30

default persistent.pref_text_size_label = 28
default persistent.pref_text_size_dialogue = 28
default wells_menu_tab = "main"
default persistent.font_escolhida = None
default persistent.wells_line_spacing = 5
default persistent.wells_text_size_mult = 1.0 
default persistent.wells_dialogue_y_offset = 0
default persistent.wells_dual_dialogue_offset = 200 
default persistent.wells_dual_dialog_offset = 300
default persistent.wells_dual_dialogue_fix = False
default persistent.wells_say_mode = 0
default persistent.wells_multiple_slot = 0
default persistent.wells_multiple_text_size = 23

################################################################################
## NATIVE PYTHON LOGIC
################################################################################
init python:
    config.gestures = { 
        "n"   : "game_menu",        # n   = Deslizar para CIMA (Abre o Menu do Jogo)
        "s"   : "hide_windows",     # s   = Deslizar para BAIXO (Esconde a Interface de Diálogos)
        "w"   : "rollback",         # w   = Deslizar para a ESQUERDA (Retorna o Texto/Diálogo Anterior)
        "e"   : "skip",             # e   = Deslizar para a DIREITA (Ativa o Avanço Rápido/Skip)
        "n_s" : "toggle_afm",       # n_s = Deslizar para CIMA e para BAIXO (Liga/Desliga Avanço Automático)
        "n_w" : "wells_toggle_qm"   # n_w = Deslizar para CIMA e para a ESQUERDA (Gesto de L Invertido)
    }

    import os

    def toggle_power_save():
        if preferences.gl_framerate == 30:
            preferences.gl_framerate = None
        else:
            preferences.gl_framerate = 30
        renpy.restart_interaction()

    def get_all_languages():
        languages = ["Default"]
        path = os.path.join(renpy.config.gamedir, 'tl')
        if os.path.exists(path):
            for entry in os.listdir(path):
                if os.path.isdir(os.path.join(path, entry)):
                    languages.append(entry)
        return languages

    def toggle_multiple_dialogue():
        persistent.multiple_dialogue = not persistent.multiple_dialogue
        renpy.restart_interaction()

    def listar_fontes():
        fontes = []
        path = os.path.join(renpy.config.gamedir, 'wells/fonts')
        if os.path.exists(path):
            for f in os.listdir(path):
                if f.lower().endswith((".ttf", ".otf")):
                    fontes.append(f)
        return fontes

    def wells_font_transformer(old_font):
        if persistent.font_escolhida:
            return persistent.font_escolhida
        return old_font

    config.font_transforms["wells_custom"] = wells_font_transformer
    config.overlay_screens.append("quick_menu")

    if renpy.variant("touch"):
        style.wells_menu_quick_button_text.size = 40
        style.wells_menu_quick_frame.padding = (30, 20)
    else:
        style.wells_menu_quick_button_text.size = 25

init -1 python:
    if persistent.use_hw_video is None:
        persistent.use_hw_video = True
    config.hw_video = persistent.use_hw_video

    if persistent.multiple_dialogue is None:
        persistent.multiple_dialogue = True

    if persistent.font_escolhida:
        _preferences.font_transform = "wells_custom"
