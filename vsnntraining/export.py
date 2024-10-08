from lvsfunc import ExportFrames, clip_to_npy
from vstools import SPath, SPathLike

from .types import OutputFormat, TrainingPair

__all__: list[str] = [
    'export_training_pair',
]


def export_training_pair(
    training_pair: TrainingPair,
    out_dir: SPathLike = 'bin/',
    interval: int = 24,
    output_fmt: OutputFormat = OutputFormat.NPY
) -> tuple[list[SPath], list[SPath]]:

    training_pair.prepare(output_fmt)

    if interval > 1:
        training_pair.pick_random_frames(interval)

    training_pair.create_dirs(out_dir)

    if output_fmt is OutputFormat.NPY:
        return (
            clip_to_npy(training_pair.low_quality, training_pair.lq_dir),
            clip_to_npy(training_pair.ground_truth, training_pair.gt_dir)
        )

    export_func = ExportFrames.from_param(output_fmt.value)

    assert export_func is not None, f'Invalid output format: {output_fmt}'

    return (
        export_func(training_pair.low_quality, training_pair.lq_dir / '%d.png'),
        export_func(training_pair.ground_truth, training_pair.gt_dir / '%d.png')
    )
