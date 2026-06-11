from PIL import Image

def resize_image(input_path, output_path):
    img = Image.open(input_path)

    resized_img = img.resize((800, 600))

    resized_img.save(output_path)

    print("Image resized successfully!")

resize_image("sample.jpg", "resized_sample.jpg")