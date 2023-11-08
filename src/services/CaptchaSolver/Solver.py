# github.com/angelillija

import random
import time
import cv2
from io import BufferedReader
from numpy import uint8, frombuffer
from httpx import Client as Session


class TikTokCaptchaSolver:
    def __init__(self, device_id: int, install_id: int) -> None:
        self.session = Session()
        self.base_url = "https://rc-verification-i18n.tiktokv.com"
        self.params = {
            "lang":"en",
            "app_name":"",
            "h5_sdk_version":"2.31.5",
            "h5_sdk_use_type":"cdn",
            "sdk_version":"3.8.15",
            "iid":install_id,
            "did":device_id,
            "device_id":device_id,
            "ch":"web_text",
            "aid":"1988",
            "os_type":"2",
            "mode":"slide",
            "tmp":"1699328825003",
            "platform":"pc",
            "webdriver":"true",
            "fp":"verify_lonshekq_A9Nk5NjE_b0I2_4SQS_BeAu_rjrTPUYfJlnR",
            "type":"verify",
            "subtype":"slide",
            "challenge_code":"99999",
            "os_name":"mac",
            "h5_check_version":"3.8.15",
            "region":"ttp",
            "triggered_region":"ttp"
        }
        
        # https://verification.us.tiktok.com/captcha/verify?lang=en&app_name=&h5_sdk_version=2.31.5&h5_sdk_use_type=cdn&sdk_version=3.8.15&iid=0&did=7298561532169782830&device_id=7298561532169782830&ch=web_text&aid=1988&os_type=2&mode=slide&tmp=1699328825003&platform=pc&webdriver=true&fp=verify_lonshekq_A9Nk5NjE_b0I2_4SQS_BeAu_rjrTPUYfJlnR&type=verify&detail=cLPzYw65-sTl4Rfl6n-QSQblC-XsBJIxDFEE78xOuzbdoxjCJE7ZckNZaBidrGpXF1HPV7vKSS2HFeauOQoFXGMx9Fksv7cG6k9u2nnRDVJpAacwVZFLaEHR0kbFIJr4bqTWPabBFQbYr45L2hrLnUv6rXENVTB0wLpjCgNy2HgDQP9DsKARSmPRmtpdn1tKunlBtwKl0-IF-bGsoetk0yTFFcB4v5NS5lHAmIL6*975iFl1NEsVNwz69AAZV06M3uUvuBI3b9r2IH8FZ9rQZ8Ll--p2d*JzOBlOmGBSMoe5SwMTwrkeT05FfiEy2mq6xKMS0n2URZbOLDLMi8rJru2taJyh*KRSLhPBuONqfVgiDcVj8hP7isiOwFJGac7r0qez-vY48CCDPXtILQ..&server_sdk_env=%7B%22idc%22:%22useast5%22,%22region%22:%22US-TTP%22,%22server_type%22:%22business%22%7D&subtype=slide&challenge_code=99999&os_name=mac&h5_check_version=3.8.15&region=ttp&triggered_region=ttp


    @staticmethod
    def process_image(buffer: BufferedReader):
        nparr = frombuffer(buffer, uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        blurred = cv2.GaussianBlur(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY), (3, 3), 0)
        return cv2.addWeighted(
            cv2.convertScaleAbs(cv2.Sobel(blurred, cv2.CV_16S, 1, 0, ksize=3)),
            0.5,
            cv2.convertScaleAbs(cv2.Sobel(blurred, cv2.CV_16S, 0, 1, ksize=3)),
            0.5,
            0,
        )

    def solve_captcha(self) -> dict:
        captcha = self.session.get(
            url=f"{self.base_url}/captcha/get", params=self.params
        ).json()
        puzzle, piece = [
            self.process_image(
                self.session.get(captcha["data"]["question"][f"url{url}"]).content
            )
            for url in [1, 2]
        ]

        time.sleep(1)

        randlength = round(random.uniform(50, 100))
        max_loc = cv2.minMaxLoc(cv2.matchTemplate(puzzle, piece, cv2.TM_CCOEFF_NORMED))[
            3
        ][0]

        return self.session.post(
            url=f"{self.base_url}/captcha/verify",
            params=self.params,
            json={
                "modified_img_width": 552,
                "id": captcha["data"]["id"],
                "mode": "slide",
                "reply": [
                    {
                        "relative_time": (i * randlength),
                        "x": round(max_loc / (randlength / i)),
                        "y": captcha["data"]["question"]["tip_y"],
                    }
                    for i in range(1, randlength)
                ],
            },
        ).json()