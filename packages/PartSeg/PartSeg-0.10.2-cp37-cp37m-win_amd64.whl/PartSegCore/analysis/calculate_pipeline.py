import typing

from PartSegCore.io_utils import HistoryElement
from PartSegCore.class_generator import BaseSerializableClass
from PartSegCore.segmentation import RestartableAlgorithm
from PartSegCore.analysis.analysis_utils import SegmentationPipeline
from PartSegCore.analysis.algorithm_description import analysis_algorithm_dict
from PartSegCore.mask_create import calculate_mask
from PartSegImage import Image
import numpy as np


def _empty_fun(_a1, _a2):
    pass


class PipelineResult(BaseSerializableClass):
    segmentation: np.ndarray
    full_segmentation: np.ndarray
    mask: np.ndarray
    history: typing.List[HistoryElement]
    description: str


def calculate_pipeline(image: Image, mask: typing.Optional[np.ndarray], pipeline: SegmentationPipeline, report_fun):
    history = []
    report_fun("max", 2 * len(pipeline.mask_history) + 1)
    for i, el in enumerate(pipeline.mask_history):
        algorithm: RestartableAlgorithm = analysis_algorithm_dict[el.segmentation.algorithm]()
        algorithm.set_image(image)
        algorithm.set_mask(mask)
        algorithm.set_parameters(**el.segmentation.values)
        result = algorithm.calculation_run(_empty_fun)
        segmentation = result.segmentation
        full_segmentation = result.full_segmentation
        report_fun("step", 2 * i + 1)
        new_mask = calculate_mask(el.mask_property, segmentation, mask, image.spacing)
        segmentation_parameters = {"algorithm_name": el.segmentation.name, "values": el.segmentation.values}
        history.append(
            HistoryElement.create(segmentation, full_segmentation, mask, segmentation_parameters, el.mask_property)
        )
        report_fun("step", 2 * i + 2)
        mask = new_mask
    algorithm: RestartableAlgorithm = analysis_algorithm_dict[pipeline.segmentation.algorithm]()
    algorithm.set_image(image)
    algorithm.set_mask(mask)
    algorithm.set_parameters(**pipeline.segmentation.values)
    result = algorithm.calculation_run(_empty_fun)
    segmentation = result.segmentation
    full_segmentation = result.full_segmentation
    report_fun("step", 2 * len(pipeline.mask_history) + 1)
    return PipelineResult(segmentation, full_segmentation, mask, history, algorithm.get_info_text())
