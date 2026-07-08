import torch.nn as nn


class CNNModel(nn.Module):
    def __init__(self, num_classes):
        super().__init__()
        self.block1 = nn.Sequential(
            nn.Conv2d(
                in_channels=1, out_channels=96,
                kernel_size=7, stride=2, padding=0
            ),
            nn.BatchNorm2d(96),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=3, stride=2),
        )

        self.block2 = nn.Sequential(
            nn.Conv2d(
                in_channels=96, out_channels=256,
                kernel_size=5, stride=2, padding=0
            ),
            nn.BatchNorm2d(256),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=3, stride=2),
        )

        self.block3 = nn.Sequential(
            nn.Conv2d(
                in_channels=256, out_channels=384,
                kernel_size=3, stride=1, padding=1
            ),
            nn.BatchNorm2d(384),
            nn.ReLU(inplace=True),
        )

        self.block4 = nn.Sequential(
            nn.Conv2d(
                in_channels=384, out_channels=256,
                kernel_size=3, stride=1, padding=1
            ),
            nn.BatchNorm2d(256),
            nn.ReLU(inplace=True),
        )

        self.block5 = nn.Sequential(
            nn.Conv2d(
                in_channels=256, out_channels=256,
                kernel_size=3, stride=1, padding=1
            ),
            nn.BatchNorm2d(256),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=(5, 3), stride=(3, 2)),
        )

        self.fc6 = nn.Sequential(
            nn.Conv2d(in_channels=256, out_channels=4096,
                      kernel_size=(4, 1), stride=1),
            nn.BatchNorm2d(4096),
            nn.ReLU(inplace=True),
        )

        self.avgpool = nn.AdaptiveAvgPool2d((1, 1))

        self.fc7 = nn.Sequential(
            nn.Conv2d(in_channels=4096, out_channels=1024, kernel_size=1),
            nn.BatchNorm2d(1024),
            nn.ReLU(inplace=True),
        )

        self.fc8 = nn.Conv2d(in_channels=1024,
                             out_channels=num_classes,
                             kernel_size=1)

    def forward(self, x):
        x = self.block1(x)
        x = self.block2(x)
        x = self.block3(x)
        x = self.block4(x)
        x = self.block5(x)

        x = self.fc6(x)
        x = self.avgpool(x)
        x = self.fc7(x)
        x = self.fc8(x)
        x = x.squeeze(-1).squeeze(-1)

        return x
