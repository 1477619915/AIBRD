import torch
import torch.nn.functional as F

class CrossAttentionFusion(torch.nn.Module):
    def __init__(self, bert_dim, pattern_dim):
        super(CrossAttentionFusion, self).__init__()
        self.scale_bert = bert_dim ** 0.5
        self.scale_sem = pattern_dim ** 0.5

        # 选择更大的维度作为统一的隐藏维度
        hidden_dim = max(bert_dim, pattern_dim)

        # 线性映射，使得两个特征映射到相同的 hidden_dim
        self.W_q_sem = torch.nn.Linear(pattern_dim, hidden_dim)
        self.W_k_bert = torch.nn.Linear(bert_dim, hidden_dim)
        self.W_v_bert = torch.nn.Linear(bert_dim, hidden_dim)

        self.W_q_bert = torch.nn.Linear(bert_dim, hidden_dim)
        self.W_k_sem = torch.nn.Linear(pattern_dim, hidden_dim)
        self.W_v_sem = torch.nn.Linear(pattern_dim, hidden_dim)

        self.output_fc = torch.nn.Linear(hidden_dim, hidden_dim)  # 输出投影层
        self.hidden_dim = hidden_dim  # 记录隐藏层维度

    def scaled_dot_product_attention(self, Q, K, V, scale_factor):
        """
        计算缩放点积注意力
        """
        attn_scores = torch.matmul(Q, K.transpose(-2, -1)) / scale_factor
        attn_weights = F.softmax(attn_scores, dim=-1)
        output = torch.matmul(attn_weights, V)
        return output

    def forward(self, bert_emb, sem_emb):
        """
        bert_emb: (batch_size, seq_len, bert_dim)
        sem_emb: (batch_size, seq_len, pattern_dim)
        """
        # 语义知识库 -> Query，BERT 词嵌入 -> Key, Value
        Q_sem = self.W_q_sem(sem_emb)
        K_bert = self.W_k_bert(bert_emb)
        V_bert = self.W_v_bert(bert_emb)
        attn_sem2bert = self.scaled_dot_product_attention(Q_sem, K_bert, V_bert, self.scale_bert)

        # BERT 词嵌入 -> Query，语义知识库 -> Key, Value
        Q_bert = self.W_q_bert(bert_emb)
        K_sem = self.W_k_sem(sem_emb)
        V_sem = self.W_v_sem(sem_emb)
        attn_bert2sem = self.scaled_dot_product_attention(Q_bert, K_sem, V_sem, self.scale_sem)

        # 加和两个方向的注意力信息
        fusion_output = attn_sem2bert + attn_bert2sem
        fusion_output = self.output_fc(fusion_output)  # 线性变换后输出

        return fusion_output

# # 测试
# batch_size = 4
# seq_len = 10
# bert_dim = 768  # BERT 词嵌入维度
# pattern_dim = 600  # 语义知识库维度

# bert_emb = torch.randn(batch_size, seq_len, bert_dim)  # 随机 BERT 词嵌入
# sem_emb = torch.randn(batch_size, seq_len, pattern_dim)  # 随机语义知识库特征

# model = CrossAttentionFusion(bert_dim, pattern_dim)
# output = model(bert_emb, sem_emb)

# print(output.shape)  # (batch_size, seq_len, max(bert_dim, pattern_dim))
