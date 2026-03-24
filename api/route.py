from fastapi import FastAPI, status, UploadFile, HTTPException
import json
from api.services import parse_followers_file, parse_following_file

app = FastAPI(
    title="Unfollowers for Instagram",
    version="1.0",
    description="Simple API that finds out your unfollowers",
    summary="Checks the followers and following JSON files fetched from Instagram"
)

@app.post("/analyze", status_code=status.HTTP_200_OK)
async def analyze(followers_file: UploadFile, following_file: UploadFile):
    try:
        followers_content = await followers_file.read()
        following_content = await following_file.read()

        followers_data = json.loads(followers_content.decode('utf-8'))
        following_data = json.loads(following_content.decode('utf-8'))
        
        # Parse followers (Expects a list top-level)
        if isinstance(followers_data, list):
            followers_set = parse_followers_file(followers_data)
        else:
            raise HTTPException(status_code=400, detail="Invalid followers data format. Expected a list.")

        # Parse following (Expects dict with 'relationships_following' key)
        if isinstance(following_data, dict) and "relationships_following" in following_data:
            following_set = parse_following_file(following_data["relationships_following"])
        else:
            raise HTTPException(status_code=400, detail="Invalid following data format. Expected 'relationships_following' key.")

        unfollowers = following_set - followers_set
        not_followed_back = followers_set - following_set

        return {
            "Followers_count": len(followers_set),
            "Following_count": len(following_set),
            "Unfollowers_count": len(unfollowers),
            "Unfollowers": sorted(list(unfollowers)),
            "People_I_am_not_following_back_count": len(not_followed_back),
            "People_I_am_not_following_back": sorted(list(not_followed_back))
        }
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Error decoding JSON. Please upload valid Instagram data files.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))