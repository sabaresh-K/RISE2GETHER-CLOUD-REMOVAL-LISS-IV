import torch
from src.models import CloudRemovalGenerator, SARCycleGANGenerator, SARCycleGANDiscriminator

def test_models():
    print("=== Testing CloudClear Model Engines ===")
    
    # 1. Test Engine 1: CloudRemovalGenerator
    gen1 = CloudRemovalGenerator()
    x_opt = torch.randn(2, 3, 256, 256)
    out1 = gen1(x_opt)
    print(f"Engine 1 Output Shape: {out1.shape} (Expected: [2, 3, 256, 256])")
    assert out1.shape == (2, 3, 256, 256), "Engine 1 output shape mismatch!"
    
    # 2. Test Engine 2: SARCycleGANGenerator with 5-channel paired SAR input
    gen2 = SARCycleGANGenerator(in_channels=5, out_channels=3)
    x_paired = torch.randn(2, 5, 256, 256)
    out2 = gen2(x_paired)
    print(f"Engine 2 Paired Output Shape: {out2.shape} (Expected: [2, 3, 256, 256])")
    assert out2.shape == (2, 3, 256, 256), "Engine 2 paired output shape mismatch!"

    # 3. Test Engine 2 with 3-channel input (Synthetic SAR mode)
    out2_synth = gen2(x_opt)
    print(f"Engine 2 Synthetic Output Shape: {out2_synth.shape} (Expected: [2, 3, 256, 256])")
    assert out2_synth.shape == (2, 3, 256, 256), "Engine 2 synthetic output shape mismatch!"

    # 4. Test PatchGAN Discriminator
    disc = SARCycleGANDiscriminator(in_channels=3)
    disc_score = disc(out2)
    print(f"PatchGAN Discriminator Score Shape: {disc_score.shape} (Expected: [2, 1, 16, 16])")
    assert disc_score.shape == (2, 1, 16, 16), "Discriminator output shape mismatch!"

    print("SUCCESS: All Engine 1 & Engine 2 model tests passed successfully!")

if __name__ == "__main__":
    test_models()
