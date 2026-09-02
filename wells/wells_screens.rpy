################################################################################
##     ▼ SCREEN SAY PRINCIPAL (SISTEMA ADAPTATIVO DIRETOR DE SLOTS) ▼         ##
################################################################################
init 999 screen say(who, what, multiple=None):
    if persistent.wells_say_slot == 1:
        use wells_say_slot_1(who, what, multiple)
    elif persistent.wells_say_slot == 2:
        use wells_say_slot_2(who, what, multiple)
    elif persistent.wells_say_slot == 3:
        use wells_say_slot_3(who, what, multiple)
    elif persistent.wells_say_slot == 4:
        use wells_say_slot_4(who, what, multiple)
    elif persistent.wells_say_slot == 5:
        use wells_say_slot_5(who, what, multiple)
    elif persistent.wells_say_slot == 6:
        use wells_say_slot_6(who, what, multiple)
    else:
        window:
            id "window"
            if who is not None:
                window:
                    id "namebox"
                    style "namebox"
                    text who id "who"
            text what id "what"
        if not renpy.variant("small"):
            add SideImage() xalign 0.0 yalign 1.0
            use quick_menu()

################################################################################
##                    ▲ FIM DA SCREEN PRINCIPAL ▲                             ##
##============================================================================##
##                                                                            ##
##               ▼ (ARQUIVO DE SLOTS - CONTEÚDO COMPLETO) ▼                   ##
##                                                                            ##
##          Abaixo segue o sistema de slots para screen's say's               ##
##          Apartir do slot 1 ao 3 são screens fixas com travas               ##
##          de segurança que evitam traceback e textos invisiveis             ##
##          O slot 6 contém o layout com identidade visual                    ##
##          nativa do framework legado (estilos 1280 e 1920)                  ##
##                                                                            ##
################################################################################

# Variável persistente que controla qual tela está ativa (0 = Pass-Through Padrão)
default persistent.wells_say_slot = 0
# ===============================================================================
# SLOT 1: BEING A DIK
# ===============================================================================
screen wells_say_slot_1(who, what, multiple=None):
    style_prefix "say"

    window:
        # [BLINDAGEM EM LINHA ÚNICA] Faz a checagem direto no argumento para respeitar a sintaxe do Ren'Py
        background Transform(style.window.background, alpha=(persistent.say_window_alpha if (hasattr(persistent, 'say_window_alpha') and persistent.say_window_alpha is not None) else 1.0))
        id "window"
        if multiple and multiple > 0:
            yoffset (persistent.wells_dual_dialogue_offset * multiple)
        else:
            yoffset (persistent.wells_dialogue_y_offset if persistent.wells_dialogue_y_offset is not None else 0)

        if who is not None:

            window:
                id "namebox"
                style "namebox"
                text who id "who":
                    size (persistent.pref_text_size_label or 26) # Sua variável de tamanho de nome

        text what id "what":
            line_spacing (persistent.wells_line_spacing or 5)
            size (persistent.pref_text_size_dialogue or 28)
            if getattr(persistent, "wells_force_outline", False):
                outlines [(absolute(2), "#292929ff", 0, 0)]

    if not renpy.variant("small"):
        add SideImage() xalign 0.0 yalign 1.0
        use quick_menu()
# ===============================================================================
# SLOT 2: ETERNUM
# ===============================================================================
screen wells_say_slot_2(who, what, multiple=None):
    style_prefix "say"

    window:
        id "window"
        if multiple and multiple > 0:
            yoffset (persistent.wells_dual_dialogue_offset * multiple)
        else:
            yoffset (persistent.wells_dialogue_y_offset if persistent.wells_dialogue_y_offset is not None else 0)

        xsize (persistent.textbox_width + 274 if (hasattr(persistent, 'textbox_width') and persistent.textbox_width is not None) else 1080 + 274)
        ysize (persistent.textbox_height if (hasattr(persistent, 'textbox_height') and persistent.textbox_height is not None) else 185)
        
        if persistent.quick_menu:
            ypos 1080 - (persistent.textbox_height if (hasattr(persistent, 'textbox_height') and persistent.textbox_height is not None) else 185) - 32
        else:
            ypos 1080 - (persistent.textbox_height if (hasattr(persistent, 'textbox_height') and persistent.textbox_height is not None) else 185)

        background Frame(Transform("gui/textbox.png", alpha=(persistent.textbox_opacity if (hasattr(persistent, 'textbox_opacity') and persistent.textbox_opacity is not None) else 1.0)))

        vbox:
            xpos gui.name_xpos
            ypos 40
            xsize (persistent.textbox_width if (hasattr(persistent, 'textbox_width') and persistent.textbox_width is not None) else 1080)
            spacing 15

            if who is not None:
                window:
                    id "namebox"
                    style "namebox"
                    text who id "who":
                        size (persistent.pref_text_size_label or 26)

            text what id "what":
                size (persistent.pref_text_size_dialogue or (persistent.text_size if (hasattr(persistent, 'text_size') and persistent.text_size is not None) else 28))
                outlines [ (absolute(persistent.text_outline if (hasattr(persistent, 'text_outline') and persistent.text_outline is not None) else 2), "#000", absolute(0), absolute(0)) ]
                line_spacing (persistent.wells_line_spacing or 5) 

    if not renpy.variant("small"):
        add SideImage() xalign 0.0 yalign 1.0
        use quick_menu()
