################################################################################
## QUICK MENU MOVEL
################################################################################

# =============================================================================
# VARIÁVEIS E FUNÇÕES DO SISTEMA (CÁLCULO SEGURO DE BORDA)
# =============================================================================
init python
    # Estado do menu (False = Botão Fechado  True = Barra Aberta)
    if not hasattr(store, 'wells_aberto')
        store.wells_aberto = False

    # Posições estáveis na memória
    if not hasattr(store, 'wells_x')
        store.wells_x = 14
    if not hasattr(store, 'wells_y')
        store.wells_y = 500

    # Posição calculada para a barra grande abrir sem saltos
    if not hasattr(store, 'wells_render_x')
        store.wells_render_x = 14

    # Função universal estável
    def salvar_pos_universal(drags, drop)
        store.wells_x = drags[0].x
        store.wells_y = drags[0].y
        
        # Largura estimada da sua barra grande com os botões (aprox. 650 pixels)
        largura_barra = 650
        limite_direito = config.screen_width - largura_barra
        
        # Se você soltar o botão muito perto da direita, a barra recua o necessário
        if store.wells_x  limite_direito
            store.wells_render_x = limite_direito
        else
            store.wells_render_x = store.wells_x
            
        return

    # Mantido para compatibilidade absoluta com os Saves antigos
    def salvar_pos_botao(drags, drop)
        return salvar_pos_universal(drags, drop)

    def salvar_pos_menu(drags, drop)
        return salvar_pos_universal(drags, drop)

# Transição visual original mantida
transform wells_float_right
    xanchor 0.0 yanchor 1.0
    on show
        xpos -1000
        easein 0.5 xpos 0.0
    on hide
        easeout 0.5 xpos -1000

# =============================================================================
# A TELA ÚNICA INTELIGENTE (SEM ALTERAÇÃO DE ÂNCORA)
# =============================================================================
screen quick_menu()
    zorder 200          
    tag quick_menu
    modal False 

    if quick_menu
        draggroup
            
            # --- ESTADO 1 O BOTÃO AZUL FECHADO (FIXO E ESTÁVEL) ---
            if not store.wells_aberto
                drag
                    drag_name id_botao_fechado 
                    draggable True
                    drag_raise True
                    dragged salvar_pos_universal
                    
                    # Âncora fixa padrão impede o botão de saltar na tela [1]
                    xanchor 0.0
                    yanchor 0.0
                    xpos store.wells_x
                    ypos store.wells_y

                    frame
                        at wells_float_right
                        background Frame(wellsguibase_nova.png, 3, 3)
                        # Deixa 3 pixels de espaço na Esquerda, Topo, Direita e Base
                        padding (2, 3, 2, 3)
                        
                        imagebutton
                            idle wellsguibtn_quick_idle.png
                            hover wellsguibtn_quick_hover.png
                            action SetVariable(store.wells_aberto, True)
                            focus_mask True
                            alt Abrir Quick Menu

            # --- ESTADO 2 A BARRA GRANDE ABERTA (RECUO MATEMÁTICO SEGURO) ---
            else
                drag
                    drag_name id_barra_aberta 
                    draggable True
                    drag_raise True
                    dragged salvar_pos_universal
                    
                    xanchor 0.0
                    yanchor 0.0
                    # Usa a coordenada segura calculada em Python
                    xpos store.wells_render_x
                    ypos store.wells_y

                    frame
                        at wells_float_right
                        background Frame(wellsguiquick_aberto.png, 10, 10)
                        padding (25, 18, 30, 18) 

                        hbox
                            spacing 15      
                            yalign 0.5
                            style_prefix wells_menu_quick

                            imagebutton
                                idle wellsguibtn_fechar_idle.png
                                hover wellsguibtn_fechar_hover.png
                                action SetVariable(store.wells_aberto, False)
                                alt Fechar Menu

                            imagebutton
                                idle wellsguibtn_voltar_idle.png
                                hover wellsguibtn_voltar_hover.png
                                action [Rollback()]
                                alt Voltar Linha

                            imagebutton
                                idle wellsguibtn_pular_idle.png
                                hover wellsguibtn_pular_hover.png
                                action [Skip(), SetVariable(store.wells_aberto, False)] 
                                alternate Skip(fast=True, confirm=True)
                                alt Pular Diálogo

                            imagebutton
                                idle wellsguibtn_salvar_idle.png
                                hover wellsguibtn_salvar_hover.png
                                action [ShowMenu(save), SetVariable(store.wells_aberto, False)] 
                                alt Salvar Jogo

                            imagebutton
                                idle wellsguibtn_carregar_idle.png
                                hover wellsguibtn_carregar_hover.png
                                action [ShowMenu(load), SetVariable(store.wells_aberto, False)] 
                                alt Carregar Jogo

                            imagebutton
                                idle wellsguibtn_opcoes_idle.png
                                hover wellsguibtn_opcoes_hover.png
                                action [ShowMenu(preferences), SetVariable(store.wells_aberto, False)] 
                                alt Opções

                            imagebutton
                                idle wellsguibtn_menu_idle.png
                                hover wellsguibtn_menu_hover.png
                                action [Show(wells_menu_language), SetVariable(store.wells_aberto, False)] 
                                alt Menu Universal

                            imagebutton
                                idle wellsguibtn_mod_idle.png
                                hover wellsguibtn_mod_hover.png
                                action [Show(mod_menu), SetVariable(store.wells_aberto, False)] 
                                alt mod screen
