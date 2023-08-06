"""
Automatically generated.
"""
from wai.annotations.core.plugin.registry._PluginRegistry import PluginRegistry
from wai.annotations.core.plugin.registry._RegistryEntry import RegistryEntry

registry = PluginRegistry(adams=RegistryEntry('wai.annotations.adams.ADAMSFormatSpecifier', 'wai.annotations 0.3.0', 'ADAMSReportReaderCLIFactory', 'FromADAMSReportCLIFactory', 'ToADAMSReportCLIFactory', 'ADAMSReportWriterCLIFactory'), coco=RegistryEntry('wai.annotations.coco.COCOFormatSpecifier', 'wai.annotations 0.3.0', 'COCOReaderCLIFactory', 'FromCOCOCLIFactory', 'ToCOCOCLIFactory', 'COCOWriterCLIFactory'), roi=RegistryEntry('wai.annotations.roi.ROIFormatSpecifier', 'wai.annotations 0.3.0', 'ROIReaderCLIFactory', 'FromROICLIFactory', 'ToROICLIFactory', 'ROIWriterCLIFactory'), tfrecords=RegistryEntry('wai.annotations.tf.TFFormatSpecifier', 'wai.annotations 0.3.0', 'TensorflowExampleReaderCLIFactory', 'FromTensorflowExampleCLIFactory', 'ToTensorflowExampleCLIFactory', 'TensorflowExampleWriterCLIFactory'), vgg=RegistryEntry('wai.annotations.vgg.VGGFormatSpecifier', 'wai.annotations 0.3.0', 'VGGReaderCLIFactory', 'FromVGGCLIFactory', 'ToVGGCLIFactory', 'VGGWriterCLIFactory'))
