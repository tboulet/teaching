# Reinforcement Learning course

This repository contains the code and materials for the practical work of the Reinforcement Learning course for "Parcours IA - ENSC 2025/2026".

# Installation

The code is verified to work with python 3.11, windows and with the ``uv`` package manager. You might consider creating a new virtual environment for this project.

To install `uv`, you can run:

```bash
pip install uv
```

Then, create and activate a virtual environment (replace `3.11` with your desired Python version if needed):
```bash
uv venv --python 3.11 # Or if not using uv: python -m venv venv
venv\Scripts\activate # On Windows
source venv/bin/activate # On Linux or MacOS
```

Then, install the dependencies:

```bash
uv pip install -r requirements.txt
```

# Torch installation

(only required for 2nd part of the TP)

Install torch following the instructions on https://pytorch.org/get-started/locally/ (the command depends on your system and whether you have a CUDA-capable GPU).
By default and for example, on Windows with uv and CUDA 12.6, you can run:

```bash
uv pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu126
```

To verify torch installation, you can run:

```bash
python ENSC3A_RL_2025-2026\verify_installation.py  # On Windows
python ENSC3A_RL_2025-2026/verify_installation.py  # On Linux or MacOS
```

# Usage

The notebook `ENSC3A_RL_2025-2026/Deep_RL.py` contains the practical work for the course. You can run it using Jupyter Notebook on VS Code or on Colab [here](https://colab.research.google.com/drive/13iiiH74SSlf9ExoJHT0ooI39aJdIVugM).


