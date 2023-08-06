from . import now_str

draft_id = {}


def test_create_draft(client_with_auth):
    env = client_with_auth.config.env
    draft = {
        'title': f'draft title {now_str()}',
        'content': f'draft content {now_str()}',
        'mime_type': 'text/plain',
    }
    res = client_with_auth.draft.create(draft)
    assert res.status_code == 200
    data = res.json()
    global draft_id
    draft_id[env] = data['draftId']
    assert draft_id[env]


def test_get_draft_by_id(client_with_auth):
    env = client_with_auth.config.env
    global draft_id
    res = client_with_auth.draft.get_by_id(draft_id[env])
    assert res.status_code == 200


def test_update_draft(client_with_auth):
    env = client_with_auth.config.env
    global draft_id
    draft = {
        'title': f'draft update title {now_str()}',
        'content': f'draft update content {now_str()}',
        'mime_type': 'text/plain',
    }
    res = client_with_auth.draft.update(draft_id[env], draft)
    assert res.status_code == 200


def test_get_drafts(client_with_auth):
    res = client_with_auth.draft.get_drafts()
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, dict)
    lst = data['data']['list']
    assert lst and isinstance(lst, list)


def test_delete_draft(client_with_auth):
    env = client_with_auth.config.env
    global draft_id
    res = client_with_auth.draft.delete(draft_id[env])
    assert res.status_code == 200
