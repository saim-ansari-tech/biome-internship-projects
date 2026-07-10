import torch

from torch.utils.data import DataLoader

from dataset import SpeakerDataset
from model import ECAPATDNN

from sklearn.metrics import confusion_matrix, classification_report
import matplotlib.pyplot as plt
import pandas as pd

test_dataset = SpeakerDataset(r"biome-internship-projects\
                              Task_5\data\test.csv")

test_loader = DataLoader(test_dataset, batch_size=32, shuffle=False)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

print("Device:", device)

model = ECAPATDNN(num_speakers=100)

model = model.to(device)

model.load_state_dict(torch.load("ecapa_tdnn.pth", map_location=device))
model.eval()

print("Model loaded successfully!")

criterion = torch.nn.CrossEntropyLoss()

running_loss = 0.0
correct = 0
total = 0
all_labels = []
all_predictions = []

with torch.no_grad():

    for mel, label in test_loader:

        mel = mel.to(device)
        label = label.to(device)

        logits, embedding = model(mel)

        loss = criterion(logits, label)

        running_loss += loss.item()

        predictions = torch.argmax(logits, dim=1)

        all_labels.extend(label.cpu().numpy())
        all_predictions.extend(predictions.cpu().numpy())

        correct += (predictions == label).sum().item()

        total += label.size(0)


test_loss = running_loss / len(test_loader)

test_accuracy = 100 * correct / total


report = classification_report(all_labels, all_predictions, output_dict=True)

report_df = pd.DataFrame(report).transpose()

f1_scores = report_df.iloc[:-3]["f1-score"]

plt.figure(figsize=(10, 6))

plt.bar(range(len(f1_scores)), f1_scores)

plt.xlabel("Speaker ID")
plt.ylabel("F1 Score")
plt.title("F1 Score for Each Speaker")

plt.ylim(0, 1)

plt.tight_layout()

plt.savefig("f1_scores.png", dpi=300)

plt.show()

print("\n==============================")
print("Evaluation Results")
print("==============================")
print(f"Test Loss     : {test_loss:.4f}")
print(f"Test Accuracy : {test_accuracy:.2f}%")
print("==============================")

report = classification_report(all_labels, all_predictions, output_dict=True)

report_df = pd.DataFrame(report).transpose()

f1_scores = report_df.iloc[:-3]["f1-score"]

plt.figure(figsize=(10, 6))

plt.bar(range(len(f1_scores)), f1_scores)

plt.xlabel("Speaker ID")
plt.ylabel("F1 Score")
plt.title("F1 Score for Each Speaker")

plt.ylim(0, 1)

plt.tight_layout()

plt.savefig("f1_scores.png", dpi=300)

plt.show()

print("\nClassification Report")
print("==============================")

print(classification_report(all_labels, all_predictions, digits=4))

cm = confusion_matrix(all_labels, all_predictions)

print(cm)
