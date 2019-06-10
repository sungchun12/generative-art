import PIL, random, sys  # import native modules
from PIL import Image, ImageDraw  # import pillow image drawing modules

origDimension = 1500  # sets default image size
r = lambda: random.randint(50, 215)  # rgb range
rc = lambda: (r(), r(), r())  # rgb coordinates
listSym = []  # symmetry square color tracking list


def create_square(border, draw, randColor, element, size):
    if element == int(
        size / 2
    ):  # if element equals size of sprite/2, draw a rectangle that fits in square border, random color
        draw.rectangle(border, randColor)
    elif (
        len(listSym) == element + 1
    ):  # if length of symmetrylist == element + 1, draw a rectangle within the square border and populate the symmetry list TODO
        draw.rectangle(border, listSym.pop())
    else:  # else append the random color square to the symmetry tracking list and draw a random color
        listSym.append(randColor)
        draw.rectangle(border, randColor)


def create_invader(border, draw, size):
    x0, y0, x1, y1 = border  # coordinates for invader creations
    squareSize = (x1 - x0) / size  # size of the full border for invader
    randColors = [
        rc(),
        rc(),
        rc(),
        (0, 0, 0),
        (0, 0, 0),
        (0, 0, 0),
    ]  # choose random colors based on lambda function "rc()" defined above
    i = 1
    for y in range(0, size):
        i *= -1  # equivalent to i = i*-1, create the opposite side for symmetry
        element = 0  # starting point square
        for x in range(
            0, size
        ):  # loop through to create color squares within the sprite border
            topLeftX = (
                x * squareSize + x0
            )  # pass through x,y coordinates for square size
            topLeftY = y * squareSize + y0
            botRightX = topLeftX + squareSize
            botRightY = topLeftY + squareSize
            create_square(
                (topLeftX, topLeftY, botRightX, botRightY),
                draw,
                random.choice(randColors),
                element,
                size,
            )  # creates individual pixel squares within the sprite borders
            if element == int(size / 2) or element == 0:
                i *= -1
            element += i


def main(size, invaders, imgSize):
    """Main orchestrator function"""
    origDimension = imgSize  # capture the image size
    origImage = Image.new(
        "RGB", (origDimension, origDimension)
    )  # create square border dimensions for full image
    draw = ImageDraw.Draw(origImage)  # draw within the full image size
    invaderSize = (
        origDimension / invaders
    )  # full image size divided by number of invaders
    padding = invaderSize / size  # creates black buffer space between sprites
    for x in range(
        0, invaders
    ):  # nested loops to create coordinate-based grid for sprite borders with black buffer space between sprites
        for y in range(0, invaders):
            topLeftX = (
                x * invaderSize + padding / 2
            )  # x-coordinate*invader size + padding/2
            topLeftY = y * invaderSize + padding / 2
            botRightX = topLeftX + invaderSize - padding
            botRightY = topLeftY + invaderSize - padding
            create_invader(
                (topLeftX, topLeftY, botRightX, botRightY), draw, size
            )  # creates the invader based on coordinates, full image size, and size of sprite dimensions
    origImage.save(
        "C:/Users/sungwon.chung/Desktop/generative_art/"
        + "Example-"
        + str(size)
        + "x"
        + str(size)
        + "-"
        + str(invaders)
        + "-"
        + str(imgSize)
        + ".jpg"
    )  # save to path


# how do I parameterize these arguments through a post api request. I'll likekly need to use the requests module
if __name__ == "__main__":
    main(
        int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    )  # system arguments are [SPRITE_DIMENSIONS] [NUMBER] [IMAGE_SIZE], example: python spritething.py 5 5 1900, only odd numbers work

# the below is the way I'd want to see users interact with the API
# I need to change "Content-Type" to image/png for method response and integration response
# Figure out how to parse json
# design pattern would include a separate script containing other functions
# lambda handler will use each function above to execute
# create a function to parse the json(maybe within the handler)
# have the handler save the image in a temporary directory for the api gateway to point to
# open the file
# the handler will have (event, context) as variables, figure out what they mean for api gateway
# I'll have to include input parameters  as json

# def getImage(event, context):
#   img_jpg = open(’./test.jpg’, ‘rb’).read()
#   out_b64 = b64encode(img_jpg)
#   return {
#     ‘statusCode’: 200,
#     ‘body’: out_b64,
#     ‘isBase64Encoded’: True,
#     ‘headers’: {‘Content-Type’: ‘image/jpeg’},
#     }
# import requests

# input_json = {
#     "Q1": "q1_other",
#     "Q2": "q2_25_29",
#     "Q3": "q3_united_",
#     "Q4": "q4_other",
#     "Q6": "q6_data_sc",
#     "Q7": "q7_other2",
#     "Q8": "q8_2_3",
#     "Q10": "q10_we_rec",
#     "q11_analyz": "on",
#     "q11_run_a_": "on",
#     "q11_build_": "on",
#     "q15_amazon": "on",
#     "other": "on",
#     "q16_python": "on",
#     "q16_sql": "on",
#     "Q23": "q23_25_to_",
#     "q31_catego": "on",
#     "q31_geospa": "on",
#     "q31_numeri": "on",
#     "q31_tabula": "on",
#     "q31_text_d": "on",
#     "q31_time_s": "on",
#     "q42_revenu": "on"
# }


# header = {'Content-Type': 'application/x-www-form-urlencoded'}
# url = 'https://tk9k0fkvyj.execute-api.us-east-2.amazonaws.com/default/top20-predictor'

# test = requests.post(url, params=input_json, headers=header).json()

# print(test)
