import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms, models
from torch.utils.data import DataLoader

class EmbeddingNet(nn.Module):
    def __init__(self):
        super(EmbeddingNet, self).__init__()
        self.base_model = models.resnet18(pretrained=True)
        self.base_model.fc = nn.Linear(self.base_model.fc.in_features, 128)

    def forward(self, x):
        x = self.base_model(x)
        return nn.functional.normalize(x, p=2, dim=1)

def train_model(data_dir):
    transform = transforms.Compose([
        transforms.Resize((160, 160)),
        transforms.ToTensor()
    ])

    dataset = datasets.ImageFolder(data_dir, transform=transform)
    dataloader = DataLoader(dataset, batch_size=32, shuffle=True)

    model = EmbeddingNet()
    criterion = nn.TripletMarginLoss(margin=1.0)
    optimizer = optim.Adam(model.parameters(), lr=1e-4)

    model.train()
    for epoch in range(10):
        running_loss = 0.0
        for inputs, labels in dataloader:
            anchor, positive, negative = inputs[0::3], inputs[1::3], inputs[2::3]
            optimizer.zero_grad()
            emb_a = model(anchor)
            emb_p = model(positive)
            emb_n = model(negative)
            loss = criterion(emb_a, emb_p, emb_n)
            loss.backward()
            optimizer.step()
            running_loss += loss.item()
        print(f"Epoch {epoch+1}: Loss = {running_loss:.4f}")
    torch.save(model.state_dict(), 'models/embedding_net.pth')

if __name__ == "__main__":
    train_model("data/training_faces")
