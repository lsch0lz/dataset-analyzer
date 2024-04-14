import os
import logging
from collections import defaultdict
from heapq import nlargest
from typing import List, Dict

from utils.similarity_search.model import SimilarImages, SimilarImage, TopKSimilarImages
from utils.similarity_search.similarity_scorer import SimilarityScorer

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class DataLoader:
    def __init__(self, image_path: str, similarity_threshold: int):
        self.image_path = image_path if image_path.endswith("/") else image_path + "/"
        self.similarity_threshold = similarity_threshold

    def get_similar_images(self) -> SimilarImages:
        image_paths: List = []
        for image in os.listdir(self.image_path):
            image_path: str = self.image_path + image
            image_paths.append(image_path)

        cleaned_image_paths: List[str] = self._remove_non_image_paths(image_paths)
        logger.info(f"Number of Images in Dir: {len(cleaned_image_paths)}")

        similar_image_paths: SimilarImages = SimilarityScorer(cleaned_image_paths, self.similarity_threshold).get_images_w_similar_score()
        logger.info(f"Number of ImagePairs: {len(similar_image_paths.similar_images)}")

        return similar_image_paths

    @staticmethod
    def _remove_non_image_paths(image_paths: List[str]) -> List[str]:
        cleaned_image_paths: List[str] = []
        for image_path in image_paths:
            if image_path.endswith(".jpg") or image_path.endswith(".png") or image_path.endswith(".jpeg"):
                cleaned_image_paths.append(image_path)

        return cleaned_image_paths


def filter_images_based_on_threshold(similar_images: SimilarImages, similarity_threshold: float) -> SimilarImages:
    filtered_similar_images: SimilarImages = SimilarImages(similar_images=[])
    for similar_image in similar_images.similar_images:
        if similar_image.similarity_score >= similarity_threshold:
            filtered_similar_images.similar_images.append(similar_image)

    return filtered_similar_images


def find_top_k_image_pairs(filtered_similar_images: SimilarImages, top_k_image_pairs: int) -> SimilarImages:
    top_k_similar_images_dict: Dict[str, List[SimilarImage]] = defaultdict(list)
    for image in filtered_similar_images.similar_images:
        top_k_similar_images_dict[image.image1_path].append(image)

    top_k_similar_images_list = []
    for image_path, images in top_k_similar_images_dict.items():
        top_k = nlargest(top_k_image_pairs, images, key=lambda x: x.similarity_score)
        top_k_similar_images_list.extend(top_k)

    return SimilarImages(top_k_similar_images_list)