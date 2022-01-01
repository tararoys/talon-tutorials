# These are active when we have focus on the tutorial_draft window
title: /next line/

mode: command
mode: dictation
-

settings():
  # Enable 'Smart dictation mode', see https://github.com/knausj85/knausj_talon/pull/356
  user.context_sensitive_dictation = 1

# Replace a single word with a phrase
replace <user.tutorial_draft_anchor> with <user.text>:
  user.tutorial_draft_select("{tutorial_draft_anchor}")
  result = user.formatted_text(text, "NOOP")
  insert(result)

# Position cursor before word
cursor <user.tutorial_draft_anchor>:
  user.tutorial_draft_position_caret("{tutorial_draft_anchor}")

cursor before <user.tutorial_draft_anchor>:
  user.tutorial_draft_position_caret("{tutorial_draft_anchor}")

# Position cursor after word
cursor after <user.tutorial_draft_anchor>:
  user.tutorial_draft_position_caret("{tutorial_draft_anchor}", 1)

# Select a whole word
select <user.tutorial_draft_anchor>:
  user.tutorial_draft_select("{tutorial_draft_anchor}")

# Select a range of words
select <user.tutorial_draft_anchor> through <user.tutorial_draft_anchor>:
  user.tutorial_draft_select("{tutorial_draft_anchor_1}", "{tutorial_draft_anchor_2}")

# Delete a word
clear <user.tutorial_draft_anchor>:
  user.tutorial_draft_select("{tutorial_draft_anchor}", "", 1)
  key(backspace)

# Delete a range of words
clear <user.tutorial_draft_anchor> through <user.tutorial_draft_anchor>:
  user.tutorial_draft_select(tutorial_draft_anchor_1, tutorial_draft_anchor_2, 1)
  key(backspace)

# reformat word
<user.formatters> word <user.tutorial_draft_anchor>:
  user.tutorial_draft_select("{tutorial_draft_anchor}", "", 1)
  user.formatters_reformat_selection(user.formatters)

# reformat range
<user.formatters> <user.tutorial_draft_anchor> through <user.tutorial_draft_anchor>:
    user.tutorial_draft_select(tutorial_draft_anchor_1, tutorial_draft_anchor_2, 1)
    user.formatters_reformat_selection(user.formatters)
