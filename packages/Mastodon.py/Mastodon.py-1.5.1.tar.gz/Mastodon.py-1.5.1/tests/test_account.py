import pytest
from mastodon.Mastodon import MastodonAPIError, MastodonIllegalArgumentError
import re
import time

@pytest.mark.vcr()
def test_account(api):
    account = api.account(1)
    assert account

@pytest.mark.vcr()
def test_verify_credentials(api):
    account_a = api.account_verify_credentials()
    account_b = api.me()
    
    assert account_a.id == account_b.id
    
@pytest.mark.vcr()
def test_account_following(api):
    following = api.account_following(1)
    assert isinstance(following, list)


@pytest.mark.vcr()
def test_account_followers(api):
    followers = api.account_followers(1)
    assert isinstance(followers, list)


@pytest.mark.vcr()
def test_account_relationships(api):
    relationships = api.account_relationships(1)
    assert isinstance(relationships, list)
    assert len(relationships) == 1


@pytest.mark.vcr()
def test_account_search(api):
    results = api.account_search('admin')
    admin_acc = results[0]
    
    assert isinstance(results, list)
    assert len(results) == 1

    api.account_follow(admin_acc)
    results = api.account_search('admin', following = True)
    assert isinstance(results, list)
    assert len(results) == 1
    
    api.account_unfollow(admin_acc)
    results = api.account_search('admin', following = True)
    assert isinstance(results, list)
    assert len(results) == 0
    
    results = api.account_search('admin')
    assert isinstance(results, list)
    assert len(results) == 1
    
@pytest.mark.vcr()
def test_account_follow_unfollow(api):
    relationship = api.account_follow(1)
    try:
        assert relationship
        assert relationship['following']
    finally:
        relationship = api.account_unfollow(1)
        assert relationship
        assert not relationship['following']


@pytest.mark.vcr()
def test_account_block_unblock(api):
    relationship = api.account_block(1)
    try:
        assert relationship
        assert relationship['blocking']
    finally:
        relationship = api.account_unblock(1)
        assert relationship
        assert not relationship['blocking']


@pytest.mark.vcr()
def test_account_mute_unmute(api):
    relationship = api.account_mute(1)
    try:
        assert relationship
        assert relationship['muting']
    finally:
        relationship = api.account_unmute(1)
        assert relationship
        assert not relationship['muting']


@pytest.mark.vcr()
def test_mutes(api):
    mutes = api.mutes()
    assert isinstance(mutes, list)


@pytest.mark.vcr()
def test_blocks(api):
    blocks = api.blocks()
    assert isinstance(blocks, list)


@pytest.mark.vcr(match_on=['path'])
def test_account_update_credentials(api):
    with open('tests/image.jpg', 'rb') as f:
        image = f.read()

    account = api.account_update_credentials(
        display_name='John Lennon',
        note='I walk funny',
        avatar = "tests/image.jpg",
        header = image,
        header_mime_type = "image/jpeg",
        fields = [
            ("bread", "toasty."),
            ("lasagna", "no!!!"),
        ]
    )
    
    assert account
    assert account["display_name"] == 'John Lennon'
    assert re.sub("<.*?>", " ", account["note"]).strip() == 'I walk funny'
    assert account["fields"][0].name == "bread"
    assert account["fields"][0].value == "toasty."
    assert account["fields"][1].name == "lasagna"
    assert account["fields"][1].value == "no!!!"

@pytest.mark.vcr()
def test_account_update_credentials_too_many_fields(api):
    with pytest.raises(MastodonIllegalArgumentError):
        api.account_update_credentials(fields = [
            ('a', 'b'),
            ('c', 'd'), 
            ('e', 'f'), 
            ('g', 'h'), 
            ('i', 'j'),
        ])

@pytest.mark.vcr(match_on=['path'])
def test_account_update_credentials_no_header(api):
    account = api.account_update_credentials(
            display_name='John Lennon',
            note='I walk funny',
            avatar = "tests/image.jpg")
    assert account

@pytest.mark.vcr(match_on=['path'])
def test_account_update_credentials_no_avatar(api):
    with open('tests/image.jpg', 'rb') as f:
        image = f.read()

    account = api.account_update_credentials(
            display_name='John Lennon',
            note='I walk funny',
            header = image,
            header_mime_type = "image/jpeg")
    assert account

@pytest.mark.vcr()
def test_account_pinned(status, status2, api):
    try:
        status = api.status_pin(status['id'])
        pinned = api.account_statuses(api.account_verify_credentials(), pinned = True)
        assert status in pinned
        assert not status2 in pinned
    finally:
        api.status_unpin(status['id'])

@pytest.mark.vcr()
def test_follow_suggestions(api2, status):
    api2.status_favourite(status)
    
    suggestions = api2.suggestions()
    assert(suggestions)
    assert(len(suggestions) > 0)
    
    api2.suggestion_delete(suggestions[0])
    suggestions2 = api2.suggestions()
    assert(len(suggestions2) < len(suggestions))
    
@pytest.mark.vcr()
def test_account_pin_unpin(api, api2):
    user = api2.account_verify_credentials()
    
    # Make sure we are in the correct state
    try:
        api.account_follow(user)
    except:
        pass
    
    try:
        api.account_unpin(user)
    except:
        pass
    
    relationship = api.account_pin(user)
    endorsed = api.endorsements()
        
    try:
        assert relationship
        assert relationship['endorsed']
        assert user["id"] in map(lambda x: x["id"], endorsed)
    finally:
        relationship = api.account_unpin(user)
        endorsed2 = api.endorsements()
        api.account_unfollow(user)        
        assert relationship
        assert not relationship['endorsed']
        assert not user["id"] in map(lambda x: x["id"], endorsed2)

@pytest.mark.vcr()
def test_preferences(api):
    prefs = api.preferences()
    assert prefs

@pytest.mark.vcr()
def test_suggested_tags(api):
    try:
        status = api.status_post("cool free #ringtones")
        time.sleep(2)
        
        suggests = api.featured_tag_suggestions()
        assert suggests
        assert len(suggests) > 0
    finally:
        api.status_delete(status)
    
@pytest.mark.vcr()
def test_featured_tags(api):
    featured_tag = api.featured_tag_create("mastopytesttag")
    assert featured_tag
    
    tag_list = api.featured_tags()
    assert featured_tag.name in list(map(lambda x: x.name, tag_list))
    
    api.featured_tag_delete(featured_tag)
    tag_list = api.featured_tags()
    assert not featured_tag.name in list(map(lambda x: x.name, tag_list))
        
        
        
        
        
        
        
        
        
