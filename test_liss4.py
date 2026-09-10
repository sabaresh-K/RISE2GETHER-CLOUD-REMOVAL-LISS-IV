from datasets.liss4_dataset import LISS4Dataset
from torch.utils.data import DataLoader

dataset = LISS4Dataset("datasets/liss4")

loader = DataLoader(
    dataset,
    batch_size=4,
    shuffle=True
)

cloudy, clean = next(iter(loader))

print("====================================")
print("Dataset Loaded Successfully")
print("====================================")
print("Cloudy Shape :", cloudy.shape)
print("Clean Shape  :", clean.shape)
print("Cloudy Range :", cloudy.min().item(), cloudy.max().item())
print("Clean Range  :", clean.min().item(), clean.max().item())