# ===============================================================================
# SLOT 3: PASS-THROUGH COM CONTORNO OPCIONAL
# ===============================================================================
screen wells_say_slot_3(who, what, multiple=None):
    window:
        id "window"
        if who is not None:
            window:
                id "namebox"
                style "namebox"
                text who id "who":
                    if getattr(persistent, "wells_force_outline", False):
                        outlines [(absolute(2), "#292929ff", 0, 0)]

        text what id "what":
            size (persistent.pref_text_size_dialogue or 28)
            if getattr(persistent, "wells_force_outline", False):
                outlines [(absolute(2), "#292929ff", 0, 0)]

    if not renpy.variant("small"):
        add SideImage() xalign 0.0 yalign 1.0
        use quick_menu()


# ===============================================================================
# SLOT 4: EM BRANCO (ESPAÇO RESERVADO)
# ===============================================================================
screen wells_say_slot_4(who, what, multiple=None):
    pass



# ===============================================================================
# SLOT 5: EM BRANCO (ESPAÇO RESERVADO)
# ===============================================================================
screen wells_say_slot_5(who, what, multiple=None):
    pass


# ===============================================================================
# SLOT 6: LAYOUT NATIVO LEGADO DO FRAMEWORK (SISTEMA INTEGRADO)
# ===============================================================================
screen wells_say_slot_6(who, what, multiple=None):
    if config.screen_width == 1280:
        style_prefix "say_wells_1280"
    if config.screen_width == 1920:
        style_prefix "say_wells_1920"

    if persistent.wells_say_mode == 0:
        if persistent.wells_dual_dialogue_fix:
            window:
                id "window"
                if multiple and multiple > 0:
                    yoffset (persistent.wells_dual_dialogue_offset * multiple)
                else:
                    yoffset (persistent.wells_dialogue_y_offset if persistent.wells_dialogue_y_offset is not None else 0)

                if config.screen_width == 1280:
                    style "say_wells_1280"
                if config.screen_width == 1920:
                    style "say_wells_1920"

                if who is not None:
                    window:
                        if config.screen_width == 1280:
                            style "namebox_wells_1280"
                        if config.screen_width == 1920:
                            style "namebox_wells_1920"
                        text who id "who":
                            size (persistent.pref_text_size_label or 26)
                            if getattr(persistent, "wells_force_outline", False):
                                outlines [(absolute(2), "#292929ff", 0, 0)]

                text what id "what":
                    if config.screen_width == 1920:
                        ypos -56
                        xpos (355 if who else 0.2)
                        xsize 980
                        line_spacing (persistent.wells_line_spacing or 5)
                        size (persistent.pref_text_size_dialogue or 26)
                        color "#FFFFFF"
                        if getattr(persistent, "wells_force_outline", False):
                            outlines [(absolute(2), "#292929ff", 0, 0)]
        else:
            window:
                if multiple and multiple > 0:
                    yoffset (persistent.wells_dual_dialogue_offset * multiple)
                else:
                    yoffset (persistent.wells_dialogue_y_offset if persistent.wells_dialogue_y_offset is not None else 0)

                if config.screen_width == 1280:
                    style "say_wells_1280"
                if config.screen_width == 1920:
                    style "say_wells_1920"

                if who is not None:
                    window:
                        if config.screen_width == 1280:
                            style "namebox_wells_1280"
                        if config.screen_width == 1920:
                            style "namebox_wells_1920"
                        text who id "who":
                            size (persistent.pref_text_size_label or 26)
                            if getattr(persistent, "wells_force_outline", False):
                                outlines [(absolute(2), "#292929ff", 0, 0)]

                text what id "what":
                    if config.screen_width == 1920:
                        ypos -56
                        xpos (355 if who else 0.2)
                        xsize 980
                        line_spacing (persistent.wells_line_spacing or 5)
                        size (persistent.pref_text_size_dialogue or 26)
                        color "#FFFFFF"
                        if getattr(persistent, "wells_force_outline", False):
                            outlines [(absolute(2), "#292929ff", 0, 0)]

    elif persistent.wells_say_mode == 1:
        style_prefix "say"
        window:
            id "window"
            if multiple and multiple > 0:
                yoffset (persistent.wells_dual_dialogue_offset * multiple)
            else:
                yoffset (persistent.wells_dialogue_y_offset if persistent.wells_dialogue_y_offset is not None else 0)

            if who is not None:
                window:
                    id "namebox"
                    style "namebox"
                    text who id "who":
                        size (persistent.pref_text_size_label or 26)

            text what id "what":
                line_spacing (persistent.wells_line_spacing or 5)
                size (persistent.pref_text_size_dialogue or 26)
                color "#FFFFFF"
                outlines [(absolute(2), "#292929ff", 0, 0)]

    if not renpy.variant("small"):
        add SideImage() xalign 0.0 yalign 1.0
        use quick_menu()

