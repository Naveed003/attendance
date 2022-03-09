from PIL import Image
import base64
from io import BytesIO
import requests


def ImageExtractAndReturn(url, EMPL_ID, CompanyName):

    EMPL_ID = str(EMPL_ID)
    try:
        if "data:image/jpeg;base64," in url:
            base_string = url.replace("data:image/jpeg;base64,", "")
            decoded_img = base64.b64decode(base_string)
            img = Image.open(BytesIO(decoded_img))

        elif "data:image/png;base64," in url:
            base_string = url.replace("data:image/png;base64,", "")
            decoded_img = base64.b64decode(base_string)
            img = Image.open(BytesIO(decoded_img))

        else:
            response = requests.get(url)
            img = Image.open(BytesIO(response.content)).convert("RGB")

        status = "Image has been succesfully sent to the server."
    except Exception as e:
        status = "Error! = " + str(e)

    return img
