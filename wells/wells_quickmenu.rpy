################################################################################
## MODULE: wells_quickmenu.rpy (CORRIGIDO E OTIMIZADO)
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
            xysize (120, 40)
            idle "wells/gui/gatilho_idle.png"
            hover "wells/gui/gatilho-hover.png"
            action ShowMenu("quick_menu2")
            alt " Quick "

# Deixamos a tela antiga vazia para o rodapé padrão sumir do jogo
screen quick_menu():
    variant ("small", "medium", "large")
    tag quick_menu
    pass 

# --- 2. A CAIXINHA COM OS BOTÕES METÁLICOS (Estágio 2 - Menu suspenso) ---
screen quick_menu2():
    zorder 199 
    tag menu # Garante tratamento como menu de pausa oficial
    modal False 

    # Clicou fora da barra em qualquer lugar da tela, fecha e volta para o jogo
    button:
        action Return()
        background None
        xsize 1.0 ysize 1.0

    # Seu painel metálico fixado no topo centralizado
    frame:
        xalign 0.5 ypos 0
        background Frame("wells/gui/base_nova.png", 3, 3)
        padding (14, 8, 12, 8)  
        
        # Alterado de vbox para hbox para os botões ficarem lado a lado na horizontal
        hbox:
            spacing 10 
            yalign 0.5 

            # BOTÃO 1: Menu (Chama o estágio 3)
            imagebutton:
                xysize (120, 40)
                idle "wells/gui/imgbutton/menu_idle.png"
                hover "wells/gui/imgbutton/menu_hover.png"
                action ShowMenu("quick_menu3")
                alt " Menu "
            # BOTÃO 2: BACK (Executa rollback)
            imagebutton:
                xysize (120, 40)
                idle "wells/gui/imgbutton/rollback_idle.png"
                hover "wells/gui/imgbutton/rollback_hover.png"
                action (Rollback(), Return())
                alt " Rollback "
            # BOTÃO 3: SKIP (Ativa o salto)
            imagebutton:
                xysize (120, 40)
                idle "wells/gui/imgbutton/skip_idle.png"
                hover "wells/gui/imgbutton/skip_hover.png"
                action (Skip(), Return()) 
                alternate Skip(fast=True, confirm=True)
                alt " Skip "

# --- 3. PAINEL CENTRALIZADO DE FUNÇÕES (Estágio 3) ---
screen quick_menu3():
    zorder 199          
    tag menu 
    modal False          

    # Fundo escuro cobrindo toda a extensão da tela
    frame:
        style "empty"
        background Solid("#00000060") 
        xsize 1.0 ysize 1.0   
        
        # Botão invisível de fechar agora cobre o fundo de forma absoluta sem empurrar a moldura
        button:
            action Return()
            background None
            xsize 1.0 ysize 1.0

    # Moldura centralizada perfeitamente no meio da tela através de coordenadas diretas
    frame:
        xalign 0.5 yalign 0.5
        style "empty"
        background Frame("wells/gui/quickbox.png", 20, 20)
        xsize 340 ysize 600
        padding (35, 45, 35, 5)

        vbox:
            spacing 25
            xalign 0.5 yalign 0.5

            # --- BOTÃO 1: CLOSE ---
            imagebutton:
                xysize (180, 34)
                xalign 0.5
                idle "wells/gui/imgbutton/close_idle.png"
                hover "wells/gui/imgbutton/close_hover.png"
                action Return()
                alt "Close"

            # --- BOTÃO 2: SAVE ---
            imagebutton:
                xysize (180, 34)
                xalign 0.5
                idle "wells/gui/imgbutton/save_idle.png"
                hover "wells/gui/imgbutton/save_hover.png"
                action Show("wells_custom_save")
                alt "Save"

            # --- BOTÃO 3: LOAD ---
            imagebutton:
                xysize (180, 34)
                xalign 0.5
                idle "wells/gui/imgbutton/load_idle.png"
                hover "wells/gui/imgbutton/load_hover.png"
                action Show("wells_custom_load")
                alt "Load"

            # --- BOTÃO 4: CONFIGS ---
            imagebutton:
                xysize (180, 34)
                xalign 0.5
                idle "wells/gui/imgbutton/config_idle.png"
                hover "wells/gui/imgbutton/config_hover.png"
                action ShowMenu("preferences")
                alt "Configs"

            # --- BOTÃO 5: WELLS FRAMEWORK ---
            imagebutton:
                xysize (180, 34)
                xalign 0.5
                idle "wells/gui/imgbutton/wells_idle.png"
                hover "wells/gui/imgbutton/wells_hover.png"
                action Show("wells_menu_language")
                alt "Wells menu"

            # --- BOTÃO 6: MAIN MENU ---
            imagebutton:
                xysize (180, 34)
                xalign 0.5
                idle "wells/gui/imgbutton/main_idle.png"
                hover "wells/gui/imgbutton/main_hover.png"
                action MainMenu()
                alt "Main menu"
