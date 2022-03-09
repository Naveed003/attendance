from argparse import _MutuallyExclusiveGroup
from ast import Str
import re
from urllib import response
from PIL import Image
import base64
from io import BytesIO
import requests


def ImageExtractAndSave(urls, EMPL_ID, CompanyName):

    EMPL_ID = str(EMPL_ID)
    file_name_for_base64_data = EMPL_ID

    file_name_for_regular_data = EMPL_ID
    count = 1
    for url in urls:
        try:
            if "data:image/jpeg;base64," in url:
                base_string = url.replace("data:image/jpeg;base64,", "")
                decoded_img = base64.b64decode(base_string)
                img = Image.open(BytesIO(decoded_img))

                file_name = f"Companies/{CompanyName}/" + \
                    file_name_for_base64_data + f"-{count}" + ".jpg"
                img.save(file_name, "jpeg")

            elif "data:image/png;base64," in url:
                base_string = url.replace("data:image/png;base64,", "")
                decoded_img = base64.b64decode(base_string)
                img = Image.open(BytesIO(decoded_img))

                file_name = f"Companies/{CompanyName}/" + \
                    file_name_for_base64_data + f"-{count}" + ".png"
                img.save(file_name, "png")

            else:
                response = requests.get(url)
                img = Image.open(BytesIO(response.content)).convert("RGB")
                file_name = f"Companies/{CompanyName}/" + \
                    file_name_for_regular_data + f"-{count}" + ".jpg"
                img.save(file_name, "jpeg")

            status = "Image has been succesfully sent to the server."
        except Exception as e:
            status = "Error! = " + str(e)

        count += 1

    return status
