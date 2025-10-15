---
title: "CorrDiff Notes"
collection: modeling
type: "Notes for Running CorrDiff on Dolma"
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
# pick the latest regression module archive
REG_MDLUS=$(ls -1t checkpoints_regression/UNet.*.mdlus | head -n1)
echo "$REG_MDLUS"
# e.g. /net/flood/.../corrdiff/checkpoints_regression/UNet.0.2000128.mdlus

# then launch diffusion with the .mdlus
python train.py --config-name=config_training_hrrr_mini_diffusion.yaml \
  ++training.io.regression_checkpoint_path="$REG_MDLUS" \
  ++dataset.data_path="$DATA" \
  ++dataset.stats_path="$STATS"

# Generate
# From: /net/flood/data2/users/x_yan/physicsnemo/examples/weather/corrdiff
# 1) Pick the latest packaged modules (.mdlus)
REG_MDLUS=$(ls -1t checkpoints_regression/*.mdlus | head -n1)
RES_MDLUS=$(ls -1t checkpoints_diffusion/*.mdlus | head -n1)   # run AFTER diffusion finishes

echo "REG_MDLUS=$REG_MDLUS"
echo "RES_MDLUS=$RES_MDLUS"

# 2) (optional) sanity that they’re valid tar archives
tar -tf "$REG_MDLUS" >/dev/null && echo "reg ok"
tar -tf "$RES_MDLUS" >/dev/null && echo "res ok"

# 3) Run generation with .mdlus files (NOT .pt)
python generate.py --config-name=config_generate_hrrr_mini.yaml \
  ++generation.io.res_ckpt_filename="$RES_MDLUS" \
  ++generation.io.reg_ckpt_filename="$REG_MDLUS" \
  ++dataset.data_path="$DATA" \
  ++dataset.stats_path="$STATS"

```

## Train With Customized Dataset

```bash
# =========================
# 0) Activate the CorrDiff env
# =========================
source activate /net/flood/data2/users/x_yan/physicsnemo/examples/weather/corrdiff/corrdiff-env

# (optional sanity)
python - <<'PY'
import torch; print("CUDA available:", torch.cuda.is_available(), "CUDA:", torch.version.cuda)
PY

# =========================
# 1) Set paths & choose ONE split
# =========================
EX=/net/flood/data2/users/x_yan/physicsnemo/examples/weather/corrdiff
BASE=/net/flood/data2/users/x_yan/00_6hourly_puerto-rico_cgp_inflation_factor_48ens

DOM=historical     # or: future | invariant
SPLIT=1            # single split only

# where to put stats and checkpoints
mkdir -p $EX/data

# =========================
# 2) Compute normalization stats (from TRAIN)
#    - Reads:  $BASE/6_hourly_${DOM}/training_data/split${SPLIT}/{lens2_gp_itr_3.npz, mpas_rain.npz}
#    - Writes: $EX/data/cgpmpas_${DOM}_s${SPLIT}_stats.json
#
#    - In: lens2_gp_itr_3.npz (train), mpas_rain.npz (train) → Out: data/cgpmpas_${DOM}_s${SPLIT}_stats.json
# =========================
python tools/compute_stats_cgp_mpas.py \
  --base-root "$BASE" \
  --domain "$DOM" \
  --split $SPLIT \
  --out "$EX/data/cgpmpas_${DOM}_s${SPLIT}_stats.json"

# =========================
# 3) Train REGRESSION (stage 1, smaller model for speed)
#    - Uses your config: conf/config_training_cgp_mpas_regression.yaml
#    - Dataset is your cgp_mpas.py class via Hydra overrides
#    - Writes checkpoints into: checkpoints_cgpmpas_${DOM}_s${SPLIT}_regression/
#
#    - In: dataset (CGP HR as input, MPAS HR as target), stats.json → Out: checkpoints_cgpmpas_${DOM}_s${SPLIT}_regression/*.pt
# =========================
cd $EX
python train.py --config-name=config_training_cgp_mpas_regression.yaml \
  ++dataset.type=datasets/cgp_mpas.py::CgpMpasSplit \
  ++dataset.base_root="$BASE" \
  ++dataset.domain="$DOM" \
  ++dataset.split=$SPLIT \
  ++dataset.phase=train \
  ++dataset.stats_path="$EX/data/cgpmpas_${DOM}_s${SPLIT}_stats.json" \
  ++validation.type=datasets/cgp_mpas.py::CgpMpasSplit \
  ++validation.base_root="$BASE" \
  ++validation.domain="$DOM" \
  ++validation.split=$SPLIT \
  ++validation.phase=val \
  ++validation.stats_path="$EX/data/cgpmpas_${DOM}_s${SPLIT}_stats.json" \
  ++results_dir=checkpoints_cgpmpas_${DOM}_s${SPLIT}_regression

# Grab the newest regression checkpoint path for diffusion
REG_CKPT=$(ls -1t checkpoints_cgpmpas_${DOM}_s${SPLIT}_regression/*.pt | head -1)
echo "REG_CKPT = $REG_CKPT"

# =========================
# 4) Train DIFFUSION (stage 2)
#    - Uses your config: conf/config_training_cgp_mpas_diffusion.yaml
#    - Warm-starts from the regression checkpoint
#    - Writes diffusion checkpoints into: checkpoints_cgpmpas_${DOM}_s${SPLIT}_diffusion/
#
#    - In: regression checkpoint + same dataset/stats → Out: checkpoints_cgpmpas_${DOM}_s${SPLIT}_diffusion/*.mdlus
# =========================
python train.py --config-name=config_training_cgp_mpas_diffusion.yaml \
  ++training.io.regression_checkpoint_path="$REG_CKPT" \
  ++dataset.type=datasets/cgp_mpas.py::CgpMpasSplit \
  ++dataset.base_root="$BASE" \
  ++dataset.domain="$DOM" \
  ++dataset.split=$SPLIT \
  ++dataset.phase=train \
  ++dataset.stats_path="$EX/data/cgpmpas_${DOM}_s${SPLIT}_stats.json" \
  ++validation.type=datasets/cgp_mpas.py::CgpMpasSplit \
  ++validation.base_root="$BASE" \
  ++validation.domain="$DOM" \
  ++validation.split=$SPLIT \
  ++validation.phase=val \
  ++validation.stats_path="$EX/data/cgpmpas_${DOM}_s${SPLIT}_stats.json" \
  ++results_dir=checkpoints_cgpmpas_${DOM}_s${SPLIT}_diffusion


# Newest diffusion checkpoint (.mdlus)
DIFF_CKPT=$(ls -1t checkpoints_cgpmpas_${DOM}_s${SPLIT}_diffusion/*.mdlus | head -1)
echo "DIFF_CKPT = $DIFF_CKPT"


# =========================
# 5) SAME-CLIMATE generation for train/val/test
#    - Uses your config: conf/config_generate_cgp_mpas.yaml
#    - Produces NetCDF files: gen_${DOM}_s${SPLIT}_${EP}.nc
#    - Then exports to .npz next to the split:
#      lens2_corrdiff_sr_itr_3.npz  (keys: train/val/test)
#
#    - In: regression + diffusion checkpoints + dataset(phase) → Out: gen_${DOM}*.nc (NetCDF)
#    - In: NetCDF → Out: lens2_corrdiff_sr_*.npz placed next to your split, key’d by epoch (train/val/test)
# =========================
for EP in train val test; do
  OUTNC=gen_${DOM}_s${SPLIT}_${EP}.nc

  python generate.py --config-name=config_generate_cgp_mpas.yaml \
    ++generation.io.reg_ckpt_filename="$REG_CKPT" \
    ++generation.io.res_ckpt_filename="$DIFF_CKPT" \
    ++dataset.type=datasets/cgp_mpas.py::CgpMpasSplit \
    ++dataset.base_root="$BASE" \
    ++dataset.domain="$DOM" \
    ++dataset.split=$SPLIT \
    ++dataset.phase=$EP \
    ++dataset.stats_path="$EX/data/cgpmpas_${DOM}_s${SPLIT}_stats.json" \
    ++generation.io.out_filename="$OUTNC"

  # Export NetCDF → .npz with your naming
  python tools/export_corrdiff_to_npz.py \
    --netcdf "$OUTNC" \
    --base-root "$BASE" \
    --domain-out "$DOM" \
    --split $SPLIT \
    --epoch $EP \
    --combo same
done
```

### Results will look like
```bash
$BASE/6_hourly_${DOM}/training_data/split${SPLIT}/lens2_corrdiff_sr_itr_3.npz
  ├─ train: (N,Hf,Wf)
  ├─ val  : (N,Hf,Wf)
  └─ test : (N,Hf,Wf)
```

### Cross-climate generation for the same split 
#### HIST model on FUT data → lens2_corrdiff_sr_hist_on_fut.npz (under FUT)
```bash
DOM_TRAIN=historical; DOM_GEN=future; SPLIT=1
REG_CKPT=$(ls -1t checkpoints_cgpmpas_${DOM_TRAIN}_s${SPLIT}_regression/*.pt | head -1)
DIFF_CKPT=$(ls -1t checkpoints_cgpmpas_${DOM_TRAIN}_s${SPLIT}_diffusion/*.mdlus | head -1)

for EP in train val test; do
  OUTNC=gen_${DOM_TRAIN}_on_${DOM_GEN}_s${SPLIT}_${EP}.nc
  python generate.py --config-name=config_generate_cgp_mpas.yaml \
    ++generation.io.reg_ckpt_filename="$REG_CKPT" \
    ++generation.io.res_ckpt_filename="$DIFF_CKPT" \
    ++dataset.type=datasets/cgp_mpas.py::CgpMpasSplit \
    ++dataset.base_root="$BASE" \
    ++dataset.domain="$DOM_GEN" \
    ++dataset.split=$SPLIT \
    ++dataset.phase=$EP \
    ++dataset.stats_path="$EX/data/cgpmpas_${DOM_TRAIN}_s${SPLIT}_stats.json" \
    ++generation.io.out_filename="$OUTNC"

  python tools/export_corrdiff_to_npz.py \
    --netcdf "$OUTNC" \
    --base-root "$BASE" \
    --domain-out future \
    --split $SPLIT \
    --epoch $EP \
    --combo hist_on_fut
done
```

#### FUT model on HIST data → lens2_corrdiff_sr_fut_on_hist.npz (under HIST)
```bash
DOM_TRAIN=future; DOM_GEN=historical; SPLIT=1
REG_CKPT=$(ls -1t checkpoints_cgpmpas_${DOM_TRAIN}_s${SPLIT}_regression/*.pt | head -1)
DIFF_CKPT=$(ls -1t checkpoints_cgpmpas_${DOM_TRAIN}_s${SPLIT}_diffusion/*.mdlus | head -1)

for EP in train val test; do
  OUTNC=gen_${DOM_TRAIN}_on_${DOM_GEN}_s${SPLIT}_${EP}.nc
  python generate.py --config-name=config_generate_cgp_mpas.yaml \
    ++generation.io.reg_ckpt_filename="$REG_CKPT" \
    ++generation.io.res_ckpt_filename="$DIFF_CKPT" \
    ++dataset.type=datasets/cgp_mpas.py::CgpMpasSplit \
    ++dataset.base_root="$BASE" \
    ++dataset.domain="$DOM_GEN" \
    ++dataset.split=$SPLIT \
    ++dataset.phase=$EP \
    ++dataset.stats_path="$EX/data/cgpmpas_${DOM_TRAIN}_s${SPLIT}_stats.json" \
    ++generation.io.out_filename="$OUTNC"

  python tools/export_corrdiff_to_npz.py \
    --netcdf "$OUTNC" \
    --base-root "$BASE" \
    --domain-out historical \
    --split $SPLIT \
    --epoch $EP \
    --combo fut_on_hist
done
```

#### INV model on HIST/FUT → lens2_corrdiff_sr_inv_on_hist.npz & lens2_corrdiff_sr_inv_on_fut.npz (under INV)
```bash
# INV → HIST
DOM_TRAIN=invariant; DOM_GEN=historical; SPLIT=1
REG_CKPT=$(ls -1t checkpoints_cgpmpas_${DOM_TRAIN}_s${SPLIT}_regression/*.pt | head -1)
DIFF_CKPT=$(ls -1t checkpoints_cgpmpas_${DOM_TRAIN}_s${SPLIT}_diffusion/*.mdlus | head -1)
for EP in train val test; do
  OUTNC=gen_${DOM_TRAIN}_on_${DOM_GEN}_s${SPLIT}_${EP}.nc
  python generate.py --config-name=config_generate_cgp_mpas.yaml \
    ++generation.io.reg_ckpt_filename="$REG_CKPT" \
    ++generation.io.res_ckpt_filename="$DIFF_CKPT" \
    ++dataset.type=datasets/cgp_mpas.py::CgpMpasSplit \
    ++dataset.base_root="$BASE" \
    ++dataset.domain="$DOM_GEN" \
    ++dataset.split=$SPLIT \
    ++dataset.phase=$EP \
    ++dataset.stats_path="$EX/data/cgpmpas_${DOM_TRAIN}_s${SPLIT}_stats.json" \
    ++generation.io.out_filename="$OUTNC"

  python tools/export_corrdiff_to_npz.py \
    --netcdf "$OUTNC" \
    --base-root "$BASE" \
    --domain-out invariant \
    --split $SPLIT \
    --epoch $EP \
    --combo inv_on_hist
done

# INV → FUT
DOM_TRAIN=invariant; DOM_GEN=future; SPLIT=1
REG_CKPT=$(ls -1t checkpoints_cgpmpas_${DOM_TRAIN}_s${SPLIT}_regression/*.pt | head -1)
DIFF_CKPT=$(ls -1t checkpoints_cgpmpas_${DOM_TRAIN}_s${SPLIT}_diffusion/*.mdlus | head -1)
for EP in train val test; do
  OUTNC=gen_${DOM_TRAIN}_on_${DOM_GEN}_s${SPLIT}_${EP}.nc
  python generate.py --config-name=config_generate_cgp_mpas.yaml \
    ++generation.io.reg_ckpt_filename="$REG_CKPT" \
    ++generation.io.res_ckpt_filename="$DIFF_CKPT" \
    ++dataset.type=datasets/cgp_mpas.py::CgpMpasSplit \
    ++dataset.base_root="$BASE" \
    ++dataset.domain="$DOM_GEN" \
    ++dataset.split=$SPLIT \
    ++dataset.phase=$EP \
    ++dataset.stats_path="$EX/data/cgpmpas_${DOM_TRAIN}_s${SPLIT}_stats.json" \
    ++generation.io.out_filename="$OUTNC"

  python tools/export_corrdiff_to_npz.py \
    --netcdf "$OUTNC" \
    --base-root "$BASE" \
    --domain-out invariant \
    --split $SPLIT \
    --epoch $EP \
    --combo inv_on_fut
done
```
