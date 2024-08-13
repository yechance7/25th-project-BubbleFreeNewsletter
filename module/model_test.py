#단일 문장 혹은 문단을 추론하고 싶으면 아래 코드 이용

import torch
import torch.nn as nn
from transformers import BertForSequenceClassification, BertTokenizer
from dataset import TextDataset
from torch.utils.data import DataLoader
import pandas as pd
from sklearn.metrics import confusion_matrix, recall_score
import tqdm
from args import get_args

def test(model_name, file_path, num_labels, max_len, batch_size):
    #val_loss가 가장 적은 checkpoint 가져오기
    model = BertForSequenceClassification.from_pretrained(model_name, num_labels=num_labels)
    tokenizer = BertTokenizer.from_pretrained(model_name)

    checkpoint_path = "/content/checkpoints/20240809_014107/model_epoch_1_val_loss_0.0278.pt"
    model.load_state_dict(torch.load(checkpoint_path))


    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)

    test_df = pd.read_csv(f'{file_path}/test.csv') 
    test_texts, test_labels = test_df['Article'].values, test_df['label'].values
    tokenizer = BertTokenizer.from_pretrained(model_name)
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

    recall = recall_score(all_labels, all_predictions, average='weighted')
    conf_matrix = confusion_matrix(all_labels, all_predictions)

    accuracy = correct / total
    print(f'Test Accuracy: {accuracy}')
    print(f'Test Recall: {recall}')
    print('Confusion Matrix:')
    print(conf_matrix)

    class_recall = []
    for i in range(conf_matrix.shape[0]):
        true_positive = conf_matrix[i, i]
        false_negative = sum(conf_matrix[i, :]) - true_positive
        recall_value = true_positive / (true_positive + false_negative) if (true_positive + false_negative) > 0 else 0
        class_recall.append(recall_value)

    average_recall = sum(class_recall) / len(class_recall)

    print("Class-wise Recall:", class_recall)
    print("Average Recall:", average_recall)

if __name__ == "__main__":
    args= [
        "--model_name", "kpfbert",
        "--file_path", "src/data",
        "--num_labels", "2",
        "--max_len", "512",
        "--batch_size", "16"
    ]
    arg = get_args(args)

    model_name = arg.model_name
    file_path = arg.file_path
    num_labels = arg.num_labels
    max_len = arg.max_len
    batch_size = arg.batch_size

    test(model_name, file_path, num_labels, max_len, batch_size)
   
    