# coding=UTF-8
# ex:ts=4:sw=4:et=on

# Copyright (c) 2013, Mathijs Dumon
# All rights reserved.
# Complete license can be found in the LICENSE file.

import logging
logger = logging.getLogger(__name__)

from mvc.models.properties import (
    IntegerProperty, ReadOnlyMixin, FloatProperty, LabeledProperty
)

from pyxrd.generic.models import PyXRDLine, ChildModel
from pyxrd.calculations.statistics import Rpw, Rp, derive

class Statistics(ChildModel):
    # PROPERTIES:
    specimen = property(ChildModel.parent.fget, ChildModel.parent.fset)

    @IntegerProperty(default=0, label="Points", visible=False, mix_with=(ReadOnlyMixin,))
    def points(self):
        try:
            e_ex, e_ey, e_cx, e_cy = self.specimen.get_exclusion_xy() #@UnusedVariable
            return e_ex.size
        except: pass
        return 0

    Rp = FloatProperty(default=None, label="Rp", visible=True)
    Rwp = FloatProperty(default=None, label="Rwp", visible=True)
    Rpder = FloatProperty(default=None, label="Rpder", visible=True)

    residual_pattern = LabeledProperty(default=None, label="Residual pattern")
    der_exp_pattern = LabeledProperty(default=None, label="Derived experimental pattern")
    der_calc_pattern = LabeledProperty(default=None, label="Derived calculated pattern")
    der_residual_pattern = LabeledProperty(default=None, label="Derived residual pattern")

    # ------------------------------------------------------------
    #      Initialization and other internals
    # ------------------------------------------------------------
    def __init__(self, *args, **kwargs):
        super(Statistics, self).__init__(*args, **kwargs)
        self.observe_model(self.parent)

    # ------------------------------------------------------------
    #      Notifications of observable properties
    # ------------------------------------------------------------
    @ChildModel.observe("parent", assign=True, after=True)
    def on_parent_changed(self, model, prop_name, info):
        self.update_statistics()

    # ------------------------------------------------------------
    #      Methods & Functions
    # ------------------------------------------------------------
    def _get_experimental(self):
        if self.specimen is not None:
            x, y = self.specimen.experimental_pattern.get_xy_data()
            return x.copy(), y.copy()
        else:
            return None, None
    def _get_calculated(self):
        if self.specimen is not None:
            x, y = self.specimen.calculated_pattern.get_xy_data()
            return x.copy(), y.copy()
        else:
            return None, None

    def scale_factor_y(self, offset):
        return self.specimen.scale_factor_y(offset) if self.specimen else (1.0, offset)

    def update_statistics(self, derived=False):
        # Clear factors:
        self.Rp = 0
        self.Rwp = 0
        self.Rpder = 0

        # Setup lines if not yet done:
        if self.residual_pattern == None:
            self.residual_pattern = PyXRDLine(label="Residual", color="#000000", lw=0.5, parent=self)

        if self.der_exp_pattern == None:
            self.der_exp_pattern = PyXRDLine(label="Exp. 1st der.", color="#000000", lw=2, parent=self)

        if self.der_calc_pattern == None:
            self.der_calc_pattern = PyXRDLine(label="Calc. 1st der.", color="#AA0000", lw=2, parent=self)

        if self.der_residual_pattern == None:
            self.der_residual_pattern = PyXRDLine(label="1st der. residual", color="#AA00AA", lw=1, parent=self)

        # Get data:
        exp_x, exp_y = self._get_experimental()
        cal_x, cal_y = self._get_calculated()
        der_exp_y, der_cal_y = None, None
        del cal_x # don't need this, is the same as exp_x

        # Try to get statistics, if it fails, just clear and inform the user
        try:
            if cal_y is not None and exp_y is not None and cal_y.size > 0 and exp_y.size > 0:
                # Get the selector for areas to consider in the statistics:
                selector = self.specimen.get_exclusion_selector()

                if derived:
                    # Calculate and set first derivate patterns:
                    der_exp_y, der_cal_y = derive(exp_y), derive(cal_y)
                    self.der_exp_pattern.set_data(exp_x, der_exp_y)
                    self.der_calc_pattern.set_data(exp_x, der_cal_y)

                # Calculate and set residual pattern:
                self.residual_pattern.set_data(exp_x, exp_y - cal_y)
                if derived:
                    self.der_residual_pattern.set_data(exp_x, der_exp_y - der_cal_y)

                # Calculate 'included' R values:
                self.Rp = Rp(exp_y[selector], cal_y[selector])
                self.Rwp = Rpw(exp_y[selector], cal_y[selector])
                if derived:
                    self.Rpder = Rp(der_exp_y[selector], der_cal_y[selector])
            else:
                self.residual_pattern.clear()
                self.der_exp_pattern.clear()
                self.der_calc_pattern.clear()
        except:
            self.residual_pattern.clear()
            self.der_exp_pattern.clear()
            self.der_calc_pattern.clear()
            logger.error("Error occurred when trying to calculate statistics, aborting calculation!")
            raise

    pass # end of class
