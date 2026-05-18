"""Entry point for the Vehicle Speed Detection System."""

import os
import sys

from src.main import VehicleSpeedDetectionSystem

# Input and output configuration
INPUT_VIDEO = os.path.join("input", "footage.mp4")
OUTPUT_VIDEO = os.path.join("output", "footage_processed.mp4")


def main():
    """Main entry point."""
    # Validate input file
    if not os.path.isfile(INPUT_VIDEO):
        print(f"Error: Input file not found: {INPUT_VIDEO}")
        print("Please place your 'footage.mp4' file in the 'input/' folder.")
        sys.exit(1)

    # Create output directory if needed
    os.makedirs("output", exist_ok=True)

    print("=" * 60)
    print("  Vehicle Speed Detection System")
    print("=" * 60)
    print(f"  Input:  {INPUT_VIDEO}")
    print(f"  Output: {OUTPUT_VIDEO}")
    print("=" * 60)

    # Run the system
    system = VehicleSpeedDetectionSystem(INPUT_VIDEO, OUTPUT_VIDEO)
    system.run()


if __name__ == "__main__":
    main()
