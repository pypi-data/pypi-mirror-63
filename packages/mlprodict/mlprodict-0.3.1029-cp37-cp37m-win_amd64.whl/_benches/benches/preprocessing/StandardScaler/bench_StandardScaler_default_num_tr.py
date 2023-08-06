import numpy  # pylint: disable=W0611
from onnx.defs import onnx_opset_version
# Import specific to this model.
from sklearn.preprocessing import StandardScaler


from mlprodict.asv_benchmark import _CommonAsvSklBenchmarkTransform
from mlprodict.onnx_conv import to_onnx  # pylint: disable=W0611
from mlprodict.onnxrt import OnnxInference  # pylint: disable=W0611


class StandardScaler_default_num_tr_benchTransform(
        _CommonAsvSklBenchmarkTransform):
    """
    :epkg:`asv` example for a transform,
    Full template can be found in
    `common_asv_skl.py <https://github.com/sdpython/mlprodict/blob/
    master/mlprodict/asv_benchmark/common_asv_skl.py>`_.
    """
    params = [
        ['skl', 'pyrtc'],
        [1, 10, 100, 1000, 10000, 100000],
        [4, 20],
        [12],
        ['float'],
        [{}],
    ]

    par_modelname = 'StandardScaler'
    par_extra = {
    }
    chk_method_name = 'transform'
    par_scenario = 'default'
    par_problem = 'num-tr'
    par_optimisation = None
    par_convopts = None

    def setup_cache(self):  # pylint: disable=W0235
        super().setup_cache()

    def _create_model(self):
        return StandardScaler()
