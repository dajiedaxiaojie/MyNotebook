Install PyTorch with matched device
===
NVIDIA GPU
---

pip install torch==2.4.0+cu124 torchaudio==2.4.0+cu124 --extra-index-url https://download.pytorch.org/whl/cu124

AMD GPU
---
pip install torch==2.5.1+rocm6.2 torchaudio==2.5.1+rocm6.2 --extra-index-url https://download.pytorch.org/whl/rocm6.2

Intel GPU
---
pip install torch torchaudio --index-url https://download.pytorch.org/whl/test/xpu

Apple Silicon
---
pip install torch torchaudio
