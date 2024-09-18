from vstools import (FieldBased, FieldBasedT, FunctionUtil,
                     UnsupportedFieldBasedError, core, get_lowest_values,
                     get_neutral_value, vs)

__all__: list[str] = [
    'field_inpainting',
]


def field_inpainting(clip: vs.VideoNode, field_based: FieldBasedT | None = None) -> vs.VideoNode:
    """
    LQ function for a model that uses field inpainting to deinterlace spatially.

    For some sources, Nnedi3 and Eedi3 aren't good enough.
    Field inpainting is a good alternative for those.

    The weakness is the same as Nnedi3/Eedi3: there is no temporal processing.
    This could potentially be fixed with a new type of model,
    or by adding this as a spatial deinterlacer for QTGMC or similar.

    :param clip:            High-quality source clip.
    :param field_based:     The field-based parameter for the field order.
                            True for TFF, False for BFF, None for auto.
                            Default: None.

    :return:                Low-quality output clip.
    """

    func = FunctionUtil(clip, field_inpainting, None, vs.YUV)

    field_based = FieldBased.from_param_or_video(field_based, func.work_clip, func_except=func.func)

    if not field_based.is_inter:
        raise UnsupportedFieldBasedError("You must set the `field_based` parameter!", func.func)

    sep = func.work_clip.std.SeparateFields(field_based.is_tff)

    green = sep.std.BlankClip(
        color=[get_neutral_value(func.work_clip), *get_lowest_values(func.work_clip)[1:]], keep=True
    )

    woven = core.std.Interleave([sep, green]).std.DoubleWeave(field_based.is_tff)[::4]

    return func.return_clip(woven)
