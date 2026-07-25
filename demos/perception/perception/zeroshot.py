from __future__ import annotations

import numpy as np

from .detection import Detection
from .segmentation import Instance, Segmentation

DINO_MODEL = "IDEA-Research/grounding-dino-base"
SAM_MODEL = "facebook/sam-vit-huge"


def _device() -> str:
    import torch

    return "mps" if torch.backends.mps.is_available() else "cpu"


class GroundedSam:
    def __init__(self, box_threshold: float = 0.3, text_threshold: float = 0.25):
        import torch
        from transformers import AutoModelForZeroShotObjectDetection, AutoProcessor, SamModel, SamProcessor

        self._torch = torch
        self._device = _device()
        self._box_threshold = box_threshold
        self._text_threshold = text_threshold

        self._dino_processor = AutoProcessor.from_pretrained(DINO_MODEL)
        self._dino = AutoModelForZeroShotObjectDetection.from_pretrained(DINO_MODEL).to(self._device).eval()
        self._sam_processor = SamProcessor.from_pretrained(SAM_MODEL)
        self._sam = SamModel.from_pretrained(SAM_MODEL).to(self._device).eval()

    def detect_and_segment(self, rgb: np.ndarray, prompt: str) -> tuple[list[Detection], Segmentation]:
        from PIL import Image

        image = Image.fromarray(rgb)
        detections = self._detect(image, prompt)
        segmentation = self._segment(image, rgb.shape[:2], detections)
        return detections, segmentation

    def _detect(self, image, prompt: str) -> list[Detection]:
        inputs = self._dino_processor(images=image, text=prompt, return_tensors="pt").to(self._device)
        with self._torch.no_grad():
            outputs = self._dino(**inputs)

        result = self._dino_processor.post_process_grounded_object_detection(
            outputs,
            inputs["input_ids"],
            threshold=self._box_threshold,
            text_threshold=self._text_threshold,
            target_sizes=[image.size[::-1]],
        )[0]

        detections = []
        for box, score, label in zip(result["boxes"], result["scores"], result["text_labels"]):
            x1, y1, x2, y2 = box.tolist()
            detections.append(
                Detection(x=x1, y=y1, width=x2 - x1, height=y2 - y1, label=label, score=float(score))
            )
        return detections

    def _segment(self, image, shape: tuple[int, int], detections: list[Detection]) -> Segmentation:
        height, width = shape
        label_map = np.zeros((height, width), dtype=np.uint16)
        instances: list[Instance] = []

        for index, detection in enumerate(detections, start=1):
            mask = self._mask_for_box(image, detection)
            label_map[mask] = index
            instances.append(Instance(id=index, label=detection.label, score=detection.score))

        return Segmentation(label_map, instances)

    def _mask_for_box(self, image, detection: Detection) -> np.ndarray:
        box = [detection.x, detection.y, detection.x + detection.width, detection.y + detection.height]
        inputs = self._sam_processor(image, input_boxes=[[box]], return_tensors="pt")
        inputs = inputs.__class__(
            {k: (v.float() if v.is_floating_point() else v) for k, v in inputs.items()}
        )
        model_inputs = {k: v.to(self._device) for k, v in inputs.items() if k in ("pixel_values", "input_boxes")}

        with self._torch.no_grad():
            outputs = self._sam(**model_inputs, multimask_output=True)

        masks = self._sam_processor.image_processor.post_process_masks(
            outputs.pred_masks.float().cpu(), inputs["original_sizes"], inputs["reshaped_input_sizes"]
        )[0][0]
        best = int(outputs.iou_scores[0, 0].argmax())
        return masks[best].numpy().astype(bool)
