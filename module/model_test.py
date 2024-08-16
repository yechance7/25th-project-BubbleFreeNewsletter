#모델 성능 지표 평가

import torch
import torch.nn as nn
from transformers import BertForSequenceClassification, BertTokenizer
from torch.utils.data import DataLoader
import pandas as pd
from sklearn.metrics import accuracy_score, precision_score, confusion_matrix, recall_score, f1_score
from tqdm import tqdm
from dataset import TextDataset
from test_plot import plot_metrics
from args import get_args


def test(model_path, data_path, ckpt, num_labels, max_len, batch_size):
    #val_loss가 가장 적은 checkpoint 가져오기
    model = BertForSequenceClassification.from_pretrained(model_path, num_labels=num_labels)
    tokenizer = BertTokenizer.from_pretrained(model_path)

    checkpoint_path = ckpt
    state_dict = torch.load(checkpoint_path)

    # 모델에 state_dict 로드
    model.load_state_dict(state_dict)


    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)

    test_df = pd.read_csv(f'{data_path}/test.csv')
    test_texts, test_labels = test_df['Article'].values, test_df['label'].values
    tokenizer = BertTokenizer.from_pretrained(model_path)
    test_dataset = TextDataset(test_texts, test_labels, tokenizer, max_len)
    test_dataloader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)

    model.eval()

    correct = 0
    total = 0
    all_labels = []
    all_predictions = []

    with torch.no_grad():
        test_progress_bar = tqdm(test_dataloader, desc="Testing", dynamic_ncols=True, leave=False)

        for batch in test_progress_bar:
            input_ids = batch['input_ids'].to(device)
            attention_mask = batch['attention_mask'].to(device)
            labels = batch['labels'].to(device)

            outputs = model(input_ids, attention_mask=attention_mask)
            logits = outputs.logits
            predicted = torch.argmax(logits, dim=1)

            all_labels.extend(labels.cpu().numpy())
            all_predictions.extend(predicted.cpu().numpy())

            total += labels.size(0)
            correct += (predicted == labels).sum().item()

            test_progress_bar.set_postfix({"accuracy": correct / total})

    conf_matrix = confusion_matrix(all_labels, all_predictions)
    accuracy = accuracy_score(all_labels, all_predictions)
    precision = precision_score(all_labels, all_predictions, average='macro')
    recall = recall_score(all_labels, all_predictions, average='macro')
    f1 = f1_score(all_labels, all_predictions, average='macro')

    # Print metrics
    print(f'Test Accuracy: {accuracy}')
    print(f'Test Precision: {precision}')
    print(f'Test Recall: {recall}')
    print(f'Test F1 Score: {f1}')
    print('Confusion Matrix:')
    print(conf_matrix)

    # Plot metrics
    plot_metrics(conf_matrix, accuracy, precision, recall, f1)



if __name__ == "__main__":
    args= [
        "--model_path", "kpfbert",
        "--data_path", "src/data",
        "--num_classes", "2",
        "--max_len", "512",
        "--batch_size", "16"
    ]
    arg = get_args(args)

    model_path = arg.model_path
    data_path = arg.data_path
    num_labels = arg.num_classes
    max_len = arg.max_len
    batch_size = arg.batch_size
    ckpt = 'checkpoints/20240816_122359/model_epoch_4_val_loss_0.1095.pt'

    test(model_path, data_path, ckpt, num_labels, max_len, batch_size)
   
    