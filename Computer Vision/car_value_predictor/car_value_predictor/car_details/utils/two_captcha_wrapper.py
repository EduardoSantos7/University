import json
import os
import requests
from time import sleep
import logging
from dotenv import load_dotenv


load_dotenv()

ERROR = "ERROR"


class TwoCaptchaWrapper:
    '''
    2captcha service wrapper
    '''

    def __init__(self):
        self.api_key = os.getenv('TWO_CAPTCHA_API_KEY', None)
        self.session = requests.Session()

    def post_image_task(self, file_path):
        """ Method that posts the petition for solving the captcha
        :params file_path: String with the path to the captcha image
        :return: String with the captcha response or False if an error
        """
        url = 'http://2captcha.com/in.php'
        input_file = {'file': open(file_path, 'rb')}
        data = {'key': self.api_key, 'method': 'post', 'json': 1}
        response = self.session.post(url, files=input_file, data=data)
        id_answer = self.handle_id_answer(response.text)
        finished = False
        for _ in range(20):  # For making up to 120 seconds of waits
            if 'CAPCHA_NOT_READY' not in response.text:
                finished = True
                break
            # Time Requested by the web page
            sleep(6)
            response = self.session.post(url, files=input_file, data=data)
            id_answer = self.handle_id_answer(response.text)

        if not finished:
            return False

        return id_answer

    def get_image_response(self, captcha_id):
        """ Method that obtains the solution for the captcha sent
        :param captcha_id: Integer with the captcha petition
        :return String with the solution from the captcha or False is an error occurred
        """
        url = 'http://2captcha.com/res.php'
        data = {'key': self.api_key, 'action': 'get',
                'id': captcha_id, 'json': 1}
        response = self.session.post(url, data=data)
        json_response = json.loads(response.text)
        recaptcha_answer = json_response["request"]
        finished = False
        for _ in range(20):  # For making up to 120 seconds of waits
            if 'CAPCHA_NOT_READY' not in response.text:
                finished = True
                break
            # Time Requested by the web page
            sleep(6)
            response = self.session.post(url, data=data)
            json_response = json.loads(response.text)
            recaptcha_answer = json_response["request"]

        if not finished:
            return False

        return recaptcha_answer

    def obtain_image_captcha(self, file_path):
        """Method for obtaining the response from the image captcha to 2captcha
        :params file_path: Path to the image to analyze
        :params county: String with the county code
        :return Text obtained from the image by the service
        """
        id_answer = self.post_image_task(file_path)
        if not id_answer:
            message = f"Unable to obtain response for request of captcha from 2Captcha"
            print(message)
            return None

        try:
            captcha_id = int(id_answer)
        except ValueError:
            message = f"Error in captcha request from 2Captcha: {id_answer}"
            print(message)
            return None

        recaptcha_answer = self.get_image_response(captcha_id)
        if not recaptcha_answer:
            message = f"Unable to obtain response for captcha image solution from 2Captcha"
            print(message)
            return None

        print(f"Output from 2Captcha {recaptcha_answer}")
        return recaptcha_answer

    def solve_image_captcha(self, captcha_tmp_path):
        """Use 2captcha to get captcha solution
        :param captcha_tmp_path: String with the path to the image
        :returns: Captcha solution as string
        """
        # Get solution and apply it
        for i in range(1, 4):
            print(f"Attempt #{i} for recaptcha solution")
            solution = self.obtain_image_captcha(captcha_tmp_path)
            print(f'this {solution}')
            if solution and ERROR not in solution.upper():
                break

        if solution is None or ERROR in solution.upper():
            if not solution:
                message = f"2Captcha service didn't return a response for the captcha"
            else:
                message = f"Error in captcha solution from 2Captcha: {solution}"
            return None

        print("Captcha solution: {}".format(solution))
        return solution

    def handle_id_answer(self, response_text):
        """ Function for handling the id_answer from the response in a safer way
        :param: response_text: String with the response (either json or plain text)
        :return: String with the id from the text or None if not found
        """
        id_answer = None
        try:
            json_response = json.loads(response_text)
            id_answer = json_response["request"]
        except json.decoder.JSONDecodeError:
            elements_splitted = response_text.split("|")
            if elements_splitted and len(elements_splitted) >= 2:
                id_answer = elements_splitted[1]
        return id_answer
