from typing import Any, Literal

from stgpytools import FuncExceptT
from vstools import CustomNotImplementedError, CustomValueError, core, fallback, vs

__all__: list[str] = [
    'horizontal_dvd_lowpass',
    'hdcam_lowpass',
    'hdcam_jc_lowpass',
    'hd_downscale_dvd',
]


def _prepare_params(
    taps: float | list[float],
    fh: float | list[float] | None | Literal[False] = None,
    fv: float | list[float] | None | Literal[False] = None,
    func_except: FuncExceptT | None = None
) -> dict[str, list[float] | None]:

    func = fallback(func_except, 'lowpass')

    if fh is None and fv is None:
        raise CustomValueError("Either fh or fv must be set!", func)

    taps_list = [taps] if isinstance(taps, (int, float)) else taps

    if fh is False and fv is False:
        return dict(taps=taps_list, fh=None, fv=None)

    fh_list = [fh] if fh is not False and not isinstance(fh, list) else fh
    fv_list = [fv] if fv is not False and not isinstance(fv, list) else fv

    if fh_list and fv_list and len(fh_list) != len(fv_list):
        raise CustomValueError("fh and fv must have the same length!", func)

    max_length = max(len(x) for x in (fh_list, fv_list) if x and x is not False) if fh_list or fv_list else 1

    taps_final = taps_list * max_length if len(taps_list) == 1 else taps_list

    if len(taps_final) < max_length:
        raise CustomValueError("taps list is too short to match fh or fv length!", func)

    fh_final = fh_list * max_length if fh_list and len(fh_list) == 1 else fh_list if fh_list else None
    fv_final = fv_list * max_length if fv_list and len(fv_list) == 1 else fv_list if fv_list else None

    return dict(
        taps=taps_final[:max_length],
        fh=fh_final,
        fv=fv_final
    )


def horizontal_dvd_lowpass(
    clip: vs.VideoNode,
    taps: float = 4,
    fh: float | list[float] = [1 / 1.25, 1 / 1.375]
) -> vs.VideoNode:
    """
    LQ function for a model to fix horizontal lowpass filtering applied to DVD masters.

    Attempt to match the lowpassing applied to SD DVD masters during authoring.
    In an ideal scenario, you would merge the frequencies that were lowpassed from
    a non-lowpassed source, but that may not always be possible.

    Example of fixing horizontal lowpass filtering: https://slow.pics/c/KscN4dZ9

    :param clip:        High-quality source clip.
    :param taps:        Number of taps for the Lanczos kernel. Default is 4.
    :param fh:          Horizontal frequency cutoff. Can be a single float or a list of floats.
                        Default: [1 / 1.25, 1 / 1.375].

    :return:            Low-quality output clip.
    """

    params = _prepare_params(taps=[taps, taps], fh=fh, fv=False)

    return clip.fmtc.resample(kernel="lanczos", **params)


def hdcam_lowpass(clip: vs.VideoNode, taps: float = 8, fh: float | list[float] = [1 / 1.25, 1 / 1.375]) -> vs.VideoNode:
    """
    LQ function for a model to fix HDCAM master sources.

    Attempt to match the lowpassing applied to HDCAM master sources.
    Clean sources will basically never exist, and the lowpass filter
    is incredibly destructive to the image.

    :param clip:        High-quality source clip.
    :param taps:        Number of taps for the Lanczos kernel. Default is 8.

    :return:            Low-quality output clip.
    """

    params = _prepare_params(taps=taps, fh=fh, fv=False)

    return clip.fmtc.resample(kernel="lanczos", **params)


def hdcam_jc_lowpass(clip: vs.VideoNode) -> vs.VideoNode:
    """
    LQ function for a model to fix HDCAM master sources from J.C. Staff.

    Attempt to match the lowpassing applied to HDCAM master sources from J.C. Staff.
    Their HDCAM process appears to be different to the point where
    a regular HDCAM function wouldn't match it very well.

    :param clip:        High-quality source clip.

    :return:            Low-quality output clip.
    """

    raise CustomNotImplementedError(None, hdcam_jc_lowpass)


def hd_downscale_dvd(clip: vs.VideoNode) -> vs.VideoNode:
    """
    LQ function for a model to improve HD sources that are downscaled to DVD resolution.

    HD sources that are downscaled to DVD resolution often have very strong lowpassing applied to them.
    This is particularly unfortunate when the only decent source available is the DVD.

    :param clip:        High-quality source clip.

    :return:            Low-quality output clip.
    """

    raise CustomNotImplementedError(None, hd_downscale_dvd)
