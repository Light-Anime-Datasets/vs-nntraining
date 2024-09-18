from dataclasses import dataclass
from typing import Any, Callable

from lvsfunc import clip_to_npy, get_random_frame_nums, prepare_clip_for_npy
from vstools import (CustomStrEnum, FormatsMismatchError,
                     ResolutionsMismatchError, SPath, SPathLike, core, vs)

__all__: list[str] = [
    'TrainingPair',
    'OutputFormat'
]


class OutputFormat(CustomStrEnum):
    """Output format."""

    NPY = "npy"
    PNG = "png"
    AVIF = "avif"

    @property
    def writer(self) -> Callable[[vs.VideoNode, Any], Any]:
        if self is OutputFormat.PNG and hasattr(core, 'fpng'):
            return lambda clip, **kwargs: core.fpng.Write(clip, **kwargs)

        if self is OutputFormat.NPY:
            return lambda clip, **kwargs: clip_to_npy(clip, **kwargs)

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

    def prepare(self, output_fmt: 'OutputFormat' = OutputFormat.NPY) -> None:
        """Prepare the training set for export."""

        if output_fmt is not OutputFormat.NPY:
            return

        self.ground_truth = prepare_clip_for_npy(self.ground_truth)
        self.low_quality = prepare_clip_for_npy(self.low_quality)

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
