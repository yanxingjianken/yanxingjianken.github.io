---
title: "CorrDiff Notes"
collection: modeling
type: "Notes for Running CorrDiff on DOlma"
permalink: /teaching/CorrDiff
venue: "MIT EAPS"
date: 2025-10-14
location: "Cambridge, MA"
---

Notes for building everything CorrDiff from [this tutorial](https://github.com/NVIDIA/physicsnemo/tree/main/examples/weather/corrdiff).

## Running Example

```bash
# Storage check (choose data2)
df -h | egrep '(/net/flood/data|/net/flood/data2)'

# Clone
cd /net/flood/data2/users/x_yan
git clone https://github.com/NVIDIA/physicsnemo.git
cd physicsnemo/examples/weather/corrdiff

# Env
module purge
conda create -y -p ./corrdiff-env python=3.10
source activate /net/flood/data2/users/x_yan/physicsnemo/examples/weather/corrdiff/corrdiff-env
export PYTHONNOUSERSITE=1
unset PIP_REQUIRE_VIRTUALENV
python -m pip install --upgrade pip wheel

# PyTorch CUDA 12.1 wheels (driver 535 works)
python -m pip install --index-url https://download.pytorch.org/whl/cu121 torch torchvision
python - <<'PY'
import torch; print("CUDA available:", torch.cuda.is_available(), "CUDA:", torch.version.cuda)
PY

# PhysicsNeMo + example deps + runtime fixes
python -m pip install 'nvidia-physicsnemo[all]'
python -m pip install -r requirements.txt
python -m pip install tensorboard einops
python -m pip install 'coverage==7.6.1'

# NGC CLI install
mkdir -p ~/ngc && cd ~/ngc
wget --content-disposition \
  https://api.ngc.nvidia.com/v2/resources/nvidia/ngc-apps/ngc_cli/versions/3.64.1/files/ngccli_linux.zip \
  -O ngccli_linux.zip
unzip -o ngccli_linux.zip -d ./
chmod u+x ngc-cli/ngc
echo 'export PATH="$PATH:$HOME/ngc/ngc-cli"' >> ~/.bashrc
source ~/.bashrc
ngc --version
ngc config set

# HRRR-Mini dataset
DEST=/net/flood/data2/users/x_yan/physicsnemo/examples/weather/corrdiff/data/HRRR-Mini
mkdir -p "$DEST"
ngc registry resource download-version "nvidia/modulus/modulus_datasets-hrrr_mini:1" --dest "$DEST"

# Train (regression)
cd /net/flood/data2/users/x_yan/physicsnemo/examples/weather/corrdiff
DATA="$DEST/modulus_datasets-hrrr_mini_v1/hrrr_mini/hrrr_mini_train.nc"
STATS="$DEST/modulus_datasets-hrrr_mini_v1/hrrr_mini/stats.json"
export OMP_NUM_THREADS=8 MKL_NUM_THREADS=8
python train.py --config-name=config_training_hrrr_mini_regression.yaml \
  ++dataset.data_path="$DATA" \
  ++dataset.stats_path="$STATS"

# (Later) Train diffusion
REG_CKPT="/net/flood/data2/users/x_yan/physicsnemo/examples/weather/corrdiff/checkpoints_regression/checkpoint.0.5120.pt"
python train.py --config-name=config_training_hrrr_mini_diffusion.yaml \
  ++training.io.regression_checkpoint_path="$REG_CKPT" \
  ++dataset.data_path="$DATA" \
  ++dataset.stats_path="$STATS"

# (Optional) Generate
python generate.py --config-name=config_generate_hrrr_mini.yaml \
  ++generation.io.res_ckpt_filename=/path/to/diffusion_checkpoint.mdlus \
  ++generation.io.reg_ckpt_filename="$REG_CKPT"
```

## Train With Customized Dataset
