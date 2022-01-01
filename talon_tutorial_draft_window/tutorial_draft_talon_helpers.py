from typing import Optional
from talon import ui, settings, Module, Context, actions
from .tutorial_draft_ui import DraftManager

mod = Module()

# ctx is for toggling the tutorial_draft_window_showing variable
# which lets you execute actions whenever the window is visible.
ctx = Context()

# ctx_focused is active only when the tutorial_draft window is focussed. This
# lets you execute actions under that condition.
ctx_focused = Context()
ctx_focused.matches = r"""
title: /Talon Tutorial Draft/
"""

mod.tag("tutorial_draft_window_showing", desc="Tag set when tutorial_draft window showing")
setting_theme = mod.setting(
    "tutorial_draft_window_theme",
    type=str,
    default="dark",
    desc="Sets the main colors of the window, one of 'dark' or 'light'",
)
setting_label_size = mod.setting(
    "tutorial_draft_window_label_size",
    type=int,
    default=40,
    desc="Sets the size of the word labels used in the tutorial_draft window",
)
setting_label_color = mod.setting(
    "tutorial_draft_window_label_color",
    type=str,
    default=None,
    desc=(
        "Sets the color of the word labels used in the tutorial_draft window. "
        "E.g. 00ff00 would be green"
    ),
)
setting_text_size = mod.setting(
    "tutorial_draft_window_text_size",
    type=int,
    default=40,
    desc="Sets the size of the text used in the tutorial_draft window",
)


tutorial_draft_manager = DraftManager()

# Update the styling of the tutorial_draft window dynamically as user settings change
def _update_tutorial_draft_style(*args):
    tutorial_draft_manager.set_styling(
        **{
            arg: setting.get()
            for setting, arg in (
                (setting_theme, "theme"),
                (setting_label_size, "label_size"),
                (setting_label_color, "label_color"),
                (setting_text_size, "text_size"),
            )
        }
    )


settings.register("", _update_tutorial_draft_style)


@ctx_focused.action_class("user")
class ContextSensitiveDictationActions:
    """
    Override these actions to assist 'Smart dictation mode'.
    see https://github.com/knausj85/knausj_talon/pull/356
    """

    def dictation_peek_left(clobber=False):
        area = tutorial_draft_manager.area
        return area[max(0, area.sel.left - 50) : area.sel.left]

    def dictation_peek_right():
        area = tutorial_draft_manager.area
        return area[area.sel.right : area.sel.right + 50]

    def paste(text: str):
        # todo: remove once user.paste works reliably with the tutorial_draft window
        actions.insert(text)


@ctx_focused.action_class("edit")
class EditActions:
    """
    Make default edit actions more efficient.
    """

    def selected_text() -> str:
        area = tutorial_draft_manager.area
        if area.sel:
            result = area[area.sel.left : area.sel.right]
            return result
        return ""


from talon import cron


class UndoWorkaround:
    """
    Workaround for the experimental textarea's undo being character by character.
    This keeps a debounced undo history. Can be deleted once this todo item is
    fixed: https://github.com/talonvoice/talon/issues/254#issuecomment-789149734
    """

    # Set this to False if you want to turn it off, or just delete all references
    # to this class
    enable_workaround = True

    # Stack of (text_value, selection) tuples representing the undo stack
    undo_stack = []
    # Stack of (text_value, selection) tuples representing the redo stack
    redo_stack = []
    # Used by the timer to check when the text has stopped changing
    pending_undo = None

    # timer handle
    timer_handle = None

    @classmethod
    def start_logger(cls, reset_undo_stack: bool):
        if reset_undo_stack:
            cls.undo_stack = []
            cls.redo_stack = []

        cls.stop_logger()
        cls.timer_handle = cron.interval("500ms", cls._log_changes)

    @classmethod
    def stop_logger(cls):
        if cls.timer_handle is not None:
            cron.cancel(cls.timer_handle)
        cls.timer_handle = None
        cls.pending_undo = None

    @classmethod
    def perform_undo(cls):
        if len(cls.undo_stack) == 0:
            return

        curr_text = tutorial_draft_manager.area.value
        curr_sel = (tutorial_draft_manager.area.sel.left, tutorial_draft_manager.area.sel.right)
        text, sel = cls.undo_stack[-1]
        if text == curr_text:
            cls.undo_stack.pop()
            if len(cls.undo_stack) == 0:
                return

            # Most of the time (unless user has only just finished updating) the
            # top of the stack will have the same contents as the text area. In
            # this case pop again to get a bit lower. We should never have the
            # same text twice, hence we don't need a loop.
            text, sel = cls.undo_stack[-1]

        # Remember the current state in the redo stack
        cls.redo_stack.append((curr_text, curr_sel))
        tutorial_draft_manager.area.value = text
        tutorial_draft_manager.area.sel = sel

        cls.pending_undo = (text, sel)

    @classmethod
    def perform_redo(cls):
        if len(cls.redo_stack) == 0:
            return

        text, sel = cls.redo_stack.pop()

        tutorial_draft_manager.area.value = text
        tutorial_draft_manager.area.sel = sel

        cls.pending_undo = (text, sel)
        cls.undo_stack.append((text, sel))

    @classmethod
    def _log_changes(cls):
        """
        If the text and cursor position hasn't changed for two interval iterations
        (1s) and the undo stack doesn't match the current state, then add to the stack.
        """

        curr_val = tutorial_draft_manager.area.value
        # Turn the Span into a tuple, because we can't == Spans
        curr_sel = (tutorial_draft_manager.area.sel.left, tutorial_draft_manager.area.sel.right)
        curr_state = (curr_val, curr_sel)

        state_stack_mismatch = (
            len(cls.undo_stack) == 0
            or
            # Only want to update the undo stack if the value has changed, not just
            # the selection
            curr_state[0] != cls.undo_stack[-1][0]
        )

        if cls.pending_undo == curr_state and state_stack_mismatch:
            cls.undo_stack.append(curr_state)
            # Clear out the redo stack because we've changed the text
            cls.redo_stack = []
        elif cls.pending_undo != curr_state:
            cls.pending_undo = curr_state
        elif not state_stack_mismatch and len(cls.undo_stack) > 0:
            # Remember the cursor position in the undo stack for the current text value
            cls.undo_stack[-1] = (cls.undo_stack[-1][0], curr_sel)
        else:
            # The text area text is not changing, do nothing
            pass


