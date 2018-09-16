from yget.path_validator import PathValidator

class MockPathValidator(PathValidator):
    def __init__(self, validate_directory_predicate, validate_file_predicate):
        super(MockPathValidator, self).__init__()

        self.validate_directory_predicate = validate_directory_predicate
        self.validate_file_predicate = validate_file_predicate

    def validate_directory(self, path):
        return self.validate_directory_predicate(path)

    def validate_file(self, path):
        return self.validate_file_predicate(path)
