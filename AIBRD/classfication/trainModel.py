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
            for inputs, labels, pattern_feature, tfidf_array_feature in tqdm(train_loader):
                counter += 1

                if (config.use_cuda):
                    inputs, labels, pattern_feature, tfidf_array_feature = inputs.cuda(), labels.cuda(), pattern_feature.cuda(), tfidf_array_feature.cuda()
                h = tuple([each.data for each in h])
                net.zero_grad()
                output = net(inputs, h, pattern_feature, tfidf_array_feature)
                loss = criterion(output.squeeze(), labels.long())
                loss.backward()
                optimizer.step()

            net.eval()
            with torch.no_grad():
                val_h = net.init_hidden(config.batch_size, config.use_cuda)
                val_losses = []
                y_true = []
                y_pred = []
                for inputs, labels, pattern_feature, tfidf_array_feature in valid_loader:
                    val_h = tuple([each.data for each in val_h])

                    if (config.use_cuda):
                        inputs, labels, pattern_feature, tfidf_array_feature = inputs.cuda(), labels.cuda(), pattern_feature.cuda(), tfidf_array_feature.cuda()

                    output = net(inputs, val_h, pattern_feature, tfidf_array_feature)
                    val_loss = criterion(output.squeeze(), labels.long())
                    val_losses.append(val_loss.item())
                    _, predicted = torch.max(output.data, 1)
                    y_true += labels.cpu().numpy().tolist()
                    y_pred += predicted.cpu().numpy().tolist()
            net.train()
            avg_val_loss = np.mean(val_losses)
            acc = accuracy_score(y_true, y_pred)
            precision = precision_score(y_true, y_pred, average='macro',zero_division=1)
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
            if e == 15:
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
    for inputs, labels, pattern_feature, tfidf_array_feature in tqdm(test_loader):
        h = tuple([each.data for each in h])
        if (config.use_cuda):
            inputs, labels, pattern_feature, tfidf_array_feature = inputs.cuda(), labels.cuda(), pattern_feature.cuda(), tfidf_array_feature.cuda()

        output = net(inputs, h, pattern_feature, tfidf_array_feature)
        test_loss = criterion(output.squeeze(), labels.long())
        test_losses.append(test_loss.item())
        _, predicted = torch.max(output.data, 1)
        y_true += labels.cpu().numpy().tolist()
        y_pred += predicted.cpu().numpy().tolist()
        acc = accuracy_score(y_true, y_pred)
        precision = precision_score(y_true, y_pred, average='macro', zero_division=1)
        recall = recall_score(y_true, y_pred, average='macro', zero_division=1)
        f1 = f1_score(y_true, y_pred, average='macro', zero_division=1)
        cm = confusion_matrix(y_true, y_pred)
    print(cm)
    print("Test loss: {:.3f}".format(np.mean(test_losses)))
    print("Test accuracy: {:.3f}".format(acc))
    print("Test precision: {:.3f}".format(precision))
    print("Test recall: {:.3f}".format(recall))
    print("Test f1: {:.3f}".format(f1))
    print("================================")

    ob_tp = cm[1,1] + cm[1,4] + cm[1,5] + cm[1,7] + cm[4,1] + cm[4,4] + cm[4,5] + cm[4,7] + cm[5,1] + cm[5,4] + cm[5,5] + cm[5,7] + cm[7,1] + cm[7,4] + cm[7,5] + cm[7,7]
    ob_fn = cm[1,0] + cm[1,2] + cm[1,3] + cm[1,6] + cm[4,0] + cm[4,2] + cm[4,3] + cm[4,6] + cm[5,0] + cm[5,2] + cm[5,3] + cm[5,6] + cm[7,0] + cm[7,2] + cm[7,3] + cm[7,6]
    ob_fp = cm[0,1] + cm[0,4] + cm[0,5] + cm[0,7] + cm[2,1] + cm[2,4] + cm[2,5] + cm[2,7] + cm[3,1] + cm[3,4] + cm[3,5] + cm[3,7] + cm[6,1] + cm[6,4] + cm[6,5] + cm[6,7]
    eb_tp = cm[2,2] + cm[2,4] + cm[2,6] + cm[2,7] + cm[4,2] + cm[4,4] + cm[4,6] + cm[4,7] + cm[6,2] + cm[6,4] + cm[6,6] + cm[6,7] + cm[7,2] + cm[7,4] + cm[7,6] + cm[7,7]
    eb_fn = cm[2,0] + cm[2,1] + cm[2,3] + cm[2,5] + cm[4,0] + cm[4,1] + cm[4,3] + cm[4,5] + cm[6,0] + cm[6,1] + cm[6,3] + cm[6,5] + cm[7,0] + cm[7,1] + cm[7,3] + cm[7,5]
    eb_fp = cm[0,2] + cm[0,4] + cm[0,6] + cm[0,7] + cm[1,2] + cm[1,4] + cm[1,6] + cm[1,7] + cm[3,2] + cm[3,4] + cm[3,6] + cm[3,7] + cm[5,2] + cm[5,4] + cm[5,6] + cm[5,7]
    sr_tp = cm[3,3] + cm[3,5] + cm[3,6] + cm[3,7] + cm[5,3] + cm[5,5] + cm[5,6] + cm[5,7] + cm[6,3] + cm[6,5] + cm[6,6] + cm[6,7] + cm[7,3] + cm[7,5] + cm[7,6] + cm[7,7]
    sr_fn = cm[3,0] + cm[3,1] + cm[3,2] + cm[3,4] + cm[5,0] + cm[5,1] + cm[5,2] + cm[5,4] + cm[6,0] + cm[6,1] + cm[6,2] + cm[6,4] + cm[7,0] + cm[7,1] + cm[7,2] + cm[7,4]
    sr_fp = cm[0,3] + cm[0,5] + cm[0,6] + cm[0,7] + cm[1,3] + cm[1,5] + cm[1,6] + cm[1,7] + cm[2,3] + cm[2,5] + cm[2,6] + cm[2,7] + cm[4,3] + cm[4,5] + cm[4,6] + cm[4,7]
    ob_precision = ob_tp / (ob_tp + ob_fp)
    ob_recall = ob_tp / (ob_tp + ob_fn)
    ob_f1 = (2*ob_precision*ob_recall) / (ob_precision + ob_recall)
    eb_precision = eb_tp / (eb_tp + eb_fp)
    eb_recall = eb_tp / (eb_tp + eb_fn)
    eb_f1 = (2*eb_precision*eb_recall) / (eb_precision + eb_recall)
    sr_precision = sr_tp / (sr_tp + sr_fp)
    sr_recall = sr_tp / (sr_tp + sr_fn)
    sr_f1 = (2*sr_precision*sr_recall) / (sr_precision + sr_recall) 

    print("Test OB_precision: {:.3f}".format(ob_precision))
    print("Test OB_recall: {:.3f}".format(ob_recall))
    print("Test OB_F1: {:.3f}".format(ob_f1))
    print("Test EB_precision: {:.3f}".format(eb_precision))
    print("Test EB_recall: {:.3f}".format(eb_recall))
    print("Test EB_F1: {:.3f}".format(eb_f1))
    print("Test SR_precision: {:.3f}".format(sr_precision))
    print("Test SR_recall: {:.3f}".format(sr_recall))
    print("Test SR_F1: {:.3f}".format(sr_f1))

