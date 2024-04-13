from dataclasses import dataclass
from typing import List


@dataclass
class SimilarImage:
    image1_path: str
    image2_path: str
    similarity_score: float


@dataclass
class SimilarImages:
    similar_images: List[SimilarImage]
