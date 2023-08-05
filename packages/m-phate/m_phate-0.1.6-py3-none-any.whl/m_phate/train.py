import numpy as np
import os
import scprep

scprep.utils.check_version("keras", "2.2")  # noqa
scprep.utils.check_version("tensorflow", "1.13")  # noqa

import keras

try:
    from tensorflow import GPUOptions, ConfigProto
except ImportError:
    from tensorflow.compat.v1 import GPUOptions, ConfigProto

def build_config(limit_gpu_fraction=0.2, limit_cpu_fraction=10):
    if limit_gpu_fraction > 0:
        os.environ["CUDA_VISIBLE_DEVICES"] = "0"
        gpu_options = GPUOptions(
            allow_growth=True,
            per_process_gpu_memory_fraction=limit_gpu_fraction)
        config = ConfigProto(gpu_options=gpu_options)
    else:
        os.environ["CUDA_VISIBLE_DEVICES"] = ""
        config = ConfigProto(device_count={'GPU': 0})
    if limit_cpu_fraction is not None:
        if limit_cpu_fraction == 0:
            cpu_count = 1
        if limit_cpu_fraction < 0:
            # -2 gives all CPUs except 1
            cpu_count = max(
                1, int(os.cpu_count() + limit_cpu_fraction + 1))
        elif limit_cpu_fraction < 1:
            # 0.5 gives 50% of available CPUs
            cpu_count = max(
                1, int(os.cpu_count() * limit_cpu_fraction))
        else:
            # 2 gives 2 CPUs
            cpu_count = int(limit_cpu_fraction)
        config.inter_op_parallelism_threads = cpu_count
        config.intra_op_parallelism_threads = cpu_count
        os.environ['OMP_NUM_THREADS'] = str(1)
        os.environ['MKL_NUM_THREADS'] = str(cpu_count)
    return config


class _History(keras.callbacks.Callback):

    def __init__(self, data, model, save_weights=False, *args, **kwargs):
        self.trace_data = data
        self.trace_model = model
        self.save_weights = save_weights
        if save_weights:
            self.weights = []
        self.trace = []
        super().__init__(*args, **kwargs)

    def _record_trace(self):
        if len(self.trace_model.outputs) > 1:
            self.trace.append(
                np.vstack([data.T for data in self.trace_model.predict(
                    self.trace_data)]))
        else:
            self.trace.append(self.trace_model.predict(
                    self.trace_data).T)
        if self.save_weights:
            self.weights.append(self.trace_model.layers[1].get_weights()[0])


class TraceHistory(_History):

    def on_epoch_end(self, epoch, logs):
        self._record_trace()
        return super().on_epoch_end(epoch, logs)


class BatchTraceHistory(_History):

    def on_batch_end(self, epoch, logs):
        self._record_trace()
        return super().on_batch_end(epoch, logs)
