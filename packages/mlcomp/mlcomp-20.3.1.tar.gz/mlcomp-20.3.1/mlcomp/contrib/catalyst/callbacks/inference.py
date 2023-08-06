import os

import numpy as np

from collections import defaultdict
from catalyst.dl import State as RunnerState
from catalyst.dl.core import Callback


class InferBestCallback(Callback):
    def __init__(self, out_dir=None, out_prefix=None, best_only=False):
        self.out_dir = out_dir
        self.out_prefix = out_prefix
        self.predictions = defaultdict(lambda: [])
        self.best_only = best_only
        self._keys_from_state = ['out_dir', 'out_prefix']

    def on_stage_start(self, state: RunnerState):
        for key in self._keys_from_state:
            value = getattr(state, key, None)
            if value is not None:
                setattr(self, key, value)
        # assert self.out_prefix is not None
        if self.out_dir is not None:
            self.out_prefix = str(self.out_dir) + '/' + str(self.out_prefix)
        if self.out_prefix is not None:
            os.makedirs(os.path.dirname(self.out_prefix), exist_ok=True)

    def on_loader_start(self, state: RunnerState):
        self.predictions = defaultdict(lambda: [])

    def on_batch_end(self, state: RunnerState):
        dct = state.output
        dct = {key: value.detach().cpu().numpy() for key, value in dct.items()}
        for key, value in dct.items():
            self.predictions[key].append(value)

    def on_loader_end(self, state: RunnerState):
        if self.best_only and not state.metrics.is_best:
            return

        self.predictions = {
            key: np.concatenate(value, axis=0)
            for key, value in self.predictions.items()
        }
        if self.out_prefix is not None:
            for key, value in self.predictions.items():
                suffix = '.'.join([state.loader_name, key])
                np.save(f'{self.out_prefix}/{suffix}.npy', value)
