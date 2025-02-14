from fastapi import FastAPI, status, UploadFile
import json
from api.services import parse_followers_file, parse_following_file

app = FastAPI(title="Unfollowers for Instagram",version="1.0")

@app.post("/analyze", status_code=status.HTTP_200_OK)
async def analyze(followers_file: UploadFile, following_file: UploadFile):
    
    followers_content = await followers_file.read()
    following_content = await following_file.read()

    followers_data = json.loads(followers_content.decode('utf-8'))
    following_data = json.loads(following_content.decode('utf-8'))
    
    if isinstance(followers_data, list):
        followers_list = parse_followers_file(followers_data)
    else:
        return {"error": "Invalid followers data format. Expected list."}

    if isinstance(following_data, dict) and "relationships_following" in following_data:
        following_list = parse_following_file(following_data["relationships_following"])
    else:
        return {"error": "Invalid following data format. Expected dictionary with 'relationships_following' key."}
    
    unfollowers_list = list(following_list - followers_list)
    people_im_not_following_back_list=list(followers_list-following_list)
    
    return {"Unfollowers":list(unfollowers_list),"People I am not following back":list(people_im_not_following_back_list),"followers": list(followers_list), "following": list(following_list)}