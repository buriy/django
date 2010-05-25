"""
Sets up the terminal color scheme.
"""

import os
import sys

from django.utils import termcolors

console_stdout = sys.stdout
console_stderr = sys.stderr

def pyreadline_console_patch():
    try:
        import pyreadline
        global console_stdout
        global console_stderr
        # isatty is not always implemented, #6223.
        if hasattr(sys.stdout, 'isatty') and sys.stdout.isatty():    
            console_stdout = sys.stdout
            sys.stdout = pyreadline.console.Console()
            sys.stdout.closed = False
        if hasattr(sys.stderr, 'isatty') and sys.stderr.isatty():
            console_stderr = sys.stderr
            sys.stderr = pyreadline.console.Console()
            sys.stderr.closed = False
        return True
    except ImportError:
        return False

def supports_color():
    """
    Returns True if the running system's terminal supports color, and False
    otherwise.
    """
    unsupported_platform = (sys.platform in ('win32', 'Pocket PC'))

    if unsupported_platform:
        if type(sys.stdout) is file: # if console is not patched yet
            if pyreadline_console_patch():
                unsupported_platform = False
        else:
            unsupported_platform = False
    # isatty is not always implemented, #6223.
    is_a_tty = hasattr(sys.stdout, 'isatty') and sys.stdout.isatty()
    if unsupported_platform or not is_a_tty:
        return False
    return True

def color_style():
    """Returns a Style object with the Django color scheme."""
    if not supports_color():
        style = no_style()
    else:
        DJANGO_COLORS = os.environ.get('DJANGO_COLORS', '')
        color_settings = termcolors.parse_color_setting(DJANGO_COLORS)
        if color_settings:
            class dummy: pass
            style = dummy()
            # The nocolor palette has all available roles.
            # Use that pallete as the basis for populating
            # the palette as defined in the environment.
            for role in termcolors.PALETTES[termcolors.NOCOLOR_PALETTE]:
                format = color_settings.get(role,{})
                setattr(style, role, termcolors.make_style(**format))
            # For backwards compatibility,
            # set style for ERROR_OUTPUT == ERROR
            style.ERROR_OUTPUT = style.ERROR
        else:
            style = no_style()
    return style

def no_style():
    """Returns a Style object that has no colors."""
    class dummy:
        def __getattr__(self, attr):
            return lambda x: x
    return dummy()
