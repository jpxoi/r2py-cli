"""
Colors module for R2Py CLI.

This module defines the Colors class, which is used to color the terminal output.
"""

class Colors:
    """ANSI escape sequence colors for terminal output."""
    HEADER     = '\033[95m'
    OKBLUE     = '\033[94m'
    OKCYAN     = '\033[96m'
    OKGREEN    = '\033[92m'
    WARNING    = '\033[93m'
    FAIL       = '\033[91m'
    ENDC       = '\033[0m'
    BOLD       = '\033[1m'
    UNDERLINE  = '\033[4m'
    ERROR      = '\033[31m'     # Red (normal)
    CRITICAL   = '\033[1;31m'   # Bold Red
    RESET      = ENDC

    @classmethod
    def colorize(cls, text: str, color: str) -> str:
        """
        Wrap text with the given color.
        Args:
            text (str): The text to colorize.
            color (str): The color attribute name (e.g., 'OKBLUE', 'FAIL').
        Returns:
            str: Colored text.
        """
        color_code = cls.get_color_code(color)
        return f"{color_code}{text}{cls.ENDC}"

    @classmethod
    def colorize_bold(cls, text: str, color: str) -> str:
        """
        Wrap text with the given color and bold.
        """
        color_code = cls.get_color_code(color)
        return f"{color_code}{cls.BOLD}{text}{cls.ENDC}"

    @classmethod
    def colorize_underline(cls, text: str, color: str) -> str:
        """
        Wrap text with the given color and underline.
        """
        color_code = cls.get_color_code(color)
        return f"{color_code}{cls.UNDERLINE}{text}{cls.ENDC}"

    @classmethod
    def get_color_code(cls, color: str) -> str:
        """
        Get the color code for the given color name.
        Args:
            color (str): The color attribute name (e.g., 'OKBLUE', 'FAIL').
        Returns:
            str: Color code.
        """
        return getattr(cls, color, cls.ENDC)
