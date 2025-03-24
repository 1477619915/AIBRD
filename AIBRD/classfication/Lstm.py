import torch.nn as nn
import torch

from MultimodalAttention import CrossAttentionFusion
from modelConfig import modelConfig
from patternVect import patternVect
import torch
from transformers import BertTokenizer, BertModel


class Lstm(nn.Module):
    # 类的初始化函数，参数：LSTM隐藏层的层数，输出层数，LSTM层数，是否为BiLSTM，dropout层的丢弃概率
    def __init__(self, bertpath, hidden_dim, output_size, n_layers, bidirectional=True, drop_prob=0.5):
        super(Lstm, self).__init__()

        self.output_size = output_size 
        self.n_layers = n_layers
        self.hidden_dim = hidden_dim
        self.bidirectional = bidirectional
        self.bert_dim = 768
        self.CBK_dim = 600
        self.pattern_dim = 60


        # Bert模型嵌入到自定义模型里面
        self.bert = BertModel.from_pretrained(bertpath)
        for param in self.bert.parameters():
            param.requires_grad = True

        # LSTM层
        self.lstm = nn.LSTM(768 + 600 + 60, hidden_dim, n_layers, batch_first=True, bidirectional=bidirectional)

        # dropout层
        self.dropout = nn.Dropout(drop_prob)

        # linear and sigmoid layers
        if bidirectional:
            self.fc = nn.Linear(hidden_dim * 2, output_size)
        else:
            self.fc = nn.Linear(hidden_dim, output_size)

    def forward(self, inputs, hidden, pattern_feature, tfidf_array_feature):

        bert_feature = self.bert(inputs)[0]

        # 1.拼接特征融合
        fusion = torch.cat((bert_feature, pattern_feature, tfidf_array_feature), dim=-1)
        # a.用bert作为特征
        # fusion = bert_feature
        # b.用bert+pattern作为特征
        # fusion = torch.cat((bert_feature, pattern_feature), dim=-1)
        # c.用bert+上下文知识库作为特征
        # fusion = torch.cat((bert_feature, tfidf_array_feature), dim=-1)

        # 2.LMF融合特征

        # 定义特征融合模型
        # model = CrossAttentionFusion(self.CBK_dim, self.pattern_dim).to("cuda")
        # fusion1 = model(tfidf_array_feature, pattern_feature.float())
        # fusion = torch.cat((bert_feature, fusion1), dim=-1)


        lstm_out, (hidden_last, cn_last) = self.lstm(fusion, hidden)
        # print(lstm_out.shape)   #[32,100,768]
        # print(hidden_last.shape)   #[4, 32, 384]
        # print(cn_last.shape)    #[4, 32, 384]

        # 修改 双向的需要单独处理
        if self.bidirectional:
            # 正向最后一层，最后一个时刻
            hidden_last_L = hidden_last[-2]
            # print(hidden_last_L.shape)  #[32, 384]
            # 反向最后一层，最后一个时刻
            hidden_last_R = hidden_last[-1]
            # print(hidden_last_R.shape)   #[32, 384]
            # 进行拼接
            hidden_last_out = torch.cat([hidden_last_L, hidden_last_R], dim=-1)
            # print(hidden_last_out.shape,'hidden_last_out')   #[32, 768]
        else:
            hidden_last_out = hidden_last[-1]  # [32, 384]

        # dropout and fully-connected layer
        out = self.dropout(hidden_last_out)
        # print(out.shape)    #[32,768]
        out = self.fc(out)

        return out

    def init_hidden(self, batch_size, use_cuda):
        weight = next(self.parameters()).data

        number = 1
        if self.bidirectional:
            number = 2

        if (use_cuda):
            hidden = (weight.new(self.n_layers * number, batch_size, self.hidden_dim).zero_().float().cuda(),
                      weight.new(self.n_layers * number, batch_size, self.hidden_dim).zero_().float().cuda()
                      )
        else:
            hidden = (weight.new(self.n_layers * number, batch_size, self.hidden_dim).zero_().float(),
                      weight.new(self.n_layers * number, batch_size, self.hidden_dim).zero_().float()
                      )

        return hidden
