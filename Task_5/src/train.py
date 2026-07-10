import torch

from torch.utils.data import DataLoader

from dataset import SpeakerDataset
from model import ECAPATDNN


train_dataset = SpeakerDataset(r"biome-internship-projects\
                               Task_5\data\train.csv")
val_dataset = SpeakerDataset(r"biome-internship-projects\
                             Task_5\data\val.csv")
test_dataset = SpeakerDataset(r"biome-internship-projects\
                              Task_5\data\test.csv")


train_loader = DataLoader(
    train_dataset,
    batch_size=32,
    shuffle=True
)

val_loader = DataLoader(
    val_dataset,
    batch_size=32,
    shuffle=False
)

test_loader = DataLoader(
    test_dataset,
    batch_size=32,
    shuffle=False
)

device = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)

print("Device:", device)


model = ECAPATDNN(
    num_speakers=100
)

model = model.to(device)

criterion = torch.nn.CrossEntropyLoss()

optimizer = torch.optim.Adam(
    model.parameters(),
    lr=0.001
)


num_epochs = 10

for epoch in range(num_epochs):

    model.train()

    running_loss = 0.0
    correct = 0
    total = 0

    for mel, label in train_loader:

        mel = mel.to(device)
        label = label.to(device)

        optimizer.zero_grad()

        logits, embedding = model(mel)

        loss = criterion(logits, label)

        loss.backward()

        optimizer.step()

        running_loss += loss.item()

        predictions = torch.argmax(logits, dim=1)

        correct += (predictions == label).sum().item()

        total += label.size(0)

    epoch_loss = running_loss / len(train_loader)

    epoch_accuracy = 100 * correct / total

    print(
        f"Epoch [{epoch+1}/{num_epochs}] | "
        f"Loss: {epoch_loss:.4f} | "
        f"Accuracy: {epoch_accuracy:.2f}%"
    )


torch.save(
    model.state_dict(),
    "ecapa_tdnn.pth"
)

print("\nTraining Complete!")
print("Model saved as: ecapa_tdnn.pth")
