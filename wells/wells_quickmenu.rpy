################################################################################
## MODULE: wells_quickmenu.rpy (ESTÁGIO 1 E 2 VIA SHOWMENU)
################################################################################

# 1. INJEÇÃO DA SUA TELA: Garante que o seu menu do topo rode via overlay direto
init 999 python:
    if "quick_menu1" not in config.overlay_screens:
        config.overlay_screens.append("quick_menu1")


# 2. O SEU ESTÁGIO 1 (Totalmente Limpo e Fixo no Topo)
init 999:
    screen quick_menu1():
        zorder 198
        tag quick_menu1
        modal False 

        imagebutton:
            xalign 0.5 ypos 0  
            idle "wells/gui/gatilho_idle.png"
            hover "wells/gui/gatilho-hover.png"
            action ShowMenu("quick_menu2")

# 1. Deixamos a tela antiga que o criador chama vazia para o rodapé sumir do jogo
screen quick_menu():
    variant ("small", "medium", "large")
    tag quick_menu
    pass # Transforma o menu do rodapé em fumaça invisível!

################################################################################
## MODULE: wells_quickmenu.rpy (ESTÁGIO 3: PAINEL CENTRAL VIA SHOWMENU)
################################################################################

screen quick_menu2():
    zorder 199 
    tag menu # O tag menu garante que o Ren'Py trate a tela como um menu de pausa oficial
    modal False 

    # Clicou fora da barra, volta para o jogo e reativa o gatilho discreto
    button:
        action Return()
        background None 

    # Fundo escuro para dar foco à caixinha central
    frame:
        style "empty"
        background None
        xsize 1.0 ysize 1.0   

        # Clicou no fundo escuro fora da caixa, fecha o menu e volta para o jogo
        button:
            action Return()
            background None 

        # Sua moldura central original
        frame:
            xalign 0.5 yalign 0.5
            style "empty"
            background Frame("wells/gui/quickbox.png", 20, 20)
            xsize 340 ysize 600
            padding (35, 45, 35, 5)

            vbox:
                spacing 12
                xalign 0.5 yalign 0.5
                xsize 220 
                style_prefix "wells_menu_quick"

                # --- BOTÃO 1: FECHAR (Retorna ao jogo) ---
                button:
                    padding (0, 0, 0, 0) xysize (180, 45) 
                    idle_background Frame("wells/gui/Button-idle.png", 5, 5)
                    hover_background Frame("wells/gui/Button-hover.png", 5, 5)
                    action Return()
                    xalign 0.5
                    text _("Close") xalign 0.5 yalign 0.5 size 22 hover_color "#2bff00"
                # --- BOTÃO 2: ROLLBACK (Chama a nova tela exclusiva de save) ---
                button:
                    padding (0, 0, 0, 0) xysize (180, 45)
                    idle_background Frame("wells/gui/Button-idle.png", 5, 5)
                    hover_background Frame("wells/gui/Button-hover.png", 5, 5)
                    action [Rollback(), Return()]
                    xalign 0.5
                    text _("bACK") xalign 0.5 yalign 0.5 size 22 hover_color "#2bff00"
                # --- BOTÃO 3: SKIP (Chama a nova tela exclusiva de save) ---
                button:
                    padding (0, 0, 0, 0) xysize (180, 45)
                    idle_background Frame("wells/gui/Button-idle.png", 5, 5)
                    hover_background Frame("wells/gui/Button-hover.png", 5, 5)
                    action [Skip(), Return()] 
                    alternate Skip(fast=True, confirm=True)
                    xalign 0.5
                    text _("Skip") xalign 0.5 yalign 0.5 size 22 hover_color "#2bff00"
                # --- BOTÃO 4: SALVAR (Chama a nova tela exclusiva de save) ---
                button:
                    padding (0, 0, 0, 0) xysize (180, 45)
                    idle_background Frame("wells/gui/Button-idle.png", 5, 5)
                    hover_background Frame("wells/gui/Button-hover.png", 5, 5)
                    action Show("wells_custom_save")
                    xalign 0.5
                    text _("Save") xalign 0.5 yalign 0.5 size 22 hover_color "#2bff00"
                # --- BOTÃO 5: CARREGAR (Chama a nova tela exclusiva de load) ---
                button:
                    padding (0, 0, 0, 0) xysize (180, 45)
                    idle_background Frame("wells/gui/Button-idle.png", 5, 5)
                    hover_background Frame("wells/gui/Button-hover.png", 5, 5)
                    action Show("wells_custom_load")
                    xalign 0.5
                    text _("Load") xalign 0.5 yalign 0.5 size 22 hover_color "#2bff00"
                # --- BOTÃO 6: CONFIGURAÇÕES PADRÃO DO JOGO ---
                button:
                    padding (0, 0, 0, 0) xysize (180, 45)
                    idle_background Frame("wells/gui/Button-idle.png", 5, 5)
                    hover_background Frame("wells/gui/Button-hover.png", 5, 5)
                    action ShowMenu("preferences") 
                    xalign 0.5
                    text _("Config") xalign 0.5 yalign 0.5 size 22 hover_color "#2bff00"
                # --- BOTÃO 7: MENU UNIVERSAL DA SUA FRAMEWORK ---
                button:
                    padding (0, 0, 0, 0) xysize (180, 45)
                    idle_background Frame("wells/gui/Button-idle.png", 5, 5)
                    hover_background Frame("wells/gui/Button-hover.png", 5, 5)
                    action Show("wells_menu_language") 
                    xalign 0.5
                    text _("Wells Menu") xalign 0.5 yalign 0.5 size 22 hover_color "#2bff00"
