from django_swagger_tester.dynamic.get_schema import fetch_generated_schema
from django_swagger_tester.static.get_schema import fetch_from_dir
from django_swagger_tester.static.parse import parse_endpoint


def test_identical_parsing(client, monkeypatch) -> None:  # noqa: TYP001
    """
    Asserts that the validate_response function validates correct schemas successfully.
    """
    from django.conf import settings as openapi_settings

    for endpoint_url in ['/trucks/correct/', '/cars/correct/']:
        method = 'GET'

        full_static_content = fetch_from_dir(openapi_settings.BASE_DIR + '/demo_project/openapi-schema.yml')
        static_content = parse_endpoint(schema=full_static_content, method=method, endpoint_url='/api/v1' + endpoint_url, status_code=200)
        dynamic_content = fetch_generated_schema(url=endpoint_url, method=method, status_code=200)

        assert dynamic_content == static_content
