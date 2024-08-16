#단일 문장 혹은 문단을 추론하고 싶으면 아래 코드 이용

import torch
import torch.nn as nn
from transformers import BertForSequenceClassification, BertTokenizer

model_name_or_path = "bubble_free_BERT"
tokenizer_name_or_path = "bubble_free_tokenizer"

model = BertForSequenceClassification.from_pretrained(model_name_or_path)
tokenizer = BertTokenizer.from_pretrained(tokenizer_name_or_path)

model.eval()

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

sentence = '''
저는 뚱이에요
'''

inputs = tokenizer(sentence, return_tensors="pt", max_length=128, truncation=True, padding="max_length")

inputs = {key: value.to(device) for key, value in inputs.items()}

with torch.no_grad():
    outputs = model(**inputs)
    logits = outputs.logits

    softmax = nn.Softmax(dim=1)  # dim=1은 클래스 차원에 대해 softmax를 적용
    preds = softmax(logits)


preds_rounded = preds.cpu().numpy().round(4)

predicted_class_id = torch.argmax(preds, dim=1).item()
predicted_class = model.config.id2label[predicted_class_id] if model.config.id2label else predicted_class_id

print(f"Predicted class: {predicted_class}")
print("Softmax probabilities:", preds_rounded)
print("Logits:", logits)