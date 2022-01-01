# These are available globally (in command mode)
mode: command
-
^tutorial draft show:
    # Do this toggle so we can have focus when saying 'tutorial_draft show'
    user.tutorial_draft_hide()
    user.tutorial_draft_show()
    user.tutorial_draft_resize(1000, 400)

^tutorial draft show <user.tutorial_draft_window_position>:
    # Do this toggle so we can have focus when saying 'tutorial_draft show'
    user.tutorial_draft_hide()
    user.tutorial_draft_show()
    user.tutorial_draft_named_move(tutorial_draft_window_position)

^tutorial draft show small:
    # Do this toggle so we can have focus when saying 'tutorial_draft show'
    user.tutorial_draft_hide()
    user.tutorial_draft_show()
    user.tutorial_draft_resize(1000, 400)

^tutorial draft show large:
    # Do this toggle so we can have focus when saying 'tutorial_draft show'
    user.tutorial_draft_hide()
    user.tutorial_draft_show()
    user.tutorial_draft_resize(1000, 600t)

^tutorial draft empty: user.tutorial_draft_show("")

^tutorial draft edit:
    text = edit.selected_text()
    key(backspace)
    user.tutorial_draft_show(text)

^tutorial draft edit all:
    edit.select_all()
    text = edit.selected_text()
    key(backspace)
    user.tutorial_draft_show(text)
