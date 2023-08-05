# coding=UTF-8
# ex:ts=4:sw=4:et=on

# Copyright (c) 2013, Mathijs Dumon
# All rights reserved.
# Complete license can be found in the LICENSE file.

from random import choice
import numpy as np

from mvc.models.properties import LabeledProperty
from mvc.models.properties.signal_mixin import SignalMixin
from mvc.models.properties.observe_mixin import ObserveMixin

from pyxrd.generic.io import storables, get_case_insensitive_glob
from pyxrd.generic.models.lines import PyXRDLine
from pyxrd.refinement.refinables.metaclasses import PyXRDRefinableMeta
from pyxrd.refinement.refinables.mixins import RefinementGroup
from pyxrd.file_parsers.xrd_parsers import xrd_parsers

from .abstract_phase import AbstractPhase

@storables.register()
class RawPatternPhase(RefinementGroup, AbstractPhase, metaclass=PyXRDRefinableMeta):

    # MODEL INTEL:
    class Meta(AbstractPhase.Meta):
        store_id = "RawPatternPhase"
        file_filters = [
            ("Phase file", get_case_insensitive_glob("*.PHS")),
        ]
        rp_filters = xrd_parsers.get_import_file_filters()
        rp_export_filters = xrd_parsers.get_export_file_filters()

    _data_object = None
    @property
    def data_object(self):
        self._data_object.type = "RawPatternPhase"

        self._data_object.raw_pattern_x = self.raw_pattern.data_x
        self._data_object.raw_pattern_y = self.raw_pattern.data_y[:, 0]
        self._data_object.apply_lpf = False
        self._data_object.apply_correction = False

        return self._data_object

    project = property(AbstractPhase.parent.fget, AbstractPhase.parent.fset)

    @property
    def refine_title(self):
        return "Raw Pattern Phase"

    @property
    def is_refinable(self):
        return False

    @property
    def children_refinable(self):
        return False

    @property
    def refinables(self):
        return []

    raw_pattern = LabeledProperty(
        default=None, text="Raw pattern",
        visible=True, persistent=True, tabular=True,
        inheritable=True, inherit_flag="inherit_CSDS_distribution", inherit_from="based_on.CSDS_distribution",
        signal_name="data_changed",
        mix_with=(SignalMixin, ObserveMixin,)
    )

    @property
    def spec_max_display_y(self):
        """The maximum intensity (y-axis) of the current loaded profile"""
        _max = 0.0
        if self.raw_pattern is not None:
            _max = max(_max, np.max(self.raw_pattern.max_display_y))
        return _max

    # ------------------------------------------------------------
    #      Initialization and other internals
    # ------------------------------------------------------------
    def __init__(self, *args, **kwargs):
        my_kwargs = self.pop_kwargs(kwargs,
            *[prop.label for prop in RawPatternPhase.Meta.get_local_persistent_properties()]
        )
        super(RawPatternPhase, self).__init__(*args, **kwargs)
        kwargs = my_kwargs

        with self.data_changed.hold():
            self.raw_pattern = PyXRDLine(
                data=self.get_kwarg(kwargs, None, "raw_pattern"),
                parent=self
            )
            self.display_color = self.get_kwarg(kwargs, choice(self.line_colors), "display_color")
            self.inherit_display_color = self.get_kwarg(kwargs, False, "inherit_display_color")

    def __repr__(self):
        return "RawPatternPhase(name='%s')" % (self.name)

    # ------------------------------------------------------------
    #      Notifications of observable properties
    # ------------------------------------------------------------
    @AbstractPhase.observe("data_changed", signal=True)
    def notify_data_changed(self, model, prop_name, info):
        self.data_changed.emit() # propagate signal

    pass #end of class
