import logging
from config.model_config import model_type

from domain import Emotion
from domain import PhotoEmotion

from helpers.get_from_db_or_create import get_from_db_or_create
from pydantic import BaseModel

from domain.data_access_layer.session import session



class NewPhotoEmotionCommand:
    def __init__(self):
        pass
    
    def create(self, emotion_entity: Emotion, photo_id: int):
        emotion_instance = get_from_db_or_create(Emotion, name=emotion_entity.name)

        with session() as current_session:
            current_session.add(PhotoEmotion(photo_id=photo_id,
                                            emotion_id=emotion_instance.id))
            current_session.commit()


class EmotionSchema(BaseModel):
    name: str

    class Config:
        orm_mode = True


insert_to_db_commands = {
    'emotions-model': NewPhotoEmotionCommand,
}

map_result_to_entity = {
    'emotions-model': Emotion,
}

validate_result_with_schema = {
    'emotions-model': EmotionSchema,
}

class AppendResultsCommand:
    @staticmethod
    def execute(result_message):
        for result in result_message['result']:
            valid_result = validate_result_with_schema[model_type](**result)
            result_entity = map_result_to_entity[model_type](**valid_result.dict())

            insert_to_db_command = insert_to_db_commands[model_type]
            insert_to_db_command().create(
                result_entity, 
                result_message['photo_id'],
                )
