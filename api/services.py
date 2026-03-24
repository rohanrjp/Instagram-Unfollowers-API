def parse_followers_file(data):
    """
    Extract usernames from followers_1.json.
    """
    username_set = set()
    for entry in data:
        # Each entry has a string_list_data list containing the username info
        for item in entry.get("string_list_data", []):
            if "value" in item and item["value"]:
                username_set.add(item["value"].strip().lower())
            # Fallback to href if value is missing
            elif "href" in item:
                username = item["href"].rstrip("/").split("/")[-1]
                username_set.add(username.strip().lower())
    return username_set


def parse_following_file(data):
    """
    Extract usernames from following.json.
    """
    username_set = set()
    for entry in data:
        # In following.json, the username is explicitly in the 'title' field
        if "title" in entry and entry["title"]:
            username_set.add(entry["title"].strip().lower())
        else:
            # Fallback for nested data if title is missing
            for item in entry.get("string_list_data", []):
                if "href" in item:
                    # Instagram hrefs in following usually look like .../_u/username
                    username = item["href"].rstrip("/").split("/")[-1]
                    username_set.add(username.strip().lower())
    return username_set