from __future__ import annotations

import numpy as np

DEPTH_MODEL = "depth-anything/Depth-Anything-V2-Large-hf"


class MonoDepth:
    def __init__(self):
        import torch
        from transformers import AutoImageProcessor, AutoModelForDepthEstimation

        self._torch = torch
        self._device = "mps" if torch.backends.mps.is_available() else "cpu"
        self._processor = AutoImageProcessor.from_pretrained(DEPTH_MODEL)
        self._model = AutoModelForDepthEstimation.from_pretrained(DEPTH_MODEL).to(self._device).eval()

    def relative_depth(self, rgb: np.ndarray) -> np.ndarray:
        from PIL import Image

        image = Image.fromarray(rgb)
        inputs = self._processor(images=image, return_tensors="pt").to(self._device)
        with self._torch.no_grad():
            predicted = self._model(**inputs).predicted_depth

        resized = self._torch.nn.functional.interpolate(
            predicted.unsqueeze(1).float(),
            size=image.size[::-1],
            mode="bicubic",
            align_corners=False,
        )
        return resized[0, 0].cpu().numpy()


def to_metres(relative_depth: np.ndarray, near: float = 0.4, far: float = 3.0) -> np.ndarray:
    lo, hi = float(relative_depth.min()), float(relative_depth.max())
    normalized = (relative_depth - lo) / (hi - lo + 1e-6)
    return far - normalized * (far - near)
