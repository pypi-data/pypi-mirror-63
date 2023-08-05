"""
Train an encoder/decoder on the MNIST dataset.
"""

import os

import numpy
import torch
import torch.optim as optim
from PIL import Image
from neodroidvision.reconstruction import make_vq_vae
from samples.regression.reconstruction.vq_vae2.mnist.data_loader import load_images

from neodroidvision import PROJECT_APP_PATH

DEVICE = torch.device("cuda")
VAE_PATH = PROJECT_APP_PATH.user_data / "vae.pt"

LATENT_SIZE = 16
LATENT_COUNT = 32


def main():
  vae = make_vq_vae(LATENT_SIZE, LATENT_COUNT)

  if os.path.exists(VAE_PATH):
    vae.load_state_dict(torch.load(VAE_PATH, map_location="cpu"))

  vae.to(global_torch_device())
  optimizer = optim.Adam(vae.parameters())

  for i, batch in enumerate(load_images()):
    batch = batch.to(global_torch_device())
    terms = vae(batch)
    print(
      f'step {i:d}: loss={terms["loss"].item():f} '
      f'mse={terms["losses"][-1].item():f}'
      )
    optimizer.zero_grad()
    terms["loss"].backward()
    optimizer.step()
    vae.revive_dead_entries()
    if not i % 10:
      torch.save(vae.state_dict(), VAE_PATH)
    if not i % 100:
      save_reconstructions(batch, terms["reconstructions"][-1])


def save_reconstructions(batch, decoded):
  batch = batch.detach().permute(0, 2, 3, 1).contiguous()
  decoded = decoded.detach().permute(0, 2, 3, 1).contiguous()
  input_images = (numpy.concatenate(batch.cpu().numpy(), axis=0) * 255).astype(
    numpy.uint8
    )
  output_images = numpy.concatenate(decoded.cpu().numpy(), axis=0)
  output_images = (numpy.clip(output_images, 0, 1) * 255).astype(numpy.uint8)
  joined = numpy.concatenate([input_images[..., 0], output_images[..., 0]], axis=1)
  Image.fromarray(joined).save(PROJECT_APP_PATH.user_data / "reconstructions.png")


if __name__ == "__main__":
  main()
