import httpx


def is_valid_userid(userid: int) -> bool:
    """ Returns True if the userid is valid, False otherwise. """
    return httpx.get(f"https://inventory.roblox.com/v1/users/{userid}/can-view-inventory").status_code == 200


def can_view_inv(userid: int) -> bool:
    """ Returns True if the user can view their inventory, False otherwise. """
    return httpx.get(f"https://inventory.roblox.com/v1/users/{userid}/can-view-inventory").json().get('canView', False)


def has_asset(userid: int, assetid: int) -> bool:
    """ Returns True if the user has the asset, False otherwise. """
    return httpx.get(f"https://inventory.roblox.com/v1/users/{userid}/items/Asset/{assetid}/is-owned").text == "true"


def get_profile(userid: int) -> (dict[str, str | bool | None | int] | dict):
    """ Returns the user's profile. """
    data = httpx.get(f"https://users.roblox.com/v1/users/{userid}").json()
    if 'errors' in data:
        return {}
    return data


def get_user_headshot_url(userid: int) -> str:
    """ Returns the user's headshot url. """
    res = httpx.get(f"https://thumbnails.roblox.com/v1/users/avatar-headshot?userIds={userid}&size=150x150&format=Png")
    if res.status_code != 200:
        return ''
    data = res.json()['data'][0]
    return data['imageUrl']
