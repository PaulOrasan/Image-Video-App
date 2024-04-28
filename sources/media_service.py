from entity_model import MediaResource
from repository_persistence import MediaResourceRepository


class MediaService:

    def __init__(self, mediaRepository: MediaResourceRepository):
        self.repo = mediaRepository


    def save_image(self, user_id, file_name):
        resource = MediaResource(file_name=file_name, user_id=user_id)
        self.repo.add_resource(resource)

    def find_resource_by_path(self, path):
        return self.repo.get_resource_by_file_name(path)

    def save_video(self, user_id, file_name):
        resource = MediaResource(file_name=file_name, user_id=user_id, is_image=True)
        self.repo.add_resource(resource)

    def find_resource_by_id(self, source_image_id):
        return self.repo.find_resource(source_image_id)
