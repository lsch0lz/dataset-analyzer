from collections import defaultdict
from typing import List

import streamlit as st
import torch
import clip
from PIL import Image


class SimilarityScorer:
    def __init__(self, cleaned_image_paths: List[str], similarity_threshold: int):
        self.cleaned_image_paths = cleaned_image_paths
        self.similarity_threshold = similarity_threshold
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model, self.preprocess = clip.load("RN50", device=self.device)
        self.cos = torch.nn.CosineSimilarity(dim=0)
        self.similarity_map = defaultdict(dict)
        self.progress_bar = st.progress(0, text="Computing Similarity")

    def get_images_w_similar_score(self):
        print(clip.available_models())
        print(self.device)
        similar_images = []
        for i in range(len(self.cleaned_image_paths)):
            self.progress_bar.progress(i + 1, text="Computing Similarity")
            for j in range(i + 1, len(self.cleaned_image_paths)):
                image1 = self.cleaned_image_paths[i]
                image2 = self.cleaned_image_paths[j]

                if image2 in self.similarity_map[image1]:
                    similarity = self.similarity_map[image1][image2]
                else:
                    image1_features, image2_features = self._preprocess_images(image1, image2)
                    similarity = self.cos(image1_features[0], image2_features[0]).item()
                    similarity = (similarity + 1) / 2

                if similarity >= self.similarity_threshold:
                    similar_images.append((image1, image2, similarity))

        self.progress_bar.empty()
        return similar_images

    def _preprocess_images(self, image_1, image_2):
        image1_preprocess = self.preprocess(Image.open(image_1)).unsqueeze(0).to(self.device)
        image1_features = self.model.encode_image(image1_preprocess)

        image2_preprocess = self.preprocess(Image.open(image_2)).unsqueeze(0).to(self.device)
        image2_features = self.model.encode_image(image2_preprocess)

        return image1_features, image2_features
