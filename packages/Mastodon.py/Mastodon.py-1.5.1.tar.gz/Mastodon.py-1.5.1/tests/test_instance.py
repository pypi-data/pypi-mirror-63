import pytest

from mastodon.Mastodon import MastodonVersionError

@pytest.mark.vcr()
def test_instance(api):
    instance = api.instance()

    assert isinstance(instance, dict)  # hehe, instance is instance

    expected_keys = set(('description', 'email', 'title', 'uri', 'version', 'urls'))
    assert set(instance.keys()) >= expected_keys

@pytest.mark.vcr()
def test_instance_activity(api):
    activity = api.instance_activity()
    
    assert len(activity) > 0
    assert "statuses" in activity[0]
    assert "logins" in activity[0]
    assert "week" in activity[0]

@pytest.mark.vcr()
def test_instance_peers(api):
    assert len(api.instance_peers()) == 0

@pytest.mark.vcr()
def test_low_version(api_low_version):
    with pytest.raises(MastodonVersionError):
        instance = api_low_version.instance()
    
@pytest.mark.vcr()
def test_emoji(api):
    assert len(api.custom_emojis()) == 0

@pytest.mark.vcr()
def test_health(api):
    assert api.instance_health() == True
    
@pytest.mark.vcr()
def test_nodeinfo(api):
    nodeinfo = api.instance_nodeinfo()
    assert nodeinfo
    assert nodeinfo.version == '2.0'
    
@pytest.mark.vcr()
def test_trends(api):
    assert isinstance(api.trends(), list)
    
@pytest.mark.vcr()
def test_directory(api):
    directory = api.directory()
    assert directory
    assert isinstance(directory, list)
    assert len(directory) > 0

    
