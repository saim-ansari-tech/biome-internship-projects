from torch.utils.data import DataLoader
import torch
from dataset import SpeakerDataset
from model import CNNModel
import torch.nn as nn
import torch.optim as optim


def main():
    dataset = SpeakerDataset(
        r"D:\Internship_projects\biome-internship-projects\
            Task5\data\metadata_encoded.csv"
    )

    dataloader = DataLoader(dataset, batch_size=32, shuffle=True)
    print(f"Total Samples : {len(dataset)}")
    print(f"Batch Size    : {dataloader.batch_size}")
    print(f"Total Batches : {len(dataloader)}")

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Device: {device}")

    num_classes = dataset.df["label"].nunique()
    model = CNNModel(num_classes=num_classes)
    model.to(device)

    criterion = nn.CrossEntropyLoss()

    optimizer = optim.SGD(model.parameters(), lr=0.01, momentum=0.9)

    num_epochs = 20

    for epoch in range(num_epochs):
        model.train()
        running_loss = 0.0

        for batch_idx, (features, labels) in enumerate(dataloader):
            features = features.to(device)
            labels = labels.to(device)

            output = model(features)

            loss = criterion(output, labels)

            optimizer.zero_grad()

            loss.backward()

            optimizer.step()

            running_loss += loss.item()
            epoch_loss = running_loss / (batch_idx + 1)

            print(
                f"Epoch [{epoch+1}/{num_epochs}] | "
                f"Batch [{batch_idx+1}/{len(dataloader)}] | "
                f"Batch Loss: {loss.item():.4f} | "
                f"Loss: {loss.item():.4f}"
            )

        epoch_loss = running_loss / len(dataloader)

        print("-" * 60)
        print(f"Epoch [{epoch+1}/{num_epochs}] Completed")
        print(f"Average Loss: {epoch_loss:.4f}")
        print("-" * 60)

    torch.save(model.state_dict(), "speaker_identification_model.pth")

    print("Traning Completed!")
    print("Model saved successfully!")


if __name__ == "__main__":
    main()
