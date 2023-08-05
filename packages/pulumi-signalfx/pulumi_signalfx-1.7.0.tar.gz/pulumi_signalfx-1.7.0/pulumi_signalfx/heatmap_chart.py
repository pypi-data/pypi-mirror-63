# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from typing import Union
from . import utilities, tables

class HeatmapChart(pulumi.CustomResource):
    color_range: pulumi.Output[dict]
    """
    Values and color for the color range. Example: `color_range : { min : 0, max : 100, color : "#0000ff" }`. Look at this [link](https://docs.signalfx.com/en/latest/charts/chart-options-tab.html).
    
      * `color` (`str`) - The color range to use. Must be either gray, blue, navy, orange, yellow, magenta, purple, violet, lilac, green, aquamarine.
      * `maxValue` (`float`) - The maximum value within the coloring range.
      * `minValue` (`float`) - The minimum value within the coloring range.
    """
    color_scales: pulumi.Output[list]
    """
    Single color range including both the color to display for that range and the borders of the range. Example: `[{ gt = 60, color = "blue" }, { lte = 60, color = "yellow" }]`. Look at this [link](https://docs.signalfx.com/en/latest/charts/chart-options-tab.html).
    
      * `color` (`str`) - The color range to use. Must be either gray, blue, navy, orange, yellow, magenta, purple, violet, lilac, green, aquamarine.
      * `gt` (`float`) - Indicates the lower threshold non-inclusive value for this range.
      * `gte` (`float`) - Indicates the lower threshold inclusive value for this range.
      * `lt` (`float`) - Indicates the upper threshold non-inculsive value for this range.
      * `lte` (`float`) - Indicates the upper threshold inclusive value for this range.
    """
    description: pulumi.Output[str]
    """
    Description of the chart.
    """
    disable_sampling: pulumi.Output[bool]
    """
    If `false`, samples a subset of the output MTS, which improves UI performance. `false` by default.
    """
    group_bies: pulumi.Output[list]
    """
    Properties to group by in the heatmap (in nesting order).
    """
    hide_timestamp: pulumi.Output[bool]
    """
    Whether to show the timestamp in the chart. `false` by default.
    """
    max_delay: pulumi.Output[float]
    """
    How long (in seconds) to wait for late datapoints.
    """
    minimum_resolution: pulumi.Output[float]
    """
    The minimum resolution (in seconds) to use for computing the underlying program.
    """
    name: pulumi.Output[str]
    """
    Name of the chart.
    """
    program_text: pulumi.Output[str]
    """
    Signalflow program text for the chart. More info at <https://developers.signalfx.com/docs/signalflow-overview>.
    """
    refresh_interval: pulumi.Output[float]
    """
    How often (in seconds) to refresh the values of the heatmap.
    """
    sort_by: pulumi.Output[str]
    """
    The property to use when sorting the elements. Must be prepended with `+` for ascending or `-` for descending (e.g. `-foo`).
    """
    unit_prefix: pulumi.Output[str]
    """
    Must be `"Metric"` or `"Binary`". `"Metric"` by default.
    """
    url: pulumi.Output[str]
    def __init__(__self__, resource_name, opts=None, color_range=None, color_scales=None, description=None, disable_sampling=None, group_bies=None, hide_timestamp=None, max_delay=None, minimum_resolution=None, name=None, program_text=None, refresh_interval=None, sort_by=None, unit_prefix=None, __props__=None, __name__=None, __opts__=None):
        """
        This chart type displays the specified plot in a heatmap fashion. This format is similar to the [Infrastructure Navigator](https://signalfx-product-docs.readthedocs-hosted.com/en/latest/built-in-content/infra-nav.html#infra), with squares representing each source for the selected metric, and the color of each square representing the value range of the metric.
        
        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[dict] color_range: Values and color for the color range. Example: `color_range : { min : 0, max : 100, color : "#0000ff" }`. Look at this [link](https://docs.signalfx.com/en/latest/charts/chart-options-tab.html).
        :param pulumi.Input[list] color_scales: Single color range including both the color to display for that range and the borders of the range. Example: `[{ gt = 60, color = "blue" }, { lte = 60, color = "yellow" }]`. Look at this [link](https://docs.signalfx.com/en/latest/charts/chart-options-tab.html).
        :param pulumi.Input[str] description: Description of the chart.
        :param pulumi.Input[bool] disable_sampling: If `false`, samples a subset of the output MTS, which improves UI performance. `false` by default.
        :param pulumi.Input[list] group_bies: Properties to group by in the heatmap (in nesting order).
        :param pulumi.Input[bool] hide_timestamp: Whether to show the timestamp in the chart. `false` by default.
        :param pulumi.Input[float] max_delay: How long (in seconds) to wait for late datapoints.
        :param pulumi.Input[float] minimum_resolution: The minimum resolution (in seconds) to use for computing the underlying program.
        :param pulumi.Input[str] name: Name of the chart.
        :param pulumi.Input[str] program_text: Signalflow program text for the chart. More info at <https://developers.signalfx.com/docs/signalflow-overview>.
        :param pulumi.Input[float] refresh_interval: How often (in seconds) to refresh the values of the heatmap.
        :param pulumi.Input[str] sort_by: The property to use when sorting the elements. Must be prepended with `+` for ascending or `-` for descending (e.g. `-foo`).
        :param pulumi.Input[str] unit_prefix: Must be `"Metric"` or `"Binary`". `"Metric"` by default.
        
        The **color_range** object supports the following:
        
          * `color` (`pulumi.Input[str]`) - The color range to use. Must be either gray, blue, navy, orange, yellow, magenta, purple, violet, lilac, green, aquamarine.
          * `maxValue` (`pulumi.Input[float]`) - The maximum value within the coloring range.
          * `minValue` (`pulumi.Input[float]`) - The minimum value within the coloring range.
        
        The **color_scales** object supports the following:
        
          * `color` (`pulumi.Input[str]`) - The color range to use. Must be either gray, blue, navy, orange, yellow, magenta, purple, violet, lilac, green, aquamarine.
          * `gt` (`pulumi.Input[float]`) - Indicates the lower threshold non-inclusive value for this range.
          * `gte` (`pulumi.Input[float]`) - Indicates the lower threshold inclusive value for this range.
          * `lt` (`pulumi.Input[float]`) - Indicates the upper threshold non-inculsive value for this range.
          * `lte` (`pulumi.Input[float]`) - Indicates the upper threshold inclusive value for this range.

        > This content is derived from https://github.com/terraform-providers/terraform-provider-signalfx/blob/master/website/docs/r/heatmap_chart.html.markdown.
        """
        if __name__ is not None:
            warnings.warn("explicit use of __name__ is deprecated", DeprecationWarning)
            resource_name = __name__
        if __opts__ is not None:
            warnings.warn("explicit use of __opts__ is deprecated, use 'opts' instead", DeprecationWarning)
            opts = __opts__
        if opts is None:
            opts = pulumi.ResourceOptions()
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.version is None:
            opts.version = utilities.get_version()
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = dict()

            __props__['color_range'] = color_range
            __props__['color_scales'] = color_scales
            __props__['description'] = description
            __props__['disable_sampling'] = disable_sampling
            __props__['group_bies'] = group_bies
            __props__['hide_timestamp'] = hide_timestamp
            __props__['max_delay'] = max_delay
            __props__['minimum_resolution'] = minimum_resolution
            __props__['name'] = name
            if program_text is None:
                raise TypeError("Missing required property 'program_text'")
            __props__['program_text'] = program_text
            __props__['refresh_interval'] = refresh_interval
            __props__['sort_by'] = sort_by
            __props__['unit_prefix'] = unit_prefix
            __props__['url'] = None
        super(HeatmapChart, __self__).__init__(
            'signalfx:index/heatmapChart:HeatmapChart',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, color_range=None, color_scales=None, description=None, disable_sampling=None, group_bies=None, hide_timestamp=None, max_delay=None, minimum_resolution=None, name=None, program_text=None, refresh_interval=None, sort_by=None, unit_prefix=None, url=None):
        """
        Get an existing HeatmapChart resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.
        
        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[dict] color_range: Values and color for the color range. Example: `color_range : { min : 0, max : 100, color : "#0000ff" }`. Look at this [link](https://docs.signalfx.com/en/latest/charts/chart-options-tab.html).
        :param pulumi.Input[list] color_scales: Single color range including both the color to display for that range and the borders of the range. Example: `[{ gt = 60, color = "blue" }, { lte = 60, color = "yellow" }]`. Look at this [link](https://docs.signalfx.com/en/latest/charts/chart-options-tab.html).
        :param pulumi.Input[str] description: Description of the chart.
        :param pulumi.Input[bool] disable_sampling: If `false`, samples a subset of the output MTS, which improves UI performance. `false` by default.
        :param pulumi.Input[list] group_bies: Properties to group by in the heatmap (in nesting order).
        :param pulumi.Input[bool] hide_timestamp: Whether to show the timestamp in the chart. `false` by default.
        :param pulumi.Input[float] max_delay: How long (in seconds) to wait for late datapoints.
        :param pulumi.Input[float] minimum_resolution: The minimum resolution (in seconds) to use for computing the underlying program.
        :param pulumi.Input[str] name: Name of the chart.
        :param pulumi.Input[str] program_text: Signalflow program text for the chart. More info at <https://developers.signalfx.com/docs/signalflow-overview>.
        :param pulumi.Input[float] refresh_interval: How often (in seconds) to refresh the values of the heatmap.
        :param pulumi.Input[str] sort_by: The property to use when sorting the elements. Must be prepended with `+` for ascending or `-` for descending (e.g. `-foo`).
        :param pulumi.Input[str] unit_prefix: Must be `"Metric"` or `"Binary`". `"Metric"` by default.
        
        The **color_range** object supports the following:
        
          * `color` (`pulumi.Input[str]`) - The color range to use. Must be either gray, blue, navy, orange, yellow, magenta, purple, violet, lilac, green, aquamarine.
          * `maxValue` (`pulumi.Input[float]`) - The maximum value within the coloring range.
          * `minValue` (`pulumi.Input[float]`) - The minimum value within the coloring range.
        
        The **color_scales** object supports the following:
        
          * `color` (`pulumi.Input[str]`) - The color range to use. Must be either gray, blue, navy, orange, yellow, magenta, purple, violet, lilac, green, aquamarine.
          * `gt` (`pulumi.Input[float]`) - Indicates the lower threshold non-inclusive value for this range.
          * `gte` (`pulumi.Input[float]`) - Indicates the lower threshold inclusive value for this range.
          * `lt` (`pulumi.Input[float]`) - Indicates the upper threshold non-inculsive value for this range.
          * `lte` (`pulumi.Input[float]`) - Indicates the upper threshold inclusive value for this range.

        > This content is derived from https://github.com/terraform-providers/terraform-provider-signalfx/blob/master/website/docs/r/heatmap_chart.html.markdown.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()
        __props__["color_range"] = color_range
        __props__["color_scales"] = color_scales
        __props__["description"] = description
        __props__["disable_sampling"] = disable_sampling
        __props__["group_bies"] = group_bies
        __props__["hide_timestamp"] = hide_timestamp
        __props__["max_delay"] = max_delay
        __props__["minimum_resolution"] = minimum_resolution
        __props__["name"] = name
        __props__["program_text"] = program_text
        __props__["refresh_interval"] = refresh_interval
        __props__["sort_by"] = sort_by
        __props__["unit_prefix"] = unit_prefix
        __props__["url"] = url
        return HeatmapChart(resource_name, opts=opts, __props__=__props__)
    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

