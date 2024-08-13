import os
import heapq
from datetime import datetime
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from transformers import BertForSequenceClassification, BertTokenizer
from sklearn.model_selection import train_test_split
import pandas as pd
import mlflow
from tqdm import tqdm
from dataset import TextDataset  # TextDataset을 별도의 파일에서 import합니다.
from args import get_args

def train_and_evaluate(model_name, file_path, num_labels, max_len, learning_rate, batch_size, epochs):
    # Directory for saving checkpoints
    run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    checkpoint_dir = f"checkpoints/{run_id}"
    os.makedirs(checkpoint_dir, exist_ok=True)

    top_k_checkpoints = []
    heapq.heapify(top_k_checkpoints)

    # Load data
    train_df = pd.read_csv(f'{file_path}/train.csv')    #train
    val_df = pd.read_csv(f'{file_path}/valid.csv')        #validation
    test_df = pd.read_csv(f'{file_path}/test.csv')      #test

    # Extract texts and labels
    train_texts, train_labels = train_df['Article'].values, train_df['label'].values
    val_texts, val_labels = val_df['Article'].values, val_df['label'].values
    # not used
    #test_texts, test_labels = test_df['Article'].values, test_df['label'].values

    #Tokenizer
    tokenizer = BertTokenizer.from_pretrained(model_name)

    train_dataset = TextDataset(train_texts, train_labels, tokenizer, max_len)
    val_dataset = TextDataset(val_texts, val_labels, tokenizer, max_len)

    train_dataloader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    val_dataloader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False)

    model = BertForSequenceClassification.from_pretrained(model_name, num_labels=num_labels)
    model.to(device)

    optimizer = optim.AdamW(model.parameters(), lr=learning_rate)
    criterion = nn.CrossEntropyLoss()

    with mlflow.start_run():
        mlflow.log_param("learning_rate", learning_rate)
        mlflow.log_param("batch_size", batch_size)
        mlflow.log_param("epochs", epochs)

        for epoch in range(epochs):
            model.train()
            total_train_loss = 0

            train_progress_bar = tqdm(total=len(train_dataloader), desc=f"Epoch {epoch+1}/{epochs} [Train]", dynamic_ncols=True, leave=False)

            for batch in train_dataloader:
                input_ids = batch['input_ids'].to(device)
                attention_mask = batch['attention_mask'].to(device)
                labels = batch['labels'].to(device)

                optimizer.zero_grad()

                outputs = model(input_ids=input_ids, attention_mask=attention_mask, labels=labels)
                loss = outputs.loss

                loss.backward()
                optimizer.step()

                total_train_loss += loss.item()

                train_progress_bar.update(1)
                train_progress_bar.set_postfix({"train_loss": loss.item()})

            train_progress_bar.close()

            avg_train_loss = total_train_loss / len(train_dataloader)
            print(f"Epoch {epoch+1}/{epochs}, Train Loss: {avg_train_loss}")
            mlflow.log_metric("train_loss", avg_train_loss, step=epoch)

            # Validation
            model.eval()
            total_val_loss = 0

            val_progress_bar = tqdm(total=len(val_dataloader), desc=f"Epoch {epoch+1}/{epochs} [Validation]", dynamic_ncols=True, leave=False)

            with torch.no_grad():
                for batch in val_dataloader:
                    input_ids = batch['input_ids'].to(device)
                    attention_mask = batch['attention_mask'].to(device)
                    labels = batch['labels'].to(device)

                    outputs = model(input_ids=input_ids, attention_mask=attention_mask, labels=labels)
                    loss = outputs.loss

                    total_val_loss += loss.item()

                    val_progress_bar.update(1)
                    val_progress_bar.set_postfix({"val_loss": loss.item()})

            val_progress_bar.close()

            avg_val_loss = total_val_loss / len(val_dataloader)
            print(f"Epoch {epoch+1}/{epochs}, Validation Loss: {avg_val_loss}")
            mlflow.log_metric("val_loss", avg_val_loss, step=epoch)

            # Save top K checkpoints
            if len(top_k_checkpoints) < 5:
                checkpoint_path = os.path.join(checkpoint_dir, f"model_epoch_{epoch+1}_val_loss_{avg_val_loss:.4f}.pt")
                torch.save(model.state_dict(), checkpoint_path)
                heapq.heappush(top_k_checkpoints, (avg_val_loss, checkpoint_path))
                mlflow.log_artifact(checkpoint_path)

            elif avg_val_loss < top_k_checkpoints[0][0]:
                _, old_checkpoint = heapq.heappop(top_k_checkpoints)
                checkpoint_path = os.path.join(checkpoint_dir, f"model_epoch_{epoch+1}_val_loss_{avg_val_loss:.4f}.pt")
                torch.save(model.state_dict(), checkpoint_path)
                heapq.heappush(top_k_checkpoints, (avg_val_loss, checkpoint_path))
                mlflow.log_artifact(checkpoint_path)

                # Remove old checkpoint file
                os.remove(old_checkpoint)

        print(f"Checkpoints saved to directory: {checkpoint_dir}")

if __name__ == "__main__":
    

    #hyperparameter 설정
    args = ["--model_path", "kpfbert",
            "--train_data_path", "src/data", 
            "--num_classes", "3",
            "--max_len", "512",
            "--lr", "1e-5",
            "--batch_size", "16",
            "--epoch", "5"]

    arg = get_args(args)
    model_name = arg.model_path
    file_path = arg.train_data_path
    num_labels = arg.num_classes
    max_len = arg.max_len
    learning_rate = arg.lr
    batch_size = arg.batch_size
    epochs = arg.epoch

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    mlflow.set_experiment("Kpf-BERT_Classification")

    train_and_evaluate(model_name=model_name, 
                       file_path=file_path,
                       num_labels=num_labels, 
                       max_len=max_len, 
                       learning_rate=learning_rate, 
                       batch_size=batch_size, 
                       epochs=epochs)
