| 框架名稱          | 支持平台      | 主要特點               | 模型數量/覆蓋度      |
|-------------------|--------------|------------------------|----------------------|
| timm              | PyTorch      | SOTA模型多、訓練腳本齊全 | 極多（數百種）       |
| PaddleClas        | PaddlePaddle | 工業級部署、模型豐富     | 多（數百種）         |
| MMClassification  | PyTorch      | 配置靈活、科研友好       | 多（數百種）         |
| GluonCV           | MXNet        | MXNet生態、模型豐富      | 多（數百種）         |
| Keras Applications| TensorFlow   | 易用、集成於 Keras       | 常用模型（數十種）   |
| torchvision       | PyTorch      | 官方支持、穩定、易用     | 常用模型（數十種）   |


| 框架名稱         | 適合場景           | 優勢重點                   | 手機端部署友好度     |
|------------------|--------------------|----------------------------|----------------------|
| timm             | 快速實驗、科研     | 模型最新最全，PyTorch 生態 | 需額外轉換和優化     |
| PaddleClas       | 工業部署、移動端應用 | 工業級支持，移動端部署方便 | 非常友好             |
| MMClassification | 科研與工業應用     | 配置靈活，OpenMMLab 生態   | 需額外轉換           |
| GluonCV          | MXNet 用戶，跨平台部署 | 模型豐富，支持多任務       | 一般                 |


# ultralytics install
```
conda create --name ultralytics-env python=3.11 -y
conda install -c pytorch -c nvidia -c conda-forge pytorch torchvision pytorch-cuda=11.8 ultralytics
```
