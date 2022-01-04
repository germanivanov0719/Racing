from PIL import Image

original_image = Image.open('asphalt-1.jpg')
width, height = original_image.size
resized_image = original_image.resize((250, 250))
resized_image.show()
resized_image.save('asphalt-2.jpg')
