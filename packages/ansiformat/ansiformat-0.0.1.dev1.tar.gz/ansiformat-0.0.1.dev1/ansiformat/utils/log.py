"""Logging utility and helper functions."""
import traceback

ESCAPE_TRANSLATION_TABLE = {
    ord('"'): r'\"',
    ord('\n'): r'\\n',
    ord('\r'): r'\\r',
    ord('\t'): r'\\t'
}
