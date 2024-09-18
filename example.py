from lvsfunc import npy_to_clip
from vssource import source
from vstools import set_output

from vsnntraining import OutputFormat, TrainingPair, export_training_pair, fix_offset
from vsnntraining.lq import field_inpainting

# Import clip.
gt = source("RANDOM/VIDEO.mkv")

# Apply one of the lq filters. This can just be in-line code if you write your own lq filter.
lq = field_inpainting(gt, field_based=True)

# Create a training pair
pair = TrainingPair(gt, lq)

# Export to "field_inpainting" directory with a random frame every 12 frames. We export as npy files.
export_training_pair(pair, "bin/field_inpainting", interval=12, output_fmt=OutputFormat.NPY)

# Output from terminal for illustrative purposes (you do not need to include this in your script)
r"""
Dumping numpy arrays to bin\field_inpainting\lq...: 100%|██| 181/181 [00:01<00:00, 160.08frame/s, Current file=00181.npy
Dumping numpy arrays to bin\field_inpainting\gt...: 100%|██| 181/181 [00:01<00:00, 158.68frame/s, Current file=00181.npy
"""

# You can verify if the data was actually output correctly by reading it back in.
lq = npy_to_clip("bin/field_inpainting/lq/")
gt = npy_to_clip("bin/field_inpainting/gt/")

# Because we normalize the clip, we have to fix the offsets.
lq = fix_offset(lq)
gt = fix_offset(gt)

# LQ output was TFF, so we reapply that.
lq = lq.std.SetFieldBased(2)

set_output(gt, name="Ground truth")
set_output(lq, name="Low quality")
