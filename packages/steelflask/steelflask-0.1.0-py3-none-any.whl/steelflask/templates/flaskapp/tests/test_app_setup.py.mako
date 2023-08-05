
def test_must_respond_to_ping(client, resource_uri, snapshot):
    response = client.get(resource_uri.get('ping'))
    snapshot.assert_match(response.json)


def test_gracefully_handle_404_not_found(client, snapshot):
    response = client.get('/unknowUri')
    snapshot.assert_match(response.json)


def test_gracefully_handle_405_method_not_allowed(client, resource_uri, snapshot):
    response = client.post(resource_uri.get('ping'))
    snapshot.assert_match(response.json)
