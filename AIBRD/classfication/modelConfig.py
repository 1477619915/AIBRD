import numpy as np
import torch

# 设置随机数种子，确保实验结果的可重复性
np.random.seed(0)
torch.manual_seed(0)
USE_CUDA = torch.cuda.is_available()
if USE_CUDA:
    torch.cuda.manual_seed(0)


class modelConfig:
    batch_size = 32
    output_size = 8
    hidden_dim = 714
    n_layers = 2
    lr = 1e-4
    bidirectional = True   # 这里为True，为双向LSTM
    epochs = 30
    print_every = 20
    clip = 5  # gradient clipping
    use_cuda = USE_CUDA
    bert_path = '/root/autodl-tmp/AIBRD/bert-base-uncased'  # 预训练BERT路径
    save_path = '/root/autodl-tmp/AIBRD/bert_BiLstm_1.pth'       # 训练模型保存路径
    