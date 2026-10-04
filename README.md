# Reinforcement Learning course

This repository contains the code and materials for the practical work of the Reinforcement Learning course for "Parcours IA - ENSC 2026/2027".

# Base installation

You need Python 3.10 to 3.12 (the code is tested with Python 3.12.3 on Linux). We recommend creating a virtual environment for this project.

Create the virtual environment (the command name depends on your system):
```bash
python3 -m venv venv   # On Linux or MacOS
python -m venv venv    # On Windows (or: py -m venv venv)
```

On Ubuntu/Debian, if this fails with `ensurepip is not available`, first run `sudo apt install python3-venv`.

Then activate it:
```bash
source venv/bin/activate   # On Linux or MacOS
venv\Scripts\activate      # On Windows
```

On Windows PowerShell, if activation fails with "running scripts is disabled on this system", run `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` once, then activate again (or use `cmd` instead of PowerShell).

Once the virtual environment is activated, `python` and `pip` refer to the environment's ones on every system. Install the dependencies:
```bash
python -m pip install -r requirements.txt
```

# Torch installation

(only required for the DQN part of the notebook)

The CPU version of torch is sufficient for this TP (the neural network is small) and is a much smaller download:
```bash
python -m pip install torch --index-url https://download.pytorch.org/whl/cpu   # On Linux or Windows
python -m pip install torch                                                    # On MacOS
```

If you prefer to use a NVIDIA GPU, pick the install command on https://pytorch.org/get-started/locally/ instead (for example with CUDA 12.6: `python -m pip install torch --index-url https://download.pytorch.org/whl/cu126`).

To verify torch installation, you can run:
```bash
python -c "import torch; print(torch.__version__, 'CUDA:', torch.cuda.is_available())"
```

# Usage

The notebook `ENSC3A_RL_2026-2027/notebook.ipynb` contains the practical work for the course. Open it in VS Code (with the Jupyter extension) and select the `venv` kernel in the top-right corner.

The MCTS practical work is in `ENSC3A_RL_2026-2027/mcts/`, see its [README](ENSC3A_RL_2026-2027/mcts/README.md).

If you have installation issues, you can do the TP on this [Google Colab notebook]( https://colab.research.google.com/drive/1FGXJO-G9f2HUHPdWsg3eRszc8Vtj71-K?usp=sharing). Open it and "Fichier → Enregistrer une copie dans Drive" to get your own copy. 