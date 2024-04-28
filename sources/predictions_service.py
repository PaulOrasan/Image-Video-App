from entity_model import Prediction
from repository_persistence import PredictionRepository


class PredictionService:

    def __init__(self, pred_repo: PredictionRepository):
        self.repo = pred_repo

    def save_prediction(self, user_id, source_image_id: int, output_video_id, prompt: str, motion_filed_strength_x: int, motion_filed_strength_y: int,
                        t0: int, t1: int, n_prompt: str, seed: int):
        pred = Prediction(user_id=user_id,
                          source_image_id=source_image_id,
                          output_video_id=output_video_id,
                          prompt=prompt,
                          negative_prompt=n_prompt,
                          field_x=motion_filed_strength_x,
                          field_y=motion_filed_strength_y,
                          t0=t0,
                          t1=t1,
                          seed=seed)
        self.repo.add_prediction(pred)

    def find_predictions(self, user_id):
        return self.repo.find_predictions_by_user(user_id)