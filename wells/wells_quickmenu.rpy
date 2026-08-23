################################################################################
## ATALHO ATIVADOR UNIVERSAL (SHIFT+L) VIA KEYMAP
################################################################################
init 999 python:
    config.keymap["wells_toggle_qm"] = ["shift_K_l"]

    def wells_toggle_quickmenu_action():
        store.quick_menu = not store.quick_menu
        if store.quick_menu:
            renpy.notify("Quick SHOW")
        else:
            renpy.notify("Quick HIDE")
        renpy.restart_interaction()

    config.underlay.append(renpy.Keymap(wells_toggle_qm=wells_toggle_quickmenu_action))

# [CORREÇÃO] Declarado explicitamente em init -1 para o Ren'Py carregar antes da screen
init -1 transform wells_deslizar_topo:
    xanchor 0.5 yanchor 0.0
    on show:
        ypos -200 
        easein 0.4 ypos 0
    on hide:
        easeout 0.4 ypos -200

# --- 1. O BOTÃO DISPARADOR (Invisível no modo idle, se revela ao passar o mouse) ---
init 999:
    screen quick_menu():
        zorder 198
        tag quick_menu
        modal False 

        if quick_menu:
            if not renpy.get_screen("custom_menu_wells"):
                imagebutton:
                    xalign 0.5 ypos 0  
                    idle "wells/gui/gatilho_idle.png"
                    hover "wells/gui/gatilho-hover.png"
                    action Show("custom_menu_wells")

# --- 2. A CAIXINHA COM OS BOTÕES METÁLICOS (Desliza e fixa no topo) ---
screen custom_menu_wells():
    zorder 199 
    tag custom_quick
    modal True # Garante o foco total nos botões enquanto aberta

    # Botão invisível de fundo que cobre a tela cheia: se clicar fora do menu, fecha ele
    button:
        action Hide("custom_menu_wells")
        background None 

    # Painel central que desliza do topo com os seus botões metálicos atuais
    frame:
        at wells_deslizar_topo
        xalign 0.5 ypos 0
        background Frame("wells/gui/base_nova.png", 3, 3)
        padding (18, 8, 18, 10)  
        
        hbox:
            spacing 6 
            yalign 0.5 

            # BOTÃO 1: Menu (Abre o painel estendido e fecha a barra)
            button:
                padding (0, 0, 0, 0)
                xysize (70, 40) 
                idle_background Frame("wells/gui/Button-idle.png", 3, 3)
                hover_background Frame("wells/gui/Button-hover.png", 3, 3)
                action [Hide("custom_menu_wells"), Show("quick_mod")]
                text _("Menu") xalign 0.5 yalign 0.5 size 20 hover_color "#2bff00"

            # BOTÃO 2: BACK (Executa rollback e recolhe a barra)
            button:
                padding (0, 0, 0, 0)
                xysize (70, 40)
                idle_background Frame("wells/gui/Button-idle.png", 3, 3)
                hover_background Frame("wells/gui/Button-hover.png", 3, 3)
                action [Rollback(), Hide("custom_menu_wells")]
                xalign 0.5
                text _("Back") xalign 0.5 yalign 0.5 size 22 hover_color "#2bff00"

            # BOTÃO 3: SKIP (Ativa o salto e recolhe a barra)
            button:
                padding (0, 0, 0, 0)
                xysize (70, 40)
                idle_background Frame("wells/gui/Button-idle.png", 3, 3)
                hover_background Frame("wells/gui/Button-hover.png", 3, 3)
                action [Skip(), Hide("custom_menu_wells")] 
                alternate Skip(fast=True, confirm=True)
                xalign 0.5
                text _("Skip") xalign 0.5 yalign 0.5 size 22 hover_color "#2bff00"

################################################################################
## TELA DE PAUSA CENTRALIZADA
################################################################################
init 999:
    screen quick_mod():
        zorder 199          
        tag quick_menu_tela 
        modal True          

        frame:
            style "empty"
            background Solid("#00000060") 
            xsize 1.0 ysize 1.0   

            frame:
                xalign 0.5
                yalign 0.5
                style "empty"
                background Frame("wells/gui/quickbox.png", 20, 20)
                xsize 340
                ysize 600
                padding (35, 45, 35, 5)
################################################################################
## MODULE: wells_quickmenu.rpy (BLOCO 3 DE 4)
################################################################################

                vbox:
                    spacing 12
                    xalign 0.5
                    yalign 0.5
                    xsize 220 
                    style_prefix "wells_menu_quick"

                    # --- BOTÃO 1: FECHAR ---
                    button:
                        padding (0, 0, 0, 0)
                        xysize (180, 45) 
                        idle_background Frame("wells/gui/Button-idle.png", 5, 5)
                        hover_background Frame("wells/gui/Button-hover.png", 5, 5)
                        action [Hide("quick_mod"), Show("quick_menu")]
                        xalign 0.5
                        text _("Close") xalign 0.5 yalign 0.5 size 22 hover_color "#2bff00"

                    # --- BOTÃO 4: SALVAR ---
                    button:
                        padding (0, 0, 0, 0)
                        xysize (180, 45)
                        idle_background Frame("wells/gui/Button-idle.png", 5, 5)
                        hover_background Frame("wells/gui/Button-hover.png", 5, 5)
                        action [SetVariable("wells_sl_action", "save"), Show("wells_custom_saveload"), Hide("quick_mod")]
                        xalign 0.5
                        text _("Save") xalign 0.5 yalign 0.5 size 22 hover_color "#2bff00"

                    # --- BOTÃO 5: CARREGAR ---
                    button:
                        padding (0, 0, 0, 0)
                        xysize (180, 45)
                        idle_background Frame("wells/gui/Button-idle.png", 5, 5)
                        hover_background Frame("wells/gui/Button-hover.png", 5, 5)
                        action [SetVariable("wells_sl_action", "load"), Show("wells_custom_saveload"), Hide("quick_mod")]
                        xalign 0.5
                        text _("Load") xalign 0.5 yalign 0.5 size 22 hover_color "#2bff00"

                    # --- BOTÃO 6: OPÇÕES ---
                    button:
                        padding (0, 0, 0, 0)
                        xysize (180, 45)
                        idle_background Frame("wells/gui/Button-idle.png", 5, 5)
                        hover_background Frame("wells/gui/Button-hover.png", 5, 5)
                        action [ShowMenu("preferences"), Hide("quick_mod"), Show("quick_menu")] 
                        xalign 0.5
                        text _("Config") xalign 0.5 yalign 0.5 size 22 hover_color "#2bff00"

                    # --- BOTÃO 7: MENU UNIVERSAL ---
                    button:
                        padding (0, 0, 0, 0)
                        xysize (180, 45)
                        idle_background Frame("wells/gui/Button-idle.png", 5, 5)
                        hover_background Frame("wells/gui/Button-hover.png", 5, 5)
                        action [Show("wells_menu_language"), Hide("quick_mod")] 
                        xalign 0.5
                        text _("Wells Menu") xalign 0.5 yalign 0.5 size 22 hover_color "#2bff00"
