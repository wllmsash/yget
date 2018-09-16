import getpass

class InputProvider(object):
    def get_input(self, label):
        return input(label)

    def get_password(self, label):
        return getpass.getpass(label)
