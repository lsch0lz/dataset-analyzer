import os
from typing import List


class DataLoader:
    def __init__(self, image_path):
        self.image_path = image_path if image_path.endswith("/") else image_path + "/"

    def get_similar_images(self) -> List[str]:
        image_paths: List = []
        for image in os.listdir(self.image_path):
            image_path: str = self.image_path + image
            image_paths.append(image_path)

        cleaned_image_paths: List[str] = self._remove_non_image_paths(image_paths)

        return cleaned_image_paths

    @staticmethod
    def _remove_non_image_paths(image_paths: List[str]) -> List[str]:
        cleaned_image_paths: List[str] = []
        for image_path in image_paths:
            if image_path.endswith(".jpg") or image_path.endswith(".png") or image_path.endswith(".jpeg"):
                cleaned_image_paths.append(image_path)

        return cleaned_image_paths
