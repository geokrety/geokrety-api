
from app.api.helpers.exceptions import UnprocessableEntity


def dasherize(text):
    return text.replace('_', '-')


def require_relationship(resource_list, data):
    for resource in resource_list:
        if resource not in data:
            raise UnprocessableEntity("A valid relationship with {} resource is required".format(resource),
                                      {'pointer': '/data/relationships/{}'.format(resource)})
