from PIL import Image

# Resize image while maintaining aspect ratio
def resize_image(input_path, output_path):
    img = Image.open(input_path)

    # Maximum size 800x600
    img.thumbnail((800, 600))

    img.save(output_path)

    print("Image resized successfully!")

if __name__ == "__main__":
    resize_image(
        "Project-2/image-processing/sample.jpg",
        "Project-2/image-processing/resized_sample.jpg"
    )