################################################################################
##      ▼ SISTEMA INTELIGENTE DE DIÁLOGOS MÚLTIPLOS (WELLS FRAMEWORK) ▼       ##
##============================================================================##
##                                                                            ##
##               (NOVO ARQUIVO DE SLOTS - CONTEÚDO COMPLETO)                  ##
##                                                                            ##
##        Abaixo segue o sistema de slots para screen multiple say            ##
##          a screen multiple say  é responsavel por controlar                ##
##         dialogos  multiplos sempre que 2 ou mais personagens               ##
##       falam ao mesmo tempo, então essa area é dedicada a ajustar           ##
##      o posicionamento destes dialogos bem como o tamanho eo frame,         ##
##      o procedimento para ajustar é igual ao da screen say normal,          ##
##      porém um pouco mais delicado e fino, então cuidado ao editar.         ##
##                                                                            ##
################################################################################

screen multiple_say(who, what, multiple):
    style_prefix "say"

    # 1. [BLINDAGEM DA TUPLA] Extrai o número puro (int) de diálogos de forma ultra segura
    $ num_multiplo = multiple[0] if (isinstance(multiple, (tuple, list)) and len(multiple) > 0) else (int(multiple) if multiple is not None else 1)

    # 2. [CÁLCULO ISOLADO DO ETERNUM] Faz a matemática em linhas Python protegidas para evitar o erro de float/tuple
    $ wells_et_height = persistent.textbox_height if (hasattr(persistent, 'textbox_height') and persistent.textbox_height is not None) else 185
    $ wells_et_opacity = persistent.textbox_opacity if (hasattr(persistent, 'textbox_opacity') and persistent.textbox_opacity is not None) else 1.0

    if persistent.quick_menu:
        $ wells_et_ypos = 1080 - (wells_et_height * num_multiplo) - 32
    else:
        $ wells_et_ypos = 1080 - (wells_et_height * num_multiplo)

    if persistent.wells_multiple_slot == 0:
        window:
            id "window"
            if num_multiplo and num_multiplo > 0:
                yoffset (persistent.wells_dual_dialogue_offset * num_multiplo)
            else:
                yoffset (persistent.wells_dialogue_y_offset if persistent.wells_dialogue_y_offset is not None else 0)

            if config.screen_width == 1280:
                style "say_wells_1280"
            if config.screen_width == 1920:
                style "say_wells_1920"

            vbox:
                xpos gui.name_xpos
                ypos -250 # O SEU VALOR NEGATIVO CIRÚRGICO QUE SALVA O ALINHAMENTO
                xsize (1316 if config.screen_width == 1920 else 900)
                spacing 15

                if who is not None:
                    window:
                        if config.screen_width == 1280:
                            style "namebox_wells_1280"
                        if config.screen_width == 1920:
                            style "namebox_wells_1920"
                        text who id "who":
                            size (persistent.pref_text_size_label or 26)
                            if getattr(persistent, "wells_force_outline", False):
                                outlines [(absolute(2), "#292929ff", 0, 0)]

                text what id "what":
                    line_spacing (persistent.wells_line_spacing or 5)
                    size (persistent.pref_text_size_dialogue or 28)
                    if getattr(persistent, "wells_force_outline", False):
                        outlines [(absolute(2), "#292929ff", 0, 0)]

        if not renpy.variant("small"):
            add SideImage() xalign 0.0 yalign 1.0
            use quick_menu()

    elif persistent.wells_multiple_slot == 2:
        window:
            id "window"
            ypos wells_et_ypos
            xsize (persistent.textbox_width + 274 if (hasattr(persistent, 'textbox_width') and persistent.textbox_width is not None) else 1080 + 274)
            ysize wells_et_height
            background Frame(Transform("wells/gui/textbox1920.png", alpha=wells_et_opacity))

            vbox:
                xpos gui.name_xpos
                ypos 40
                xsize (persistent.textbox_width if (hasattr(persistent, 'textbox_width') and persistent.textbox_width is not None) else 1080)
                spacing 15

                if who is not None:
                    window:
                        id "namebox"
                        style "namebox"
                        text who id "who"

                text what id "what":
                    size (persistent.text_size if (hasattr(persistent, 'text_size') and persistent.text_size is not None) else 28)
                    outlines [ (absolute(persistent.text_outline if (hasattr(persistent, 'text_outline') and persistent.text_outline is not None) else 2), "#000", absolute(0), absolute(0)) ]

        if not renpy.variant("small"):
            add SideImage() xalign 0.0 yalign 1.0
            use quick_menu()

    elif persistent.wells_multiple_slot == 3:
        window:
            id "window"
            ypos wells_et_ypos
            xsize (persistent.textbox_width + 274 if (hasattr(persistent, 'textbox_width') and persistent.textbox_width is not None) else 1080 + 274)
            ysize wells_et_height
            background Frame(Transform("wells/gui/textbox1920.png", alpha=wells_et_opacity))

            vbox:
                xpos gui.name_xpos
                ypos -250
                xsize (persistent.textbox_width if (hasattr(persistent, 'textbox_width') and persistent.textbox_width is not None) else 1080)
                spacing 15

                if who is not None:
                    window:
                        id "namebox"
                        style "namebox"
                        text who id "who"

                text what id "what":
                    size (persistent.text_size if (hasattr(persistent, 'text_size') and persistent.text_size is not None) else 28)
                    outlines [ (absolute(persistent.text_outline if (hasattr(persistent, 'text_outline') and persistent.text_outline is not None) else 2), "#000", absolute(0), absolute(0)) ]

        if not renpy.variant("small"):
            add SideImage() xalign 0.0 yalign 1.0
            use quick_menu()

    elif persistent.wells_multiple_slot == 4:
        window:
            id "window"
            style "default"
            xanchor 0.0
            xpos 80
            ypos wells_et_ypos 

            if num_multiplo == 1:
                frame:
                    background Image("wells/gui/textbox_multiple_frame.png", alpha=wells_et_opacity)
                    xsize 560      
                    ysize 270      
                    ypos 15
                    padding (30, 25)

                    vbox:
                        spacing 5
                        if who is not None:
                            window:
                                id "namebox"
                                style "namebox_multiple_wells_1920"
                                background Frame("wells/gui/namebox_multiple.png", 3, 3)
                                text who id "who":
                                    size (persistent.pref_text_size_label or 22)

                        text what id "what":
                            xsize 500 
                            size (persistent.wells_multiple_text_size if (hasattr(persistent, 'wells_multiple_text_size') and persistent.wells_multiple_text_size is not None) else 23)
                            outlines [ (absolute(persistent.text_outline if (hasattr(persistent, 'text_outline') and persistent.text_outline is not None) else 2), "#000", absolute(0), absolute(0)) ]
            else:
                frame:
                    background Image("wells/gui/textbox_multiple_frame.png", alpha=wells_et_opacity)
                    xsize 560      
                    ysize 270      
                    ypos -80
                    padding (30, 25)

                    vbox:
                        spacing 5
                        if who is not None:
                            window:
                                id "namebox"
                                style "namebox_multiple_wells_1920"
                                background Frame("wells/gui/namebox_multiple.png", 3, 3)
                                text who id "who":
                                    size (persistent.pref_text_size_label or 22)

                        text what id "what":
                            xsize 500 
                            size (persistent.wells_multiple_text_size if (hasattr(persistent, 'wells_multiple_text_size') and persistent.wells_multiple_text_size is not None) else 23)
                            outlines [ (absolute(persistent.text_outline if (hasattr(persistent, 'text_outline') and persistent.text_outline is not None) else 2), "#000", absolute(0), absolute(0)) ]

        if not renpy.variant("small"):
            add SideImage() xalign 0.0 yalign 1.0
            use quick_menu()

    elif persistent.wells_multiple_slot == 5:
        window:
            id "window"
            style "say_multiple_wells_1920"
            ypos 1260
            yoffset (40 if num_multiplo == 1 else 80)
            xsize (persistent.textbox_width + 274 if (hasattr(persistent, 'textbox_width') and persistent.textbox_width is not None) else 1080 + 274)
            ysize wells_et_height
            background Image("wells/gui/textbox_multiple_frame.png", alpha=wells_et_opacity, xalign=0.5, yalign=0.5)

            frame:
                padding (15, 2)
                vbox:
                    xpos gui.name_xpos
                    ypos -25
                    xysize (480, 65)
                    spacing 2

                    if who is not None:
                        window:
                            id "namebox"
                            style "namebox_multiple_wells_1920"
                            background Frame("wells/gui/namebox_multiple.png", 5, 5)
                            text who id "who"

                    text what id "what":
                        if config.screen_width == 1920:
                            ypos -85
                            xpos (255 if who else 0.2)
                            xsize 1316
                        size (persistent.wells_multiple_text_size if (hasattr(persistent, 'wells_multiple_text_size') and persistent.wells_multiple_text_size is not None) else 23)
                        outlines [ (absolute(persistent.text_outline if (hasattr(persistent, 'text_outline') and persistent.text_outline is not None) else 2), "#000", absolute(0), absolute(0)) ]

        if not renpy.variant("small"):
            add SideImage() xalign 0.0 yalign 1.0
            use quick_menu()

    elif persistent.wells_multiple_slot == 6:
        window:
            id "window"
            style "default"
            xanchor 0.0
            xpos 80
            ypos 680

            if num_multiplo == 1:
                frame:
                    background Image("wells/gui/textbox_multiple_frame.png", alpha=wells_et_opacity, xalign=0.5, yalign=0.5)
                    xsize 600
                    ysize 290
                    ypos 350
                    xpos 0
                    xanchor 0.0 yanchor 0.0
                    padding (55, 5)

                    vbox:
                        xpos -380
                        ypos 10
                        spacing 1
                        if who is not None:
                            window:
                                id "namebox"
                                style "namebox_multiple_wells_1920"
                                background Frame("wells/gui/namebox_multiple.png", 3, 3)
                                text who id "who":
                                    size (persistent.pref_text_size_label or 26)

                        text what id "what":
                            xsize 500 
                            size (persistent.wells_multiple_text_size if (hasattr(persistent, 'wells_multiple_text_size') and persistent.wells_multiple_text_size is not None) else 23)
                            outlines [ (absolute(persistent.text_outline if (hasattr(persistent, 'text_outline') and persistent.text_outline is not None) else 2), "#000", absolute(0), absolute(0)) ]
            else:
                frame:
                    background Image("wells/gui/textbox_multiple_frame.png", alpha=wells_et_opacity)
                    xsize 600
                    ysize 290
                    ypos -220
                    xpos 10
                    padding (15, 35)

                    vbox:
                        xpos -365
                        ypos -20
                        spacing 1
                        if who is not None:
                            window:
                                id "namebox"
                                style "namebox_multiple_wells_1920"
                                background Frame("wells/gui/namebox_multiple.png", 3, 3)
                                text who id "who":
                                    size (persistent.pref_text_size_label or 26)

                        text what id "what":
                            xsize 500 
                            size (persistent.wells_multiple_text_size if (hasattr(persistent, 'wells_multiple_text_size') and persistent.wells_multiple_text_size is not None) else 23)
                            outlines [ (absolute(persistent.text_outline if (hasattr(persistent, 'text_outline') and persistent.text_outline is not None) else 2), "#000", absolute(0), absolute(0)) ]

        if not renpy.variant("small"):
            add SideImage() xalign 0.0 yalign 1.0
            use quick_menu()

    else:
        pass
