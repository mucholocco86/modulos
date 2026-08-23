################################################################################
## MODULE: wells_saveload.rpy (CONTEÚDO COMPLETO)
################################################################################

# Variável para controlar o modo (salvar/carregar)
default wells_sl_action = "save"

screen wells_custom_saveload():
    modal True
    zorder 199 
    tag wells_saveload_screen
    add Solid("#000000aa")

    # Variável local inline para higienizar e converter com segurança a página atual para número inteiro
    $ current_page_num = int(persistent._file_page) if isinstance(persistent._file_page, (int, float)) or (isinstance(persistent._file_page, basestring if renpy.version_tuple < (8, 0, 0) else str) and persistent._file_page.isdigit()) else 1

    frame:
        xalign 0.5 yalign 0.4
        background Frame("wells/gui/frame_menu.png", 10, 10)
        xsize 1450 ysize 820 padding (50, 40)

        # Usamos uma caixa fixed estrutural para podermos amarrar os componentes de forma absoluta
        fixed:
            xfill True yfill True

            # --- TOPO PARTE 1: TÍTULO FIXADO À ESQUERDA ---
            frame:
                xpos 0 ypos 10
                background Frame("wells/gui/label_frame.png", 10, 10)
                padding (30, 8)
                if wells_sl_action == "save":
                    text "SALVAR" size 32 color "#ff4444"
                else:
                    text "CARREGAR" size 32 color "#ff4444"

            # --- TOPO PARTE 2: BOTÕES CRAVADOS NO CENTRO REAL DA MOLDURA VERMELHA ---
            hbox:
                xalign 0.5 ypos 10 
                spacing 12

                # Atalho para Salvamento Automático
                button:
                    padding (0, 0, 0, 0)
                    xysize (55, 55)
                    idle_background Frame("wells/gui/Button-idle.png", 3, 3)
                    hover_background Frame("wells/gui/Button-hover.png", 3, 3)
                    action FilePage("auto")
                    yalign 0.5
                    if persistent._file_page == "auto":
                        text _("A") xalign 0.5 yalign 0.5 size 26 color "#2bff00"
                    else:
                        text _("A") xalign 0.5 yalign 0.5 size 26 color "#ffffff"

                # Atalho para Salvamento Rápido
                button:
                    padding (0, 0, 0, 0)
                    xysize (55, 55)
                    idle_background Frame("wells/gui/Button-idle.png", 3, 3)
                    hover_background Frame("wells/gui/Button-hover.png", 3, 3)
                    action FilePage("quick")
                    yalign 0.5
                    if persistent._file_page == "quick":
                        text _("Q") xalign 0.5 yalign 0.5 size 26 color "#2bff00"
                    else:
                        text _("Q") xalign 0.5 yalign 0.5 size 26 color "#ffffff"

                # Botão Voltar 10 Páginas (Blindado contra Strings)
                button:
                    padding (0, 0, 0, 0)
                    xysize (55, 55)
                    idle_background Frame("wells/gui/Button-idle.png", 3, 3)
                    hover_background Frame("wells/gui/Button-hover.png", 3, 3)
                    action FilePage(max(1, current_page_num - 10))
                    yalign 0.5
                    text _("<<<") xalign 0.5 yalign 0.5 size 22 hover_color "#2bff00"

                # Botão Voltar 1 Página
                button:
                    padding (0, 0, 0, 0)
                    xysize (55, 55)
                    idle_background Frame("wells/gui/Button-idle.png", 3, 3)
                    hover_background Frame("wells/gui/Button-hover.png", 3, 3)
                    action FilePagePrevious()
                    yalign 0.5
                    text _("<<") xalign 0.5 yalign 0.5 size 26 hover_color "#2bff00"

                # Contador de Página Centralizado
                frame:
                    yalign 0.5
                    background Frame("wells/gui/Button-hover.png", 5, 5)
                    padding (20, 8, 20, 8)
                    minimum (70, 55)
                    if persistent._file_page == "auto":
                        text "A" xalign 0.5 yalign 0.5 size 32 color "#2bff00"
                    elif persistent._file_page == "quick":
                        text "Q" xalign 0.5 yalign 0.5 size 32 color "#2bff00"
                    else:
                        text " [persistent._file_page]" xalign 0.5 yalign 0.5 size 32 color "#2bff00"

                # Botão Avançar 1 Página
                button:
                    padding (0, 0, 0, 0)
                    xysize (55, 55)
                    idle_background Frame("wells/gui/Button-idle.png", 3, 3)
                    hover_background Frame("wells/gui/Button-hover.png", 3, 3)
                    action FilePageNext()
                    yalign 0.5
                    text _(">>") xalign 0.5 yalign 0.5 size 26 hover_color "#2bff00"

                # Botão Avançar 10 Páginas (Blindado contra Strings)
                button:
                    padding (0, 0, 0, 0)
                    xysize (55, 55)
                    idle_background Frame("wells/gui/Button-idle.png", 3, 3)
                    hover_background Frame("wells/gui/Button-hover.png", 3, 3)
                    action FilePage(current_page_num + 10)
                    yalign 0.5
                    text _(">>>") xalign 0.5 yalign 0.5 size 22 hover_color "#2bff00"

            # --- CENTRO: CONTAINER DO VIEWPORT COM SLOTS OTIMIZADOS ---
            side "c r":
                xalign 0.5 ypos 95 
                spacing 25 

                vpgrid:
                    id "wells_slots_vp"
                    cols 3                 
                    rows 5                 
                    xspacing 35            
                    yspacing 30            
                    xsize 1250             
                    ysize 565              
                    mousewheel True        
                    draggable True         
                    arrowkeys True         

                    for slot in range(1, 16):
                        vbox:
                            xysize (360, 262) 
                            spacing 5

                            fixed:
                                xysize (360, 230) 

                                button:
                                    xfill True yfill True
                                    background Solid("#00000066")
                                    action If(wells_sl_action == "save", FileSave(slot), FileLoad(slot))

                                    if FileLoadable(slot):
                                        fixed:
                                            xfill True yfill True
                                            frame:
                                                xfill True yfill True
                                                background Frame(FileScreenshot(slot), 0, 0)
                                    else:
                                        frame:
                                            xfill True yfill True
                                            background Frame("wells/gui/slot_vazio.png", 0, 0)

                                if FileLoadable(slot):
                                    button:
                                        padding (0, 0, 0, 0)
                                        xysize (72, 28) 
                                        idle_background Frame("wells/gui/Button-idle.png", 3, 3)
                                        hover_background Frame("wells/gui/Button-hover.png", 3, 3)
                                        action FileDelete(slot) 
                                        text _("Delete") xalign 0.5 yalign 0.5 size 20 hover_color "#2bff00"

                            # Exibição de Data Puramente Numérica abaixo do slot
                            if FileLoadable(slot):
                                text FileTime(slot, format=_("{#file_time}%d.%m.%Y - %H:%M"), empty=_("Vazio")):
                                    xalign 0.5
                                    size 22
                                    color "#2bff00"
                            else:
                                text "Vazio":
                                    xalign 0.5
                                    size 22
                                    color "#ffffff"

                vbar:
                    value YScrollValue("wells_slots_vp")
                    top_bar Frame("wells/gui/vertical_cheia.png", 0, 0)   
                    bottom_bar Frame("wells/gui/vertical_vazia.png", 0, 0) 
                    thumb Frame("wells/gui/v_pino.png", 10, 0)             
                    xsize 20                                               

        # --- BASE: BOTÃO VOLTAR EM POSIÇÃO RELATIVA PERFEITA DENTRO DO FRAME ---
        button:
            padding (0, 0, 0, 0)
            xysize (180, 45) 
            xalign 0.5 yalign 0.985 
            idle_background Frame("wells/gui/Button-idle.png", 5, 5)
            hover_background Frame("wells/gui/Button-hover.png", 5, 5)
            action [Hide("wells_custom_saveload")]
            text _("Voltar") xalign 0.5 yalign 0.5 size 22 hover_color "#2bff00"
