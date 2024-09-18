from vstools import CustomNotImplementedError, vs

__all__: list[str] = [
    'dempeg2',
    'deh264',
    'deh265',
    'devp9',
    'debink',
]


def dempeg2(clip: vs.VideoNode, mbps: float = 5.0) -> vs.VideoNode:
    """
    LQ function for a model to deal with mpeg2 compression noise.

    A lot of DVDs are encoded with mpeg2, and are plagued by compression noise.
    Often no alternative sources exist, or the alternatives are worse in other ways.

    Of special note is that to best represent DVD compression,
    we should encode the video at specific bitrates (matching the original compression),
    as well as encode them as interlaced.

    :param clip:        High-quality source clip.
    :param mbps:        Bitrate of the original compression in Mbps.
                        Default: 5.0.

    :return:            Low-quality output clip.
    """

    raise CustomNotImplementedError(None, dempeg2)


def deh264(clip: vs.VideoNode, mbps: float = 8.0) -> vs.VideoNode:
    """
    LQ function for a model to deal with h264 compression noise.

    Mostly useful for when you're stuck with different, bad rips from streaming services
    or old h264 BD encodes or something.

    :param clip:        High-quality source clip.
    :param mbps:        Bitrate of the original compression in Mbps.
                        Default: 8.0.

    :return:            Low-quality output clip.
    """

    raise CustomNotImplementedError(None, deh264)


def deh265(clip: vs.VideoNode, mbps: float = 10.0) -> vs.VideoNode:
    """
    LQ function for a model to deal with h265 compression noise.

    Mostly useful for when you're stuck with different, bad rips from streaming services.

    :param clip:        High-quality source clip.
    :param mbps:        Bitrate of the original compression in Mbps.
                        Default: 8.0.

    :return:            Low-quality output clip.
    """

    raise CustomNotImplementedError(None, deh265)


def devp9(clip: vs.VideoNode, mbps: float = 10.0) -> vs.VideoNode:
    """
    LQ function for a model to deal with vp9 compression noise.

    Mostly useful for when you're stuck with different, bad rips from YouTube or something.

    :param clip:        High-quality source clip.
    :param mbps:        Bitrate of the original compression in Mbps.
                        Default: 8.0.

    :return:            Low-quality output clip.
    """

    raise CustomNotImplementedError(None, devp9)


def debink(clip: vs.VideoNode, mbps: float = 10.0) -> vs.VideoNode:
    """
    LQ function for a model to deal with bink compression.

    Basically only useful for bad game video rips.

    :param clip:        High-quality source clip.
    :param mbps:        Bitrate of the original compression in Mbps.
                        Default: 10.0.

    :return:            Low-quality output clip.
    """

    raise CustomNotImplementedError(None, debink)

    raise CustomNotImplementedError(None, debink)
