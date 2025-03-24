from Lstm import Lstm
import numpy as np
import torch
import torch.nn as nn
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
from tqdm import tqdm
import datetime


def train_model(config, train_loader, valid_loader):
    net = Lstm(config.bert_path,
               config.hidden_dim,
               config.output_size,
               config.n_layers,
               config.bidirectional)
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(net.parameters(), lr=config.lr)
    if (config.use_cuda):
        net.cuda()
    net.train()
    best_acc = 0.0
    with open("training_log.txt", "w") as f:
        for e in range(config.epochs):
            # 初始化LSTM的hidden
            h = net.init_hidden(config.batch_size, config.use_cuda)
            counter = 0
            # batch loop
            for inputs, labels, pattern_feature in tqdm(train_loader):
                counter += 1

                if (config.use_cuda):
                    inputs, labels, pattern_feature = inputs.cuda(), labels.cuda(), pattern_feature.cuda()
                h = tuple([each.data for each in h])
                net.zero_grad()
                output = net(inputs, h, pattern_feature)
                loss = criterion(output.squeeze(), labels.long())
                loss.backward()
                optimizer.step()

            net.eval()
            with torch.no_grad():
                val_h = net.init_hidden(config.batch_size, config.use_cuda)
                val_losses = []
                y_true = []
                y_pred = []
                for inputs, labels, pattern_feature in valid_loader:
                    val_h = tuple([each.data for each in val_h])

                    if (config.use_cuda):
                        inputs, labels, pattern_feature = inputs.cuda(), labels.cuda(), pattern_feature.cuda()

                    output = net(inputs, val_h, pattern_feature)
                    val_loss = criterion(output.squeeze(), labels.long())
                    val_losses.append(val_loss.item())
                    _, predicted = torch.max(output.data, 1)
                    y_true += labels.cpu().numpy().tolist()
                    y_pred += predicted.cpu().numpy().tolist()
            net.train()
            avg_val_loss = np.mean(val_losses)
            acc = accuracy_score(y_true, y_pred)
            precision = precision_score(y_true, y_pred, average='macro')
            recall = recall_score(y_true, y_pred, average='macro')
            f1 = f1_score(y_true, y_pred, average='macro')
            now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            log = ("Epoch: {}/{}, Step: {}, Loss: {:.6f}, Val Loss: {:.6f}, Accuracy: {:.6f},Precision: {:.6f},"
                   " Recall: {:.6f}, F1: {:.6f}, Time:{}\n").format(e + 1, config.epochs, counter, loss.item(),
                                                                    avg_val_loss, acc, precision, recall, f1, now_time)
            f.write(log)
            print(log)
            if acc > best_acc:
                best_acc = acc
                torch.save(net.state_dict(), config.save_path)
    print("Best validation accuracy:", best_acc)


def test_model(config, test_loader):
    net = Lstm(config.bert_path,
               config.hidden_dim,
               config.output_size,
               config.n_layers,
               config.bidirectional)
    net.load_state_dict(torch.load(config.save_path))
    net.cuda()
    # 定义损失函数
    criterion = nn.CrossEntropyLoss()
    test_losses = []

    # 定义预测值和真实值
    y_true = []
    y_pred = []

    # 初始化隐藏状态
    h = net.init_hidden(config.batch_size, config.use_cuda)

    # 将模型设置为评估状态
    net.eval()

    # 遍历测试集的数据
    for inputs, labels, pattern_feature in tqdm(test_loader):
        h = tuple([each.data for each in h])
        if (config.use_cuda):
            inputs, labels, pattern_feature = inputs.cuda(), labels.cuda(), pattern_feature.cuda()

        output = net(inputs, h, pattern_feature)
        test_loss = criterion(output.squeeze(), labels.long())
        test_losses.append(test_loss.item())
        _, predicted = torch.max(output.data, 1)
        y_true += labels.cpu().numpy().tolist()
        y_pred += predicted.cpu().numpy().tolist()
        acc = accuracy_score(y_true, y_pred)
        precision = precision_score(y_true, y_pred, average='macro')
        recall = recall_score(y_true, y_pred, average='macro')
        f1 = f1_score(y_true, y_pred, average='macro')
        cm = confusion_matrix(y_true, y_pred)
        print(cm)

    print("Test loss: {:.3f}".format(np.mean(test_losses)))
    print("Test accuracy: {:.3f}".format(acc))
    print("Test precision: {:.3f}".format(precision))
    print("Test recall: {:.3f}".format(recall))
    print("Test f1: {:.3f}".format(f1))

