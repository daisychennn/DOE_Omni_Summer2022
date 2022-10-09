import base64

# converts image to base64 string
with open("logos.png", "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read())

#writes binary string to new python file 
with open("imagestring.py","w") as f:
    f.write('imageString = {}'.format(encoded_string))