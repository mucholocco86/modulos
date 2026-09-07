################################################################################
## WELLS FRAMEWORK — SISTEMA UNIVERSAL DE ESCOLHAS
## TESTE DE CONEXÃO COM WELLS WALKTHROUGH
################################################################################

init 999 screen choice(items):
    style_prefix "choice"

    if persistent.wells_choice_slot == 0:

        vbox:
            xalign (persistent.wells_choice_xpos if persistent.wells_choice_xpos is not None else 0.5)
            yalign (persistent.wells_choice_ypos if persistent.wells_choice_ypos is not None else 0.5)
            spacing (persistent.wells_choice_spacing if persistent.wells_choice_spacing is not None else gui.choice_spacing)

            for i in items:

                python:
                    if hasattr(i, "caption"):
                        caption = i.caption
                        action = i.action
                    else:
                        caption = i[0]
                        action = i[1]

                    wells_walkthrough_info = wells_walkthrough_get_info(items, i)

                if action:
                    button:
                        action action
                        style "wells_choice_button"

                        xminimum (persistent.wells_choice_width if persistent.wells_choice_width is not None else 920)
                        xmaximum (persistent.wells_choice_width if persistent.wells_choice_width is not None else 920)

                        vbox:
                            xalign 0.5
                            spacing 4

                            text caption:
                                style "wells_choice_text"
                                size (persistent.wells_choice_size if persistent.wells_choice_size is not None else gui.choice_button_text_size)
                                xalign 0.5
                                text_align 0.5

                            if wells_walkthrough_info:
                                text wells_walkthrough_info:
                                    size wells_walkthrough_text_size(18)
                                    xalign 0.5
                                    text_align 0.5
                                    color "#39ff14"

                else:
                    text caption style "wells_choice_text"

    else:

        vbox:
            style "choice_vbox"
            xalign (persistent.wells_choice_xpos if persistent.wells_choice_xpos is not None else 0.5)
            yalign (persistent.wells_choice_ypos if persistent.wells_choice_ypos is not None else 0.5)
            spacing (persistent.wells_choice_spacing if persistent.wells_choice_spacing is not None else gui.choice_spacing)

            for i in items:

                python:
                    if hasattr(i, "caption"):
                        caption = i.caption
                        action = i.action
                    else:
                        caption = i[0]
                        action = i[1]

                    wells_walkthrough_info = wells_walkthrough_get_info(items, i)

                textbutton caption:
                    action action
                    text_size (persistent.wells_choice_size if persistent.wells_choice_size is not None else gui.choice_button_text_size)
                    xalign 0.5
                    text_align 0.5
                    xminimum (persistent.wells_choice_width if persistent.wells_choice_width is not None else 920)
                    xmaximum (persistent.wells_choice_width if persistent.wells_choice_width is not None else 920)

                if wells_walkthrough_info:
                    text wells_walkthrough_info:
                        size wells_walkthrough_text_size(18)
                        xalign 0.5
                        text_align 0.5
                        color "#39ff14"
