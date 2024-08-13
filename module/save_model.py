from transformers import BertForSequenceClassification, BertTokenizer
import torch


checkpoint_path = "/content/checkpoints/20240809_014107/model_epoch_1_val_loss_0.0278.pt"
model = BertForSequenceClassification.from_pretrained('kpfbert', num_labels=3)
tokenizer = BertTokenizer.from_pretrained('kpfbert')
model.load_state_dict(torch.load(checkpoint_path))

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

model_save_path = "bubble_free_BERT"
tokenizer_save_path = "bubble_free_tokenizer"

model.save_pretrained(model_save_path)
tokenizer.save_pretrained(tokenizer_save_path)

torch.save(model.state_dict(), f"{model_save_path}/pytorch_model.bin")

print(f"Model saved to {model_save_path}")
print(f"Tokenizer saved to {tokenizer_save_path}")