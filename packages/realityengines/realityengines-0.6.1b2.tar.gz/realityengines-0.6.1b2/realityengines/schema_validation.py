

class SchemaValidation():
    '''

    '''

    def __init__(self, client, requiredDatasets=None, optionalDatasets=None, valid=None):
        self.client = client
        self.id = requiredDatasets
        self.required_datasets = requiredDatasets
        self.optional_datasets = optionalDatasets
        self.valid = valid

    def __repr__(self):
        return f"SchemaValidation(required_datasets={repr(self.required_datasets)}, optional_datasets={repr(self.optional_datasets)}, valid={repr(self.valid)})"

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.id == other.id

    def to_dict(self):
        return {'required_datasets': self.required_datasets, 'optional_datasets': self.optional_datasets, 'valid': self.valid}
