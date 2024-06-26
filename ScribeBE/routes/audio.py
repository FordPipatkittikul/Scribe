import logging
from bson.objectid import ObjectId  # type: ignore
from database.database import Database
from fastapi import APIRouter, Depends, HTTPException,UploadFile 
from auth.authenticate import authenticate
from models.audio_model import DbAudio
from bson.binary import Binary
from database.database import Database
import base64

logger = logging.getLogger(__name__)

audio_router = APIRouter(tags=["Audio"])

audio_database = Database(DbAudio)

@audio_router.get("/{id}")
async def get_audio_file(id: str, user: str = Depends(authenticate)) -> dict:
    try:
        audio_file_id = ObjectId(id)
        audio_file = await audio_database.get(audio_file_id)
        data = audio_file.file['data'] # Nithi: this data instead of file
        audio_base64 = base64.b64encode(data).decode('utf-8') 
        logger.info(f"Retrieved audio file {id} successfully")
    except Exception:
        logger.warning(f"{id} is an invalid audio file id")
        raise HTTPException(status_code=400, detail="Invalid audio file id")
    return {"audio_data": audio_base64} 

@audio_router.post("/", status_code=201)
async def recieve_audio(audio: UploadFile, user: str = Depends(authenticate)) -> dict:
    
    audio_doc = convert_audio_file(audio.file)
    audio_instance = DbAudio(**audio_doc)

    await audio_database.save(audio_instance)

    logger.info(f"New audio file from {user["email_id"]} created")
    return {"recording_id": str(audio_instance.id)}


def convert_audio_file(audio) -> dict:
    audio_data = audio.read()
    audio_binary = Binary(audio_data)
    audio_doc = {
        "file": {
            "data": audio_binary,
            "format": "wav"
        }
    }
    return audio_doc


