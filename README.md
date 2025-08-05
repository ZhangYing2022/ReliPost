# ReliPost: Background Synthesis and Layout Planning with Multimodal Large Language Model
📌 Official Implementation of the Paper:
"Towards Reliable Poster Generation: Background Synthesis and Layout Planning with Multimodal Large Language Model."

## 📢 Important Notices
🔥 Training Code: Will be released upon paper acceptance.

📝 [2025.08] Inference Code: Has been released.

## 📦 Dataset
We introduce BiPoster, a curated bilingual (Chinese-English) poster dataset, containing over 2,882 samples across 6 categories.

**The dataset will be publicly available once the anonymous policy period concludes.**

> **Note**: All samples in BiPoster were collected and annotated for **academic research purposes only**.

### ⚠️ Usage Restrictions
#### ✅ Permitted Uses:
- Academic research
- Reproduction of experimental results  
- Non-commercial educational use

#### ❌ Prohibited Uses:
- Any form of commercial use
- **Redistribution** of the dataset without permission
- Use in projects with commercial licensing, monetization, or proprietary extensions

### 📁 Structure
Each sample contains:
```bash
📦 datapath/
├── images/                  # Raw poster images
├── backgrounds/             # Backgrounds
├── layout_json/             # MLLM-predicted layout (JSON format)
└── meta.csv                 # Category, style, font info
```

#### 🔗 Download Link 
- Download the model weight by this link.
- The dataset can be downloaded once the policy period ends.


## 🛠 Environment Setup
This project uses Qwen-VL-7B as the MLLM and FLUX for background generation. Follow the instructions below to set up your environment.
```bash
# 1. Create and activate environment
conda create -n relipost python=3.10 -y
conda activate relipost

# 2. Install dependencies
pip install -r requirements.txt
```

## 🚀 Inference (Layout + Background + Rendering)
Follow these steps to generate the final poster with layout, background, and rendering:
### 1. Generate poster background
```bash
python scripts/generate_background.py \
    --prompt_file processed/background_prompts.txt \
    --output_dir results/backgrounds/
```
### 2. Predict layout using MLLM
```bash

python scripts/layout_infer.py \
    --text_dir processed/texts/ \
    --output_dir results/layout_json/
```
### 3. Render final poster using layout + background
```bash
python scripts/render_poster.py \
    --layout_dir results/layout_json/ \
    --bg_dir results/backgrounds/ \
    --output_dir results/final/
```
Each rendered poster will be saved as .png under results/final/ directory.





