# These are available when the tutorial_draft window is open, but not necessarily focussed
tag: user.tutorial_draft_window_showing

-
tutorial draft hide: user.tutorial_draft_hide()


over:

  sleep(100ms)
  text = user.tutorial_draft_get_text()
  yay = user.formatted_text(text, "CAPITALIZE_FIRST_WORD")
  user.tutorial_draft_hide()
  user.switcher_focus("Sublime Text")
  insert(yay)
  key(backspace)
  ":"
  key(enter)
  user.tutorial_draft_show()
  key(ctrl-a)
  key(backspace)

  # user.paste may be somewhat faster, but seems to be unreliable on MacOSX, see
  # https://github.com/talonvoice/talon/issues/254#issuecomment-789355238
  #user.paste(content)

  