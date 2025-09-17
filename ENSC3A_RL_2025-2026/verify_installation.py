import gymnasium as gym
import ale_py
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
import torch

print(f"Is torch detecting CUDA GPU? {torch.cuda.is_available()}")
print("Installation is verified as correct.")
