import pytest

from django_swagger_tester.case_checks import is_camel_case
from django_swagger_tester.exceptions import OpenAPISchemaError
from django_swagger_tester.validate_response import _dict

schema = {
    'type': 'object',
    'properties': {
        'name': {'description': 'A swedish car?', 'type': 'string', 'example': 'Saab'},
        'color': {'description': 'The color of the car.', 'type': 'string', 'example': 'Yellow'},
        'height': {'description': 'How tall the car is.', 'type': 'string', 'example': 'Medium height'},
        'width': {'description': 'How wide the car is.', 'type': 'string', 'example': 'Very wide'},
        'length': {'description': 'How long the car is.', 'type': 'string', 'example': '2 meters'},
    }
}
data = {'name': 'Saab', 'color': 'Yellow', 'height': 'Medium height', 'width': 'Very wide', 'length': '2 meters'}


def test_valid_dict() -> None:
    """
    Asserts that valid data passes successfully.
    """
    _dict(schema=schema, data=data, case_func=is_camel_case)


def test_bad_data_type() -> None:
    """
    Asserts that the appropriate exception is raised for a bad response data type.
    """
    with pytest.raises(OpenAPISchemaError, match="The response is <class 'list'> where it should be <class 'dict'>"):
        _dict(schema=schema, data=[data], case_func=is_camel_case)


def test_unmatched_lengths() -> None:
    """
    Asserts that different dict lengths raises an exception.
    """
    data = {'name': '', 'color': '', 'height': '', 'width': '', 'length': '', 'extra key': ''}
    with pytest.raises(
            OpenAPISchemaError,
            match='The following properties seem to be missing from your OpenAPI/Swagger documentation: `extra key`'
    ):
        _dict(schema=schema, data=data, case_func=is_camel_case)
