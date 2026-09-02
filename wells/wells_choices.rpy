# ===============================================================================
# MODULE: wells_choices.rpy (SISTEMA ADAPTATIVO UNIVERSAL DE ESCOLHAS)
# ===============================================================================
screen choice(items):
    style_prefix "choice"

    ## 1. SLOT 0: PASS-THROUGH CIRÚRGICO (ESTRUTURA ORIGINAL DO JOGO HOSPEDEIRO)
    if persistent.wells_choice_slot == 0:
        vbox:
            # Controladores universais do seu painel
            xalign (persistent.wells_choice_xpos if persistent.wells_choice_xpos is not None else 0.5)
            yalign (persistent.wells_choice_ypos if persistent.wells_choice_ypos is not None else 0.5)
            spacing (persistent.wells_choice_spacing if persistent.wells_choice_spacing is not None else 22)

            for i in items:
                # Captura dinâmica e segura para loops padrão ou desestruturados (tuplas)
                python:
                    try:
                        caption = i.caption
                        action = i.action
                    except:
                        # Captura o formato de índices do laboratório atual
                        caption = i[0]
                        action = i[1]

                if action:
                    button:
                        action action
                        style "wells_choice_button"
                        # Suas barras de tamanho controlando a largura da caixa do botão
                        xminimum (persistent.wells_choice_width if persistent.wells_choice_width is not None else 100)
                        xmaximum (persistent.wells_choice_width if persistent.wells_choice_width is not None else 100)
                        
                        text caption:
                            style "wells_choice_text"
                            size (persistent.wells_choice_size if persistent.wells_choice_size is not None else 22)
                            xalign 0.5
                            text_align 0.5
                else:
                    text caption style "wells_choice_text"
    ## 2. SLOT 1: PERSONALIZAÇÃO MANUAL E LIVRE DO SEU FRAMEWORK
    else:
        vbox:
            style "choice_vbox" 
            xalign (persistent.wells_choice_xpos if persistent.wells_choice_xpos is not None else 0.5)
            yalign (persistent.wells_choice_ypos if persistent.wells_choice_ypos is not None else 0.5)
            spacing (persistent.wells_choice_spacing if persistent.wells_choice_spacing is not None else 22)

            for i in items:
                textbutton i.caption:
                    action i.action
                    text_size (persistent.wells_choice_size if persistent.wells_choice_size is not None else 22)
                    xalign 0.5         
                    text_align 0.5     
                    xminimum (persistent.wells_choice_width if persistent.wells_choice_width is not None else 100)
                    xmaximum (persistent.wells_choice_width if persistent.wells_choice_width is not None else 100)
