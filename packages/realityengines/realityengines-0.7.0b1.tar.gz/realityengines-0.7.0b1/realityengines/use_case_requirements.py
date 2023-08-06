

class UseCaseRequirements():
    '''

    '''

    def __init__(self, client, projectDatasetType=None, name=None, description=None, required=None, allowedColumnMappings=None):
        self.client = client
        self.id = projectDatasetType
        self.project_dataset_type = projectDatasetType
        self.name = name
        self.description = description
        self.required = required
        self.allowed_column_mappings = allowedColumnMappings

    def __repr__(self):
        return f"UseCaseRequirements(project_dataset_type={repr(self.project_dataset_type)}, name={repr(self.name)}, description={repr(self.description)}, required={repr(self.required)}, allowed_column_mappings={repr(self.allowed_column_mappings)})"

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.id == other.id

    def to_dict(self):
        return {'project_dataset_type': self.project_dataset_type, 'name': self.name, 'description': self.description, 'required': self.required, 'allowed_column_mappings': self.allowed_column_mappings}
