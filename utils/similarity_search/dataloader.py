import os
from typing import List

from utils.similarity_search.similarity_scorer import SimilarityScorer


class DataLoader:
    def __init__(self, image_path: str, similarity_threshold: int):
        self.image_path = image_path if image_path.endswith("/") else image_path + "/"
        self.similarity_threshold = similarity_threshold

    def get_similar_images(self) -> List[str]:
        image_paths: List = []
        for image in os.listdir(self.image_path):
            image_path: str = self.image_path + image
            image_paths.append(image_path)

        cleaned_image_paths: List[str] = self._remove_non_image_paths(image_paths)
        similar_image_paths: List[str] = SimilarityScorer(cleaned_image_paths, self.similarity_threshold).get_images_w_similar_score()

        return similar_image_paths

    @staticmethod
    def _remove_non_image_paths(image_paths: List[str]) -> List[str]:
        cleaned_image_paths: List[str] = []
        for image_path in image_paths:
            if image_path.endswith(".jpg") or image_path.endswith(".png") or image_path.endswith(".jpeg"):
                cleaned_image_paths.append(image_path)

        return cleaned_image_paths
