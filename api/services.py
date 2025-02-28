def parse_following_file(data):
    username_list = set()
    
    for entry in data:
        for item in entry.get("string_list_data", []):
            username_list.add(item["value"])
    
    return username_list

def parse_followers_file(data):
    username_list = set()
    
    for entry in data:
        for item in entry.get("string_list_data", []):
            username_list.add(item["value"])
    
    return username_list