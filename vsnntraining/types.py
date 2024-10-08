from dataclasses import dataclass
from typing import Any, Callable

from lvsfunc import clip_to_npy, get_random_frame_nums
from vsexprtools import norm_expr
from vskernels import Lanczos
from vstools import (
    CustomStrEnum, FormatsMismatchError, FunctionUtil, ResolutionsMismatchError, SPath,
    SPathLike, core, depth, vs
)

__all__: list[str] = [
    'TrainingPair',
    'OutputFormat'
]


class OutputFormat(CustomStrEnum):
    """Output format."""

    NPY = "npy"
    NPZ = "npz"
    PNG = "png"
    AVIF = "avif"

    @property
    def writer(self) -> Callable[[vs.VideoNode, Any], Any]:
        if self is OutputFormat.PNG and hasattr(core, 'fpng'):
            return lambda clip, **kwargs: core.fpng.Write(Lanczos.resample(clip, vs.RGB24), **kwargs)

        if self is OutputFormat.NPY:
            return lambda clip, **kwargs: clip_to_npy(clip, **kwargs)

        if self is OutputFormat.NPZ:
            return lambda clip, **kwargs: clip_to_npy(clip, export_npz=True, **kwargs)

        return lambda clip, **kwargs: clip.imwri.Write(clip, imgformat=self.value, **kwargs)


@dataclass
class TrainingPair:
    """Training pair."""

    ground_truth: vs.VideoNode
    """The ground truth video clip."""

    low_quality: vs.VideoNode
    """The low quality video clip."""

    def __post_init__(self):
        self._check_mismatches()

    def _check_mismatches(self):
        FormatsMismatchError.check(self, self.ground_truth, self.low_quality)
        ResolutionsMismatchError.check(self, self.ground_truth, self.low_quality)

    def prepare(self, output_fmt: OutputFormat = OutputFormat.NPY) -> None:
        """
        Prepare the training set for export.

        We normalize the clips to a range of 0-1 by increasing the chroma planes's pixel values by 0.5.
        This will make it look noticeably different for us, but supposedly greatly simplifies the training process.
        """

        func_gt = FunctionUtil(self.ground_truth, self.prepare, None, (vs.GRAY, vs.YUV), 32)
        func_lq = FunctionUtil(self.low_quality, self.prepare, None, (vs.GRAY, vs.YUV), 32)

        if not func_gt.chroma_planes:
            return

        if output_fmt is OutputFormat.PNG:
            self.ground_truth = depth(func_gt.work_clip, 8)
            self.low_quality = depth(func_lq.work_clip, 8)
        elif output_fmt is OutputFormat.NPY:
            self.ground_truth = norm_expr(func_gt.work_clip, 'x 0.5 +', func_gt.chroma_planes)
            self.low_quality = norm_expr(func_lq.work_clip, 'x 0.5 +', func_lq.chroma_planes)

    def pick_random_frames(self, interval: int = 24) -> None:
        """Pick random frames from the training pair."""

        frames_nums = get_random_frame_nums(self.ground_truth, interval)

        self.ground_truth = core.std.Splice([self.ground_truth[num] for num in frames_nums])
        self.low_quality = core.std.Splice([self.low_quality[num] for num in frames_nums])

    def create_dirs(self, base_dir: SPathLike) -> None:
        """Create directories for the training pair."""

        out_dir = SPath(base_dir)

        self.lq_dir = out_dir / "lq"
        self.gt_dir = out_dir / "gt"

        self.lq_dir.mkdir(511, True, True)
        self.gt_dir.mkdir(511, True, True)
