from PIL import Image, ImageDraw

img = Image.new('RGB', (200, 200), color=(50, 50, 50))
d = ImageDraw.Draw(img)
d.ellipse([20, 20, 180, 180], fill=(200, 200, 200))
d.polygon([(100, 50), (50, 150), (150, 150)], fill=(100, 100, 100))

img.save('source-photo.jpg')
print("Generated a dummy source-photo.jpg!")
