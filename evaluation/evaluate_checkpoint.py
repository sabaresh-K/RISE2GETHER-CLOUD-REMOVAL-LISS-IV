import os
import csv
import torch

from models import UNetGenerator
from .evaluator import Evaluator
from src.dataset_loader import LISS4CloudDataset


DEVICE = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)


def main():

    print(f"Using device: {DEVICE}")


    # -------------------------------
    # Load Model
    # -------------------------------

    checkpoint_path = (
        "outputs/checkpoints/checkpoint_epoch_100.pth"
    )

    if not os.path.exists(checkpoint_path):
        raise FileNotFoundError(
            checkpoint_path
        )


    checkpoint = torch.load(
        checkpoint_path,
        map_location=DEVICE
    )


    model = UNetGenerator(
        input_nc=3,
        output_nc=3,
        num_downs=8,
        ngf=64
    ).to(DEVICE)


    if "netG_state_dict" in checkpoint:

        model.load_state_dict(
            checkpoint["netG_state_dict"]
        )

    else:

        model.load_state_dict(
            checkpoint
        )


    model.eval()

    print("Model loaded")


    # -------------------------------
    # Dataset
    # -------------------------------

    dataset = LISS4CloudDataset(
        base_dir="data/datasets/RICE",
        dataset_type="RICE1"
    )


    evaluator = Evaluator()

    num_samples = len(dataset)


    print(
        f"Evaluating {num_samples} images..."
    )


    total_metrics = {

        "PSNR": 0.0,
        "SSIM": 0.0,
        "RMSE": 0.0,
        "SAM": 0.0

    }


    results = []


    # -------------------------------
    # Evaluation
    # -------------------------------

    with torch.no_grad():

        for i in range(num_samples):

            # Dataset returns tuple
            cloudy, clear = dataset[i]


            cloudy = (
                cloudy
                .unsqueeze(0)
                .to(DEVICE)
            )


            clear = (
                clear
                .unsqueeze(0)
                .to(DEVICE)
            )


            prediction = model(cloudy)


            scores = evaluator.evaluate(
                prediction.squeeze(0),
                clear.squeeze(0)
            )


            for key in total_metrics:

                total_metrics[key] += scores[key]


            results.append(
                {
                    "Image": i + 1,
                    "PSNR": scores["PSNR"],
                    "SSIM": scores["SSIM"],
                    "RMSE": scores["RMSE"],
                    "SAM": scores["SAM"]
                }
            )


            if (i + 1) % 50 == 0:

                print(
                    f"Processed {i+1}/{num_samples}"
                )


    # -------------------------------
    # Results
    # -------------------------------

    print(
        "\n========== RESULTS ==========\n"
    )


    for key in total_metrics:

        average = (
            total_metrics[key]
            /
            num_samples
        )

        print(
            f"{key}: {average:.5f}"
        )


    print(
        "\n============================="
    )


    # -------------------------------
    # Save CSV
    # -------------------------------

    os.makedirs(
        "outputs",
        exist_ok=True
    )


    csv_file = (
        "outputs/evaluation_metrics.csv"
    )


    with open(
        csv_file,
        "w",
        newline=""
    ) as f:


        writer = csv.DictWriter(
            f,
            fieldnames=[
                "Image",
                "PSNR",
                "SSIM",
                "RMSE",
                "SAM"
            ]
        )


        writer.writeheader()

        writer.writerows(
            results
        )


    print(
        f"Saved: {csv_file}"
    )



if __name__ == "__main__":
    main()
