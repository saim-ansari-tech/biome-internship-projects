import torch
import torch.nn as nn


class TDNNBlock(nn.Module):
    def __init__(self, in_channels, out_channels, kernel_size, dilation=1):
        super().__init__()
        padding = ((kernel_size - 1) // 2) * dilation

        self.conv = nn.Conv1d(
            in_channels=in_channels,
            out_channels=out_channels,
            kernel_size=kernel_size,
            dilation=dilation,
            padding=padding,
        )

        self.bn = nn.BatchNorm1d(out_channels)

        self.relu = nn.ReLU()

    def forward(self, x):
        x = self.conv(x)
        x = self.bn(x)
        x = self.relu(x)

        return x


class Res2Block(nn.Module):
    def __init__(self, channels, scale=8, kernel_size=3, dilation=2):
        super().__init__()

        self.scale = scale
        self.width = channels // scale

        self.blocks = nn.ModuleList()

        for _ in range(scale - 1):
            self.blocks.append(
                TDNNBlock(
                    in_channels=self.width,
                    out_channels=self.width,
                    kernel_size=kernel_size,
                    dilation=dilation,
                )
            )

    def forward(self, x):
        splits = torch.chunk(x, self.scale, dim=1)

        outputs = []

        outputs.append(splits[0])

        for i in range(1, self.scale):
            if i == 1:
                out = self.blocks[i - 1](splits[i])
            else:
                out = self.blocks[i - 1](splits[i] + outputs[-1])

            outputs.append(out)

        return torch.cat(outputs, dim=1)


class SEBlock(nn.Module):

    def __init__(self, channels, bottleneck=128):
        super().__init__()

        self.pool = nn.AdaptiveAvgPool1d(1)

        self.fc1 = nn.Linear(channels, bottleneck)

        self.relu = nn.ReLU()

        self.fc2 = nn.Linear(bottleneck, channels)

        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        s = self.pool(x)

        s = s.squeeze(-1)

        s = self.fc1(s)

        s = self.relu(s)

        s = self.fc2(s)

        s = self.sigmoid(s)

        s = s.unsqueeze(-1)

        return x * s


class SERes2Block(nn.Module):

    def __init__(self, channels, kernel_size=3, dilation=2, scale=8):
        super().__init__()

        self.tdnn1 = TDNNBlock(channels, channels, kernel_size=1, dilation=1)

        self.res2 = Res2Block(
            channels, scale=scale, kernel_size=kernel_size, dilation=dilation
        )

        self.tdnn2 = TDNNBlock(channels, channels, kernel_size=1, dilation=1)

        self.se = SEBlock(channels)

    def forward(self, x):

        identity = x

        out = self.tdnn1(x)

        out = self.res2(out)

        out = self.tdnn2(out)

        out = self.se(out)

        out = out + identity

        return out


class AttentiveStatisticsPooling(nn.Module):

    def __init__(self, channels, bottleneck=128):
        super().__init__()

        self.attention = nn.Sequential(
            nn.Conv1d(channels, bottleneck, kernel_size=1),
            nn.ReLU(),
            nn.BatchNorm1d(bottleneck),
            nn.Conv1d(bottleneck, channels, kernel_size=1),
            nn.Softmax(dim=2),
        )

    def forward(self, x):
        alpha = self.attention(x)

        mean = torch.sum(alpha * x, dim=2)

        var = torch.sum(alpha * (x - mean.unsqueeze(2)) ** 2, dim=2)

        std = torch.sqrt(var + 1e-9)

        pooled = torch.cat([mean, std], dim=1)

        return pooled
