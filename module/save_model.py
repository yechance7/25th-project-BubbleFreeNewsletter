from transformers import BertForSequenceClassification, BertTokenizer
import torch

checkpoint_path = "checkpoints/20240816_122359/model_epoch_4_val_loss_0.1095.pt"
model = BertForSequenceClassification.from_pretrained('kpfbert', num_labels=2)
tokenizer = BertTokenizer.from_pretrained('kpfbert')
model.load_state_dict(torch.load(checkpoint_path))

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# 모델의 모든 파라미터에 .contiguous()를 적용
for param in model.parameters():
    param.data = param.data.contiguous()

model_save_path = "bubble_free_BERT"
tokenizer_save_path = "bubble_free_tokenizer"

# 모델 저장
model.save_pretrained(model_save_path)
tokenizer.save_pretrained(tokenizer_save_path)

# PyTorch 모델 상태 저장
torch.save(model.state_dict(), f"{model_save_path}/pytorch_model.bin")

print(f"Model saved to {model_save_path}")
print(f"Tokenizer saved to {tokenizer_save_path}")
