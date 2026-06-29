from PIL import Image
from pathlib import Path

def resize_image(input_path, output_path):
    try:
        img = Image.open(input_path)

        # Maintain aspect ratio
        img.thumbnail((800, 600))

        # Save with quality
        img.save(output_path, quality=95)

        print("Image resized successfully!")

    except FileNotFoundError:
        print("Error: Image file not found.")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    # Get the folder where this script is located
    current_dir = Path(__file__).parent

    input_image = current_dir / "sample3.jpg"
    output_image = current_dir / "resized_sample.jpg"

    resize_image(input_image, output_image)