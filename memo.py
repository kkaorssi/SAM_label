import numpy as np

auto = {
    'filename':{
        'masks': None,
        'obj_list':{
                'label': None,
                'mask': None
        }
    }
}

manual = {
    'filename':{
        'predictor': None,
        'obj_list': {
            'label': {
                'input_point': None,
                'input_label': None,
                'mask': None,
                'scores': None,
                'logits': None
            }
        }
    }
}