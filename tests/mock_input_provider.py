from yget.input_provider import InputProvider

class MockInputProvider(InputProvider):
    def __init__(self, input_delegate, password_delegate):
        super(MockInputProvider, self).__init__()

        self.input_delegate = input_delegate
        self.password_delegate = password_delegate

    def get_input(self, label):
        return self.input_delegate(label)

    def get_password(self, label):
        return self.password_delegate(label)
