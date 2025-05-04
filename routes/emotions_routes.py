from flask import Blueprint

from routes.queries.get_emotions_query import GetEmotionsQuery

emotions_blueprint = Blueprint('results', __name__, url_prefix='/results')


@emotions_blueprint.route('/<int:photo_id>', methods=['GET'])
def get_emotions_by_photo_id(photo_id):
    emotions_entities = GetEmotionsQuery().by_photo_id(photo_id)
    emotions_response = [emotion_entity.name for emotion_entity in emotions_entities]

    return emotions_response
    