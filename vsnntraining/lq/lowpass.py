from vstools import CustomNotImplementedError, vs

__all__: list[str] = [
    'horizontal_dvd_lowpass',
    'hdcam_lowpass',
    'hdcam_jc_lowpass',
    'hd_downscale_dvd',
]


def horizontal_dvd_lowpass(clip: vs.VideoNode, taps: float = 4) -> vs.VideoNode:
    """
    LQ function for a model to fix horizontal lowpass filtering applied to DVD masters.

    Attempt to match the lowpassing applied to SD DVD masters during authoring.
    In an ideal scenario, you would merge the frequencies that were lowpassed from
    a non-lowpassed source, but that may not always be possible.

    Example of fixing horizontal lowpass filtering: https://slow.pics/c/KscN4dZ9

    :param clip:        High-quality source clip.

    :return:            Low-quality output clip.
    """

    # https://discord.com/channels/1168547111139283026/1168591691402444902/1205161117542907905
    mangle = clip.fmtc.resample(864, kernel="lanczos", taps=taps, fh=1 / 1.5)
    mangle = mangle.fmtc.resample(clip.width, kernel="lanczos", taps=taps, fh=1 / 1.25)

    return mangle


def hdcam_lowpass(clip: vs.VideoNode) -> vs.VideoNode:
    """
    LQ function for a model to fix HDCAM master sources.

    Attempt to match the lowpassing applied to HDCAM master sources.
    Clean sources will basically never exist, and the lowpass filter
    is incredibly destructive to the image.

    :param clip:        High-quality source clip.

    :return:            Low-quality output clip.
    """

    raise CustomNotImplementedError(None, hdcam_lowpass)


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
