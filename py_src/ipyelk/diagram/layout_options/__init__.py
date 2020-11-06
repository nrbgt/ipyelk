"""Set of Widgets to help configure Elk Layout Options
https://www.eclipse.org/elk/reference/options.html
"""
# Copyright (c) 2020 Dane Freeman.
# Distributed under the terms of the Modified BSD License.

from .edge_options import (
    EadesRepulsion,
    EdgeCenterLabelPlacementStrategy,
    EdgeEdgeLayerSpacing,
    EdgeLabelPlacement,
    EdgeLabelSideSelection,
    EdgeLabelSpacing,
    EdgeNodeLayerSpacing,
    EdgeNodeSpacing,
    EdgeRouting,
    EdgeSpacing,
    EdgeThickness,
    EdgeType,
    FeedbackEdges,
    MergeEdges,
    MergeHierarchyCrossingEdges,
)
from .layout import LayoutAlgorithm
from .node_options import (
    ActivateInsideSelfLoops,
    HierarchyHandling,
    NodeLabelPlacement,
    NodeSizeConstraints,
    NodeSizeMinimum,
    NodeSizeOptions,
)
from .port_options import (
    AdditionalPortSpace,
    PortAnchorOffset,
    PortBorderOffset,
    PortConstraints,
    PortIndex,
    PortLabelPlacement,
    PortSide,
    TreatPortLabelsAsGroup,
)
from .selection_widgets import LayoutOptionWidget, OptionsWidget, SpacingOptionWidget
from .spacing_options import (
    CommentCommentSpacing,
    CommentNodeSpacing,
    ComponentsSpacing,
    LabelNodeSpacing,
    LabelSpacing,
    NodeSpacing,
    SeparateConnectedComponents,
)

__all__ = [
    "ActivateInsideSelfLoops",
    "AdditionalPortSpace",
    "CommentCommentSpacing",
    "CommentNodeSpacing",
    "ComponentsSpacing",
    "EadesRepulsion",
    "EdgeCenterLabelPlacementStrategy" "EdgeEdgeLayerSpacing",
    "EdgeCenterLabelPlacementStrategy",
    "EdgeEdgeLayerSpacing",
    "EdgeLabelPlacement",
    "EdgeLabelSideSelection",
    "EdgeLabelSpacing",
    "EdgeLabelSpacing",
    "EdgeNodeLayerSpacing",
    "EdgeNodeLayerSpacing",
    "EdgeNodeSpacing",
    "EdgeRouting",
    "EdgeSpacing",
    "EdgeThickness",
    "EdgeType",
    "FeedbackEdges",
    "HierarchyHandling",
    "LabelNodeSpacing",
    "LabelSpacing",
    "LayoutAlgorithm",
    "LayoutOptionWidget",
    "MergeEdges",
    "MergeHierarchyCrossingEdges",
    "NodeLabelPlacement",
    "NodeSizeConstraints",
    "NodeSizeMinimum",
    "NodeSizeOptions",
    "NodeSpacing",
    "OptionsWidget",
    "PortAnchorOffset",
    "PortBorderOffset",
    "PortConstraints",
    "PortIndex",
    "PortLabelPlacement",
    "PortSide",
    "SeparateConnectedComponents",
    "SpacingOptionWidget",
    "TreatPortLabelsAsGroup",
]
