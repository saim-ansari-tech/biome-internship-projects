import torch
import torch.nn as nn

from blocks import TDNNBlock, SERes2Block, AttentiveStatisticsPooling


class ECAPATDNN(nn.Module):

    def __init__(self, num_speakers):
        super().__init__()

        self.layer1 = TDNNBlock(
            in_channels=80, out_channels=512, kernel_size=5, dilation=1
        )

        self.layer2 = SERes2Block(channels=512, dilation=2)

        self.layer3 = SERes2Block(channels=512, dilation=3)

        self.layer4 = SERes2Block(channels=512, dilation=4)

        self.mfa = TDNNBlock(in_channels=1536,
                             out_channels=1536, kernel_size=1)

        self.pooling = AttentiveStatisticsPooling(channels=1536)

        self.embedding = nn.Sequential(nn.Linear(3072, 192),
                                       nn.BatchNorm1d(192))

        self.classifier = nn.Linear(192, num_speakers)

    def forward(self, x):
        x = x.transpose(1, 2)

        x = self.layer1(x)

        x1 = self.layer2(x)

        x2 = self.layer3(x1)

        x3 = self.layer4(x2)

        x = torch.cat([x1, x2, x3], dim=1)

        x = self.mfa(x)

        x = self.pooling(x)

        embedding = self.embedding(x)

        logits = self.classifier(embedding)

        return logits, embedding
