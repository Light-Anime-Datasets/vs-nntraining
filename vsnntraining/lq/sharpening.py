from typing import Any

from vstools import vs

__all__: list[str] = [
    'deunsharpening',
]


def deunsharpening(clip: vs.VideoNode, **kwargs: Any) -> vs.VideoNode:
    """
    LQ function for a model that attempts to undo unsharpening.

    Many modern sources are sharpened to the point where regular dehaloing methods are insufficient.
    This is because they often miss areas where the image was sharpened, and also don't properly deal with
    the line darkening that comes with unsharpening.

    :param clip:        High-quality source clip.
    :param kwargs:      Keyword arguments to pass to unsharp_masked.

    :return:            Low-quality output clip.
    """

    from vsrgtools import unsharp_masked

    return unsharp_masked(clip, **kwargs)
