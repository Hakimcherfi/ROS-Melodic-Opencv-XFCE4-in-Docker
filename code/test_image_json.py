import base64, json
from PIL import Image
from io import BytesIO

# filename = './image.bmp'
# # save to json
# f = open(filename, 'rb')
# img_data = f.read()
# f.close()
# enc_data = base64.b64encode(img_data)
# json.dump({'image':enc_data}, open('./out.json', 'w'))

# load from image
img = json.load(open('./out.json', 'r'))['image']
#dec_data = base64.b64decode(img)

# save image in a file
im = Image.open(BytesIO(base64.b64decode(img)))
im.save('image.png', 'PNG')