"""
Make mistletoe easier to import.
"""

__version__ = "0.10.0a1"
__all__ = [
    "renderers",
    "base_elements",
    "block_tokens",
    "block_tokenizer",
    "span_tokens",
    "span_tokenizer",
]

from mistletoe.block_tokens import Document
from mistletoe.renderers.base import BaseRenderer  # noqa: F401
from mistletoe.renderers.html import HTMLRenderer


def markdown(
    iterable, renderer=HTMLRenderer, init_token=Document, read_kwargs=None, **kwargs
):
    """
    Render text with a given renderer.

    :param iterable: string or list of strings
    :param init_token: The initial token to use for parsing the text `init_token.read`
    :param read_kwargs: key-word arguments to parse to the ``init_token.read`` method
    :param kwargs: key-word arguments to parse to the renderer initialisation
    """
    with renderer(**kwargs) as renderer:
        return renderer.render(init_token.read(iterable, **(read_kwargs or {})))
