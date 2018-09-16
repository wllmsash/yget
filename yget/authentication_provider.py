from .input_provider import InputProvider

class AuthenticationProvider:
    def __init__(self, input_provider):
        self.input_provider = input_provider

    def request_authentication_parameters(self, authentication_params):
        username = self.input_provider.get_input("Username: ")
        password = self.input_provider.get_password("Password: ")

        if not username:
            return False

        authentication_params.update({
            "username": username,
            "password": password
        })

        return True
