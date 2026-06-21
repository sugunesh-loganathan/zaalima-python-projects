from PIL import Image

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
    resize_image(
        "Project-1/image-processing/sample1.jpg",
        "Project-1/image-processing/resized_sample.jpg"
    )