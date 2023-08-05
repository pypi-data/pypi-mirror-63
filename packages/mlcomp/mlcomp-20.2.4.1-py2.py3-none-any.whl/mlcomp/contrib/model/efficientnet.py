from efficientnet_pytorch import EfficientNet as _EfficientNet

import torch.nn as nn

from mlcomp.contrib.torch.layers import LambdaLayer


class EfficientNet(nn.Module):
    def __init__(self, variant, num_classes, pretrained=True, activation=None):
        super().__init__()
        if 'efficientnet' not in variant:
            variant = f'efficientnet-{variant}'

        if pretrained:
            model = _EfficientNet.from_pretrained(variant,
                                                  num_classes=num_classes)
        else:
            model = _EfficientNet.from_name(variant, {
                'num_classes': num_classes
            })
        self.model = model

        self.model._fc = nn.Sequential(
            LambdaLayer(lambda x: x.unsqueeze_(0)),
            nn.AdaptiveAvgPool1d(self.model._fc.in_features),
            LambdaLayer(lambda x: x.squeeze_(0).view(x.size(0), -1)),
            self.model._fc
        )

        if callable(activation) or activation is None:
            self.activation = activation
        elif activation == 'softmax':
            self.activation = nn.Softmax(dim=1)
        elif activation == 'sigmoid':
            self.activation = nn.Sigmoid()
        else:
            raise ValueError(
                'Activation should be "sigmoid"/"softmax"/callable/None')

    def forward(self, x):
        res = self.model(x)
        if isinstance(res, tuple):
            res = res[0]
        if self.activation:
            res = self.activation(res)
        return res


__all__ = ['EfficientNet']
