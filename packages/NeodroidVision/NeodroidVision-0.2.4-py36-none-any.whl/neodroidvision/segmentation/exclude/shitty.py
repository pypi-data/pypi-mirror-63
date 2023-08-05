#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import torch

__author__ = 'Christian Heider Nielsen'
__doc__ = r'''

           Created on 11/10/2019
           '''

from torch import nn
import torch.nn.functional as F


class double_conv(nn.Module):
  """(conv => BN => ReLU) * 2"""

  def __init__(self, in_ch, out_ch):
    super(double_conv, self).__init__()
    self.conv = nn.Sequential(
      nn.Conv2d(in_ch, out_ch, 3, padding=1),
      nn.BatchNorm2d(out_ch),
      nn.ReLU(inplace=True),
      nn.Conv2d(out_ch, out_ch, 3, padding=1),
      nn.BatchNorm2d(out_ch),
      nn.ReLU(inplace=True),
      )

  def forward(self, x):
    x = self.conv(x)
    return x


class inconv(nn.Module):
  def __init__(self, in_ch, out_ch):
    super(inconv, self).__init__()
    self.conv = double_conv(in_ch, out_ch)

  def forward(self, x):
    x = self.conv(x)
    return x


class down(nn.Module):
  def __init__(self, in_ch, out_ch):
    super(down, self).__init__()
    self.mpconv = nn.Sequential(nn.MaxPool2d(2), double_conv(in_ch, out_ch))

  def forward(self, x):
    x = self.mpconv(x)
    return x


class up(nn.Module):
  def __init__(self, in_ch, out_ch, bilinear=True):
    super(up, self).__init__()

    if bilinear:
      self.up = nn.Upsample(scale_factor=2, mode="bilinear", align_corners=True)
    else:
      self.up = nn.ConvTranspose2d(in_ch // 2, in_ch // 2, 2, stride=2)

    self.conv = double_conv(in_ch, out_ch)

  def forward(self, x1, x2):
    x1 = self.up(x1)

    # input is CHW
    diffY = x2.size()[2] - x1.size()[2]
    diffX = x2.size()[3] - x1.size()[3]

    x1 = F.pad(x1, (diffX // 2, diffX - diffX // 2, diffY // 2, diffY - diffY // 2))

    x = torch.cat([x2, x1], dim=1)
    return self.conv(x)


class outconv(nn.Module):
  def __init__(self, in_ch, out_ch):
    super(outconv, self).__init__()
    self.conv = nn.Conv2d(in_ch, out_ch, 1)

  def forward(self, x):
    x = self.conv(x)
    return x


class ShittyUNet(nn.Module):
  def __init__(self, n_channels, n_classes):
    super().__init__()
    self.inc = inconv(n_channels, 64)
    self.down1 = down(64, 128)
    self.down2 = down(128, 256)
    self.down3 = down(256, 512)
    self.down4 = down(512, 512)
    self.up1 = up(1024, 256, False)
    self.up2 = up(512, 128, False)
    self.up3 = up(256, 64, False)
    self.up4 = up(128, 64, False)
    self.outc = outconv(64, n_classes)

  def forward(self, x):
    x1 = self.inc(x)
    x2 = self.down1(x1)
    x3 = self.down2(x2)
    x4 = self.down3(x3)
    x5 = self.down4(x4)
    x = self.up1(x5, x4)
    x = self.up2(x, x3)
    x = self.up3(x, x2)
    x = self.up4(x, x1)
    x = self.outc(x)
    return x, None
