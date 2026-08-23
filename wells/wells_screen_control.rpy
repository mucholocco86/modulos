################################################################################
## 4. SCREEN DE DIALOGOS
################################################################################
screen dialogue_adjusts():
    modal True
    zorder 200
    tag menu
    add Solid("#00000080") 

    frame:
        xalign 0.5 yalign 0.4
        background Frame("wells/gui/frame_menu.png", 10, 10)

        if config.screen_width == 1920:
            if renpy.variant("small"):
                xsize 1600 ysize 950 padding (60, 50)
            else:
                xsize 1450 ysize 820 padding (50, 40)
        else:
            xsize 1150 ysize 680 padding (40, 35)

        vbox:
            xfill True
            spacing 25

            frame:
                xpos 670
                xanchor 0.5
                ypos 15
                background Frame("wells/gui/label_frame.png", 0, 0)
                padding (10, 10)
                label _("DIALOGUE MENU"):
                        text_size 48 
                        text_color "#ff4444"
        hbox:
            xalign 0.5
            yalign 0.45          
            spacing 60           

            hbox:
                spacing 40 
                yalign 0.0

                vbox:
                    spacing 12   
                    yalign 0.0

                    vbox spacing 4:
                        label _("Tam. Nome: [persistent.pref_text_size_label]"):
                            text_size 26
                            text_color "#2cf1ff"
                            padding (15, 2)
                            background Frame("wells/gui/label_frame.png", 10, 10)
                        bar:
                            value FieldValue(persistent, 'pref_text_size_label', range=60, step=2) 
                            xsize 380 ysize 25
                            idle_right_bar Frame("wells/gui/barra_vazia.png", 5, 5)
                            hover_right_bar Frame("wells/gui/barra_vazia.png", 5, 5)
                            idle_left_bar Frame("wells/gui/barra_cheia.png", 5, 5)
                            hover_left_bar Frame("wells/gui/barra_cheia.png", 5, 5)
                            thumb "wells/gui/pino.png"
                            thumb_shadow None
                            thumb_offset 1

                    vbox spacing 4:
                        label _("Tam. Diálogo: [persistent.pref_text_size_dialogue]"):
                            text_size 26
                            text_color "#2cf1ff"
                            padding (15, 2)
                            background Frame("wells/gui/label_frame.png", 10, 10)
                        bar:
                            value FieldValue(persistent, 'pref_text_size_dialogue', range=60, step=2) 
                            xsize 380 ysize 25
                            idle_right_bar Frame("wells/gui/barra_vazia.png", 5, 5)
                            hover_right_bar Frame("wells/gui/barra_vazia.png", 5, 5)
                            idle_left_bar Frame("wells/gui/barra_cheia.png", 5, 5)
                            hover_left_bar Frame("wells/gui/barra_cheia.png", 5, 5)
                            thumb "wells/gui/pino.png"
                            thumb_shadow None
                            thumb_offset 1

                    vbox spacing 4:
                        label _("Tam. Diálogo Multiple: [persistent.wells_multiple_text_size]"):
                            text_size 26
                            text_color "#2cf1ff"
                            padding (15, 2)
                            background Frame("wells/gui/label_frame.png", 10, 10)
                        bar:
                            value FieldValue(persistent, 'wells_multiple_text_size', range=30, step=2) 
                            xsize 380 ysize 25
                            idle_right_bar Frame("wells/gui/barra_vazia.png", 5, 5)
                            hover_right_bar Frame("wells/gui/barra_vazia.png", 5, 5)
                            idle_left_bar Frame("wells/gui/barra_cheia.png", 5, 5)
                            hover_left_bar Frame("wells/gui/barra_cheia.png", 5, 5)
                            thumb "wells/gui/pino.png"
                            thumb_shadow None
                            thumb_offset 1

                    vbox spacing 4:
                        label _("Velocidade do texto"):
                            text_size 26
                            text_color "#2cf1ff"
                            padding (15, 2)
                            background Frame("wells/gui/label_frame.png", 10, 10)
                        bar:
                            value Preference("text speed") 
                            xsize 380 ysize 25
                            idle_right_bar Frame("wells/gui/barra_vazia.png", 5, 5)
                            hover_right_bar Frame("wells/gui/barra_vazia.png", 5, 5)
                            idle_left_bar Frame("wells/gui/barra_cheia.png", 5, 5)
                            hover_left_bar Frame("wells/gui/barra_cheia.png", 5, 5)
                            thumb "wells/gui/pino.png"
                            thumb_shadow None
                            thumb_offset 1

                    vbox spacing 4:
                        label _("Tempo do texto"):
                            text_size 26 
                            text_color "#2cf1ff"
                            padding (15, 2)
                            background Frame("wells/gui/label_frame.png", 10, 10)
                        bar:
                            value Preference("auto-forward time") 
                            xsize 380 ysize 25
                            idle_right_bar Frame("wells/gui/barra_vazia.png", 5, 5)
                            hover_right_bar Frame("wells/gui/barra_vazia.png", 5, 5)
                            idle_left_bar Frame("wells/gui/barra_cheia.png", 5, 5)
                            hover_left_bar Frame("wells/gui/barra_cheia.png", 5, 5)
                            thumb "wells/gui/pino.png"
                            thumb_shadow None
                            thumb_offset 1

                vbox:
                    spacing 8     
                    yalign 0.0

                    vbox spacing 2:
                        frame:
                            xalign 0.5
                            background Frame("wells/gui/label_frame.png", 10, 10)
                            padding (15, 2)
                            text "Text Scaling:" size 26 color "#2cf1ff" xalign 0.5
                        bar:
                            value Preference("font size") 
                            xsize 320 ysize 25 xalign 0.5
                            idle_right_bar Frame("wells/gui/barra_vazia.png", 5, 5)
                            hover_right_bar Frame("wells/gui/barra_vazia.png", 5, 5)
                            idle_left_bar Frame("wells/gui/barra_cheia.png", 5, 5)
                            hover_left_bar Frame("wells/gui/barra_cheia.png", 5, 5)
                            thumb "wells/gui/pino.png"
                            thumb_shadow None
                            thumb_offset 1
                        textbutton _("Reset Size"):
                            action Preference("font size", 1.0)
                            xalign 0.5 text_size 22 text_hover_color "#ff4444" yoffset -2

                    vbox spacing 2:
                        frame:
                            xalign 0.5
                            background Frame("wells/gui/label_frame.png", 10, 10)
                            padding (15, 2)
                            text "Line Spacing:" size 26 color "#2cf1ff" xalign 0.5
                        bar:
                            value FieldValue(persistent, "wells_line_spacing", range=50, offset=0) 
                            xsize 320 ysize 25 xalign 0.5
                            idle_right_bar Frame("wells/gui/barra_vazia.png", 5, 5)
                            hover_right_bar Frame("wells/gui/barra_vazia.png", 5, 5)
                            idle_left_bar Frame("wells/gui/barra_cheia.png", 5, 5)
                            hover_left_bar Frame("wells/gui/barra_cheia.png", 5, 5)
                            thumb "wells/gui/pino.png"
                            thumb_shadow None
                            thumb_offset 1
                        textbutton _("Reset Spacing"):
                            action Preference("font line spacing", 1.0)
                            xalign 0.5 text_size 22 text_hover_color "#ff4444" yoffset -2

                    vbox spacing 2:
                        frame:
                            xalign 0.5
                            background Frame("wells/gui/label_frame.png", 10, 10)
                            padding (15, 2)
                            text "Dialogue V offset:" size 26 color "#2cf1ff" xalign 0.5
                        bar:
                            value FieldValue(persistent, "wells_dialogue_y_offset", range=100, offset=-50) 
                            xsize 320 ysize 25 xalign 0.5
                            idle_right_bar Frame("wells/gui/barra_vazia.png", 5, 5)
                            hover_right_bar Frame("wells/gui/barra_vazia.png", 5, 5)
                            idle_left_bar Frame("wells/gui/barra_cheia.png", 5, 5)
                            hover_left_bar Frame("wells/gui/barra_cheia.png", 5, 5)
                            thumb "wells/gui/pino.png"
                            thumb_shadow None
                            thumb_offset 1
                        textbutton "Reiniciar Altura":
                            action SetField(persistent, "wells_dialogue_y_offset", 0)
                            xalign 0.5 text_size 22 text_hover_color "#ff4444" yoffset -2

            vbox:
                spacing 8
                yalign 0.0

                vbox:
                    spacing 6
                    style_prefix "wells_menu_check"
                    button:
                        padding (0, 0, 0, 0)
                        xysize (180, 42)
                        idle_background Frame("wells/gui/Button-idle.png", 5, 5)
                        hover_background Frame("wells/gui/Button-hover.png", 5, 5)
                        action Preference("skip", "toggle")
                        xalign 0.5
                        text _("Pular Texto") xalign 0.5 yalign 0.5 size 20 hover_color "#2bff00"
                    button:
                        padding (0, 0, 0, 0)
                        xysize (180, 42)
                        idle_background Frame("wells/gui/Button-idle.png", 5, 5)
                        hover_background Frame("wells/gui/Button-hover.png", 5, 5)
                        action Preference("after choices", "toggle")
                        xalign 0.5
                        text _("Após Escolhas") xalign 0.5 yalign 0.5 size 20 hover_color "#2bff00"
                    button:
                        padding (0, 0, 0, 0)
                        xysize (180, 42)
                        idle_background Frame("wells/gui/Button-hover.png", 5, 5)
                        hover_background Frame("wells/gui/Button-hover.png", 5, 5)
                        action InvertSelected(Preference("transitions", "toggle"))
                        xalign 0.5
                        text _("Transições") xalign 0.5 yalign 0.5 size 20 hover_color "#2bff00"

                vbox:
                    spacing 6
                    style_prefix "wells_menu_radio"
                    button:
                        padding (0, 0, 0, 0)
                        xysize (180, 42)
                        idle_background Frame("wells/gui/Button-idle.png", 5, 5)
                        hover_background Frame("wells/gui/Button-hover.png", 5, 5)
                        action Preference("rollback side", "disable")
                        xalign 0.5
                        text _("Desabilitado") xalign 0.5 yalign 0.5 size 20 hover_color "#2bff00"
                    button:
                        padding (0, 0, 0, 0)
                        xysize (180, 42)
                        idle_background Frame("wells/gui/Button-idle.png", 5, 5)
                        hover_background Frame("wells/gui/Button-hover.png", 5, 5)
                        action Preference("rollback side", "left")
                        xalign 0.5
                        text _("Esquerda") xalign 0.5 yalign 0.5 size 20 hover_color "#2bff00"
                    button:
                        padding (0, 0, 0, 0)
                        xysize (180, 42)
                        idle_background Frame("wells/gui/Button-idle.png", 5, 5)
                        hover_background Frame("wells/gui/Button-hover.png", 5, 5)
                        action Preference("rollback side", "right")
                        xalign 0.5
                        text _("Direita") xalign 0.5 yalign 0.5 size 20 hover_color "#2bff00"

                vbox:
                    spacing 6
                    style_prefix "wells_menu_radio"
                    button:
                        padding (0, 0, 0, 0)
                        xysize (180, 42)
                        idle_background Frame("wells/gui/Button-idle.png", 5, 5)
                        hover_background Frame("wells/gui/Button-hover.png", 5, 5)
                        action Function(toggle_multiple_dialogue)
                        xalign 0.5
                        text "Dual Dialogue" xalign 0.5 yalign 0.5 size 16 color ("#ffffff" if persistent.multiple_dialogue else "#2bff00") hover_color "#2bff00"
                    button:
                        padding (0, 0, 0, 0)
                        xysize (180, 42)
                        idle_background Frame("wells/gui/Button-idle.png", 5, 5)
                        hover_background Frame("wells/gui/Button-hover.png", 5, 5)
                        action ToggleField(persistent, "wells_dual_dialogue_fix")
                        xalign 0.5
                        text "Diag. Fix: [persistent.wells_dual_dialogue_fix]" xalign 0.5 yalign 0.5 size 18 color ("#2bff00" if persistent.wells_dual_dialogue_fix else "#ffffff") hover_color "#2bff00"
                    button:
                        padding (0, 0, 0, 0)
                        xysize (180, 42)
                        idle_background Frame("wells/gui/Button-idle.png", 5, 5)
                        hover_background Frame("wells/gui/Button-hover.png", 5, 5)
                        action If(persistent.wells_say_mode == 1, 
                                true=SetField(persistent, "wells_say_mode", 0), 
                                false=SetField(persistent, "wells_say_mode", 1))
                        selected True
                        xalign 0.5
                        text _("RENPY: " + ("8.X" if persistent.wells_say_mode == 1 else "7.X")) xalign 0.5 yalign 0.5 size 16 color ("#2bff00" if persistent.wells_say_mode else "#ffffff") hover_color "#2bff00"

        button:
            padding (0, 0, 0, 0)
            xysize (180, 45)
            xpos 670 ypos 675 xanchor 0.5
            idle_background Frame("wells/gui/Button-idle.png", 5, 5)
            hover_background Frame("wells/gui/Button-hover.png", 5, 5)
            action Show("wells_menu_language")
            text _("Voltar") xalign 0.5 yalign 0.5 size 22 hover_color "#2bff00"


