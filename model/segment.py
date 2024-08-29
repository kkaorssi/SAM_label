from segment_anything import SamPredictor, sam_model_registry, SamAutomaticMaskGenerator

import os
import numpy as np
import torch
import matplotlib.pyplot as plt
import cv2

MODEL_PATH = 'model'
SAM_CHECKPOINT = 'sam_vit_h_4b8939.pth'

sam_checkpoint = os.path.join(MODEL_PATH, SAM_CHECKPOINT)
model_type = 'vit_h' # default vit_h, optional vit_l, vit_b
if torch.cuda.is_available(): device = 'cpu' # cpu -> cuda
else: device = 'cpu'

class segmentAnything:
    def __init__(self):
        self.sam = sam_model_registry[model_type](checkpoint=sam_checkpoint)
        self.sam.to(device=device)

    def manual_mode(self, image):
        predictor = SamPredictor(self.sam)
        predictor.set_image(image)
        
        return predictor
        
    def auto_mode(self, image):
        mask_generator = SamAutomaticMaskGenerator(self.sam)
        masks = mask_generator.generator(image)
        
        return masks

    def add_point(self, predictor, input_point, input_label, scores=None, logits=None):
        input_point = np.array(input_point)
        input_label = np.array(input_label)
        if logits is None:
            mask_input = None
        else:
            mask_input = logits[np.argmax(scores), :, :]  # Choose the model's best mask
            mask_input = mask_input[None, :, :]
        
        masks, scores, logits = predictor.predict(
        point_coords=input_point,
        point_labels=input_label,
        mask_input=mask_input,
        multimask_output=True,
        )
        mask = masks[np.argmax(scores)]

        return mask, scores, logits