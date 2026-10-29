# VDress — Virtual Try-On

**Wearable Virtuosity: Try-on Any Outfit, Virtually**  
Master’s thesis project by **Shreyas Chakravarthy**, FAU Erlangen-Nürnberg, 2024.

Image-based virtual try-on using a VITON-HD-style pipeline: a target garment and a preprocessed person image are combined through segmentation generation, geometric matching and ALIAS synthesis. This repository contains the supplied PyTorch modules, Colab experiments, Flask interfaces and evaluation notebook.

## Pipeline

1. Load person images, clothing, clothing masks, human parsing and OpenPose annotations.
2. Construct clothing-agnostic person representations and predict segmentation.
3. Warp the garment with the geometric matching module (GMM).
4. Synthesize the try-on image with the ALIAS generator.
5. Evaluate generated images using SSIM, LPIPS and dataset-level FID.

The supplied modules load pretrained weights and perform **inference**. Module 5 runs inference on the training split; it does not train a new model. Pose estimation and human parsing must already be available; this repository does not provide a complete preprocessing pipeline for arbitrary uploaded photos.

## Start here

| File | Purpose |
| --- | --- |
| `infer.py` | Command-line inference with configurable data and checkpoint paths |
| `module1.py` | Dataset loading and clothing-agnostic representations |
| `module2.py` | Segmentation, GMM and ALIAS model architectures |
| `module3.py` | Checkpoint loading and image saving |
| `module4.ipynb` | Small test-data inference workflow |
| `module5.ipynb` | Inference on the training split |
| `module6.ipynb` | Larger test-data inference workflow |
| `Final_web2_Testingscore.ipynb` | Colab web experiment and image metrics |
| `templates/` | Notebook try-on interface templates |
| `app.py`, `demo_templates/` | Separate image-upload demo; does not perform try-on |
| Other notebooks | Earlier project and web experiments |

## Setup and inference

Use a **CUDA GPU**, such as a Colab GPU runtime. The original project was executed in Google Colab. No tested, pinned dependency environment was supplied; compatibility with a fresh environment remains to be verified.

Install a CUDA-compatible PyTorch and torchvision pair for your environment, then:

```sh
pip install -r requirements.txt
python infer.py --dataset_dir datasets --dataset_mode test --dataset_list test_pairs.txt --checkpoint_dir checkpoints --save_dir results
```

Run these commands from the repository root. Supply the following weights in `checkpoints/`:

- `seg_final.pth`
- `gmm_final.pth`
- `alias_final.pth`

Weights and dataset images are **not committed**. Obtain the original research assets from their authorized source or use the author's existing local copies. No public download link has been verified. See `checkpoints/README.md` for identifiers of the supplied files.

## Dataset layout

For each split (`test` or `train`), the loader expects these subfolders:

| Folder | Example filename |
| --- | --- |
| `image/` | `05006_00.jpg` |
| `image-parse/` | `05006_00.png` |
| `openpose-img/` | `05006_00_rendered.png` |
| `openpose-json/` | `05006_00_keypoints.json` |
| `cloth/` | `11001_00.jpg` |
| `cloth-mask/` | `11001_00.jpg` |

The supplied `datasets/test_pairs.txt` contains 2,032 pairs; `datasets/train_pairs.txt` contains 11,647. Each line is `person_filename clothing_filename`. Preserve the original preprocessing, naming and image dimensions (default 1024 × 768). Output files are written to `results/output/` by default.

## Colab notebooks and web experiments

Mount Drive and place the project at the Drive location used in the notebook. The historical notebooks retain their original paths: module 4 uses `VDress/datasets`, while modules 5 and 6 use `VDress/data`. Adjust paths before running; `infer.py` avoids those hard-coded paths.

For the notebook web interface, place `templates/` at the template location configured in that notebook. Set `NGROK_AUTHTOKEN` privately in the runtime environment before executing ngrok cells. Do not save the value in notebook source or output. Notebook outputs have been cleared for publication.

The separate local upload demo runs with `python app.py`. Put sample garment images in `static/grid_images/`, then open the localhost address printed by Flask. This demo only displays selected/uploaded images and is not a production service.

## Evaluation

`Final_web2_Testingscore.ipynb` reads images from `data_score/Reference_image` and `data_score/Generated_images`. Use matching filenames and meaningful ground-truth pairs for SSIM/LPIPS. A person wearing a different target garment is not pixel-aligned ground truth for an unpaired try-on output.

The supplied implementation computes grayscale SSIM, AlexNet LPIPS, and FID over image directories. LPIPS inputs are now mapped to [-1, 1]. This changes previously computed LPIPS values; rerun evaluation rather than reusing old scores. FID is a dataset-level statistic, not a single-image score; use sufficient samples and consistent evaluation settings. No fresh metric results are claimed here.

## Publication fixes and validation

- Removed embedded ngrok credentials and saved notebook outputs.
- Corrected LPIPS input normalization and failure handling for unreadable evaluation pairs.
- Fixed the data loader to respect disabled shuffling and retain the final partial batch.
- Added CPU checkpoint mapping and explicit weights-only loading.
- Matched standalone upload-demo templates; rejected invalid grid paths, limited upload size and disabled debug mode.
- Added a configurable inference entry point without changing the model architecture.

Python syntax and transformed notebook code were checked during preparation; data-loader ordering and final-batch options passed regression checks. Template rendering has not been tested. **End-to-end inference, checkpoint/model compatibility, web runtime and metrics remain unverified**: the preparation environment has no PyTorch/CUDA runtime and the dataset sample has not been supplied.

## Research attribution

This thesis builds on VITON-HD (Choi et al., 2021), including its segmentation, geometric matching and ALIAS concepts. The supplied architecture closely follows that research; the entire architecture should not be represented as a new invention by the thesis author. See the thesis bibliography for detailed citations. Upstream code, model and dataset licensing should be confirmed before redistribution; no blanket license is assigned by this repository.
