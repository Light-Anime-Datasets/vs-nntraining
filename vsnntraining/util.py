from vsexprtools import norm_expr
from vstools import FunctionUtil, vs

__all__: list[str] = [
    'fix_offset',
]


def fix_offset(clip: vs.VideoNode) -> vs.VideoNode:
    """
    Fix the offset of the clip.

    This is necessary because the clips are normalized to a range of 0-1 when we prepare it for export.
    """

    func = FunctionUtil(clip, fix_offset, None, (vs.GRAY, vs.YUV), 32)

    if not func.chroma_planes:
        return func.work_clip

    return norm_expr(func.work_clip, 'x 0.5 -', func.chroma_planes)
