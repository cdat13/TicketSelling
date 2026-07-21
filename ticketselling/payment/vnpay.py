class VNPay:

    def __init__(self):

        self.request_data = {}

        self.response_data = {}

    def add_param(self, key, value):

        self.request_data[key] = value