class PredictionDTO:
    def __init__(self, request_time, prompt, negative_prompt, field_x, field_y, t0, t1, seed, source_image, output_video):
        self.request_time = request_time
        self.prompt = prompt
        self.negative_prompt = negative_prompt
        self.field_x = field_x
        self.field_y = field_y
        self.t0 = t0
        self.t1 = t1
        self.seed = seed
        self.source_image = source_image
        self.output_video = output_video

    @staticmethod
    def encode_prediction_as_json(prediction, source_image, output_video):
        return {
            "request_time": str(prediction.request_time),
            "prompt": prediction.prompt,
            "negative_prompt": prediction.negative_prompt,
            "field_x": prediction.field_x,
            "field_y": prediction.field_y,
            "t0": prediction.t0,
            "t1": prediction.t1,
            "seed": prediction.seed,
            "source_image": source_image,
            "output_video": output_video
        }

    @staticmethod
    def decode_prediction_from_json(json_data):
        return PredictionDTO(
            request_time=json_data["request_time"],
            prompt=json_data["prompt"],
            negative_prompt=json_data["negative_prompt"],
            field_x=json_data["field_x"],
            field_y=json_data["field_y"],
            t0=json_data["t0"],
            t1=json_data["t1"],
            seed=json_data["seed"],
            source_image=json_data["source_image"],
            output_video=json_data["output_video"]
        )