if UndoWorkaround.enable_workaround:
    ctx_focused.action("edit.undo")(UndoWorkaround.perform_undo)
    ctx_focused.action("edit.redo")(UndoWorkaround.perform_redo)


@mod.action_class
class Actions:
    def tutorial_draft_show(text: Optional[str] = None):
        """
        Shows tutorial_draft window
        """

        tutorial_draft_manager.show(text)
        UndoWorkaround.start_logger(text is not None)
        ctx.tags = ["user.tutorial_draft_window_showing"]

    def tutorial_draft_hide():
        """
        Hides tutorial_draft window
        """

        tutorial_draft_manager.hide()
        UndoWorkaround.stop_logger()
        ctx.tags = []

    def tutorial_draft_select(
        start_anchor: str, end_anchor: str = "", include_trailing_whitespace: int = 0
    ):
        """
        Selects text in the tutorial_draft window
        """

        tutorial_draft_manager.select_text(
            start_anchor,
            end_anchor=None if end_anchor == "" else end_anchor,
            include_trailing_whitespace=include_trailing_whitespace == 1,
        )

    def tutorial_draft_position_caret(anchor: str, after: int = 0):
        """
        Positions the caret in the tutorial_draft window
        """

        tutorial_draft_manager.position_caret(anchor, after=after == 1)

    def tutorial_draft_get_text() -> str:
        """
        Returns the text in the tutorial_draft window
        """

        return tutorial_draft_manager.get_text()

    def tutorial_draft_select_text() -> str:
        """
        Returns the text in the tutorial_draft window
        """

        return tutorial_draft_manager.select_text()


    def tutorial_draft_resize(width: int, height: int):
        """
        Resize the tutorial_draft window.
        """

        tutorial_draft_manager.reposition(width=width, height=height)

    def tutorial_draft_named_move(name: str, screen_number: Optional[int] = None):
        """
        Lets you move the window to the top, bottom, left, right, or middle
        of the screen.
        """

        screen = ui.screens()[screen_number or 0]
        window_rect = tutorial_draft_manager.get_rect()
        xpos = (screen.width - window_rect.width) / 2
        ypos = (screen.height - window_rect.height) / 2

        if name == "top":
            ypos = 0
        elif name == "bottom":
            ypos = screen.height - window_rect.height - 0
        elif name == "left":
            xpos = 0
        elif name == "right":
            xpos = screen.width - window_rect.width - 0
        elif name == "middle":
            # That's the default values
            pass

        # Adjust for the fact that the screen may not be at 0,0.
        xpos += screen.x
        ypos += screen.y
        tutorial_draft_manager.reposition(xpos=xpos, ypos=ypos)


# Some capture groups we need


@mod.capture(rule="{self.letter}+")
def tutorial_draft_anchor(m) -> str:
    """
    An anchor (string of letters)
    """
    return "".join(m)


@mod.capture(rule="(top|bottom|left|right|middle)")
def tutorial_draft_window_position(m) -> str:
    """
    One of the named positions you can move the window to
    """

    return "".join(m)
