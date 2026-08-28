# ==========================================
# MODULE: wells_choices.rpy
# ==========================================
screen choice(items):
    style_prefix "choice"

    vbox:
        style "choice_vbox" 
        xalign persistent.wells_choice_xpos
        yalign persistent.wells_choice_ypos
        spacing persistent.wells_choice_spacing

        for i in items:
            textbutton i.caption:
                action i.action
                text_size persistent.wells_choice_size
                xalign 0.5         
                text_align 0.5     
                # [ADICIONADO] Controla de forma idêntica o tamanho mínimo e máximo do botão horizontalmente
                xminimum persistent.wells_choice_width
                xmaximum persistent.wells_choice_width