################################################################################
## 6. SCREEN GERENCIADOR DE LAYOUTS (SLOTS DE SCREENS)
################################################################################
screen wells_menu_slots():
    modal True
    zorder 200
    tag menu
    add Solid("#00000080") 

    frame:
        xalign 0.5 yalign 0.4
        background Frame("wells/gui/frame_menu.png", 10, 10)

        # --- LÓGICA DE RESOLUÇÃO RESPONSIVA ---
        if config.screen_width == 1920:
            if renpy.variant("small"):
                xsize 1600 ysize 950 padding (60, 50)
            else:
                xsize 1450 ysize 820 padding (50, 40)
        else:
            xsize 1150 ysize 680 padding (40, 35)

        vbox:
            xfill True
            spacing 25

            # Título do Painel
            frame:
                xpos 670
                xanchor 0.5
                ypos 15
                background Frame("wells/gui/label_frame.png", 0, 0)
                padding (10, 10)
                label _("SCREEN SAY MANAGER"):
                    text_size 48 
                    text_color "#ff4444"

            # Container Centralizado para os Botões de Seleção
            vbox:
                xalign 0.5
                yalign 0.5
                spacing 20
                xsize 450

                # --- FILERA 1: CAIXAS DE TEXTO CONVENCIONAIS ---
                label _("SAY SCREEN LAYOUT"):
                    xalign 0.5 
                    text_size 22 
                    text_color "#347bff"
                    padding (20, 5)
                    background Frame("wells/gui/label_frame.png", 10, 10)

                hbox:
                    xalign 0.5
                    spacing 10

                    #button:
                        #padding (0, 0, 0, 0)
                        #xysize (130, 45)

                    # Botão Padrão do Framework
                    button:
                        padding (0, 0, 0, 0)
                        xysize (130, 45)
                        idle_background Frame("wells/gui/Button-idle.png", 5, 5)
                        hover_background Frame("wells/gui/Button-hover.png", 5, 5)
                        action SetField(persistent, "wells_say_slot", 0)
                        text "PADRÃO" xalign 0.5 yalign 0.5 size 14 color ("#2bff00" if persistent.wells_say_slot == 0 else "#ffffff") hover_color "#2bff00"

                hbox:
                    xalign 0.5
                    spacing 10

                    # Botão Framework
                    button:
                        padding (0, 0, 0, 0)
                        xysize (130, 45)
                        idle_background Frame("wells/gui/Button-idle.png", 5, 5)
                        hover_background Frame("wells/gui/Button-hover.png", 5, 5)
                        action SetField(persistent, "wells_say_slot", 3)
                        text "Framework" xalign 0.5 yalign 0.5 size 14 color ("#2bff00" if persistent.wells_say_slot == 3 else "#ffffff") hover_color "#2bff00"

                    # Botão Eternum
                    button:
                        padding (0, 0, 0, 0)
                        xysize (130, 45)
                        idle_background Frame("wells/gui/Button-idle.png", 5, 5)
                        hover_background Frame("wells/gui/Button-hover.png", 5, 5)
                        action SetField(persistent, "wells_say_slot", 2)
                        text "ETERNUM" xalign 0.5 yalign 0.5 size 14 color ("#2bff00" if persistent.wells_say_slot == 2 else "#ffffff") hover_color "#2bff00"

                    # Botão Being a DIK
                    button:
                        padding (0, 0, 0, 0)
                        xysize (130, 45)
                        idle_background Frame("wells/gui/Button-idle.png", 5, 5)
                        hover_background Frame("wells/gui/Button-hover.png", 5, 5)
                        action SetField(persistent, "wells_say_slot", 1)
                        text "BEING A DIK" xalign 0.5 yalign 0.5 size 14 color ("#2bff00" if persistent.wells_say_slot == 1 else "#ffffff") hover_color "#2bff00"

                # --- FILERA 2: REAÇÕES E DIÁLOGOS MÚLTIPLOS ---
                label _("MULTIPLE SAY LAYOUT"):
                    xalign 0.5 
                    text_size 22 
                    text_color "#347bff"
                    padding (20, 5)
                    background Frame("wells/gui/label_frame.png", 10, 10)

                hbox:
                    xalign 0.5
                    spacing 10

                    # Botão Múltiplo Padrão Framework
                    button:
                        padding (0, 0, 0, 0)
                        xysize (130, 45)
                        idle_background Frame("wells/gui/Button-idle.png", 5, 5)
                        hover_background Frame("wells/gui/Button-hover.png", 5, 5)
                        action SetField(persistent, "wells_multiple_slot", 0)
                        text "PADRÃO +" xalign 0.5 yalign 0.5 size 14 color ("#2bff00" if persistent.wells_multiple_slot == 0 else "#ffffff") hover_color "#2bff00"

                    # Botão Eternum Positivo (+)
                    button:
                        padding (0, 0, 0, 0)
                        xysize (130, 45)
                        idle_background Frame("wells/gui/Button-idle.png", 5, 5)
                        hover_background Frame("wells/gui/Button-hover.png", 5, 5)
                        action SetField(persistent, "wells_multiple_slot", 2)
                        text "ETERNUM +" xalign 0.5 yalign 0.5 size 14 color ("#2bff00" if persistent.wells_multiple_slot == 2 else "#ffffff") hover_color "#2bff00"

                    # Botão Incubus
                    button:
                        padding (0, 0, 0, 0)
                        xysize (130, 45)
                        idle_background Frame("wells/gui/Button-idle.png", 5, 5)
                        hover_background Frame("wells/gui/Button-hover.png", 5, 5)
                        action SetField(persistent, "wells_multiple_slot", 6)
                        text "Incubus" xalign 0.5 yalign 0.5 size 14 color ("#2bff00" if persistent.wells_multiple_slot == 6 else "#ffffff") hover_color "#2bff00"

                hbox:
                    xalign 0.5
                    spacing 10

                    button:
                        padding (0, 0, 0, 0)
                        xysize (130, 45)
                        idle_background Frame("wells/gui/Button-idle.png", 5, 5)
                        hover_background Frame("wells/gui/Button-hover.png", 5, 5)
                        action SetField(persistent, "wells_multiple_slot", 4)
                        text "Esquerda" xalign 0.5 yalign 0.5 size 14 color ("#2bff00" if persistent.wells_multiple_slot == 4 else "#ffffff") hover_color "#2bff00"

                    button:
                        padding (0, 0, 0, 0)
                        xysize (130, 45)
                        idle_background Frame("wells/gui/Button-idle.png", 5, 5)
                        hover_background Frame("wells/gui/Button-hover.png", 5, 5)
                        action SetField(persistent, "wells_multiple_slot", 3)
                        text "ETERNUM -" xalign 0.5 yalign 0.5 size 14 color ("#2bff00" if persistent.wells_multiple_slot == 3 else "#ffffff") hover_color "#2bff00"

                    button:
                        padding (0, 0, 0, 0)
                        xysize (130, 45)
                        idle_background Frame("wells/gui/Button-idle.png", 5, 5)
                        hover_background Frame("wells/gui/Button-hover.png", 5, 5)
                        action SetField(persistent, "wells_multiple_slot", 5)
                        text "Direita" xalign 0.5 yalign 0.5 size 14 color ("#2bff00" if persistent.wells_multiple_slot == 5 else "#ffffff") hover_color "#2bff00"

        # Botão inferior para voltar ao menu principal do framework
        button:
            padding (0, 0, 0, 0)
            xysize (180, 45)
            xpos 670 ypos 675 xanchor 0.5
            idle_background Frame("wells/gui/Button-idle.png", 5, 5)
            hover_background Frame("wells/gui/Button-hover.png", 5, 5)
            action [Show("wells_menu_language"), Hide("wells_menu_slots")]
            text _("Voltar") xalign 0.5 yalign 0.5 size 22 hover_color "#2bff00"
