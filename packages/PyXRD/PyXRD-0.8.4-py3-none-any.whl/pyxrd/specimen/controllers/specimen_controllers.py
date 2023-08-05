# coding=UTF-8
# ex:ts=4:sw=4:et=on

# Copyright (c) 2013, Mathijs Dumon
# All rights reserved.
# Complete license can be found in the LICENSE file.

import os, locale
import logging
logger = logging.getLogger(__name__)

from mvc.adapters.gtk_support.dialogs.dialog_factory import DialogFactory
from mvc.adapters.gtk_support.tree_view_adapters import wrap_xydata_to_treemodel
from mvc.adapters import DummyAdapter

from pyxrd.generic.controllers import BaseController, DialogController, TreeViewMixin
from pyxrd.generic.views.treeview_tools import setup_treeview, new_text_column
from pyxrd.file_parsers.xrd_parsers import xrd_parsers
from pyxrd.file_parsers.exc_parsers import exc_parsers

from pyxrd.goniometer.controllers import InlineGoniometerController

from pyxrd.generic.controllers.line_controllers import (
    LinePropertiesController,
    BackgroundController,
    SmoothDataController,
    AddNoiseController,
    ShiftDataController,
    StripPeakController,
    CalculatePeakPropertiesController
)

from pyxrd.generic.views.line_views import (
    BackgroundView,
    SmoothDataView,
    AddNoiseView,
    ShiftDataView,
    StripPeakView,
    CalculatePeakPropertiesView
)

class SpecimenController(DialogController, TreeViewMixin):
    """
        Specimen controller.
    """

    widget_handlers = {
        'custom':  'custom_handler',
    }

    # ------------------------------------------------------------
    #      Initialization and other internals
    # ------------------------------------------------------------
    @staticmethod
    def custom_handler(self, prop, widget):
        if prop.label in ("goniometer"):
            self.gonio_ctrl = InlineGoniometerController(view=self.view.gonio_view, model=self.model.goniometer, parent=self)
            ad = DummyAdapter(controller=self, prop=prop) # TODO FIXME
            return ad

    def setup_experimental_pattern_tree_view(self, store, widget):
        """
            Creates the experimental data TreeView layout and behavior
        """
        setup_treeview(widget, store,
            on_cursor_changed=self.on_exp_data_tv_cursor_changed,
            sel_mode='MULTIPLE')
        store.connect('columns_changed', self.on_exp_columns_changed)
        self.update_exp_treeview(widget)
        # Other properties:
        self.exp_line_ctrl = LinePropertiesController(model=self.model.experimental_pattern, view=self.view.exp_line_view, parent=self)

    def setup_calculated_pattern_tree_view(self, store, widget):
        """
            Creates the calculated data TreeView layout and behavior
        """
        setup_treeview(widget, store,
            on_cursor_changed=self.on_exp_data_tv_cursor_changed,
            sel_mode='NONE')
        store.connect('columns_changed', self.on_calc_columns_changed)
        self.update_calc_treeview(widget)
        # Other properties:
        self.calc_line_ctrl = LinePropertiesController(model=self.model.calculated_pattern, view=self.view.calc_line_view, parent=self)

    def setup_exclusion_ranges_tree_view(self, store, widget):
        """
            Creates the exclusion ranges TreeView layout and behavior
        """
        setup_treeview(widget, store,
            on_cursor_changed=self.on_exclusion_ranges_tv_cursor_changed,
            sel_mode='MULTIPLE')
        
        def data_func(col, cell, model, iter, colnr):
            cell.set_property("text", "%g" % model.get(iter, colnr)[0])
        
        widget.append_column(new_text_column(
            'From [°2θ]', text_col=store.c_x, editable=True,
            data_func = (data_func, (store.c_x,)),
            edited_callback=(self.on_xy_data_cell_edited, (self.model.exclusion_ranges, 0)),
            resizable=True, expand=True))
        widget.append_column(new_text_column(
            'To [°2θ]', text_col=store.c_y, editable=True,
            data_func = (data_func, (store.c_y,)),
            edited_callback=(self.on_xy_data_cell_edited, (self.model.exclusion_ranges, 1)),
            resizable=True, expand=True))

    # ------------------------------------------------------------
    #      Methods & Functions
    # ------------------------------------------------------------
    def get_experimental_pattern_tree_model(self):
        return wrap_xydata_to_treemodel(self.model, type(self.model).experimental_pattern)
    def get_calculated_pattern_tree_model(self):
        return wrap_xydata_to_treemodel(self.model, type(self.model).calculated_pattern)
    def get_exclusion_ranges_tree_model(self):
        return wrap_xydata_to_treemodel(self.model, type(self.model).exclusion_ranges)

    #used to keep a permanent fix on a child controller, prevents early GC
    _child_ctrl_ref = None

    def update_calc_treeview(self, tv):
        """
            Updates the calculated pattern TreeView layout
        """
        model = self.get_calculated_pattern_tree_model()

        for column in tv.get_columns():
            tv.remove_column(column)

        def get_num(column, cell, model, itr, col_id):
            cell.set_property('text', '%.3f' % model.get_value(itr, col_id))

        tv.append_column(new_text_column('2θ', data_func=(get_num, (model.c_x,))))
        tv.append_column(new_text_column('Cal', data_func=(get_num, (model.c_y,)) ))
        for i in range(model.get_n_columns() - 2):
            tv.append_column(new_text_column(
                self.model.calculated_pattern.get_y_name(i), data_func=(get_num, (i+2,))))

    def update_exp_treeview(self, tv):
        """
            Updates the experimental pattern TreeView layout
        """
        model = self.get_experimental_pattern_tree_model()

        for column in tv.get_columns():
            tv.remove_column(column)

        def get_num(column, cell, model, itr, col_id):
            cell.set_property('text', '%.3f' % model.get_value(itr, col_id))
        
        n_columns = model.get_n_columns()
        
        if n_columns > 2:
            for i in range(n_columns):
                tv.append_column(new_text_column(
                    self.model.calculated_pattern.get_y_name(i), editable=True,
                    edited_callback=(self.on_xy_data_cell_edited, (self.model.experimental_pattern, i)),
                    data_func=(get_num, (i,))
                ))
        else:
            # X Column:
            tv.append_column(new_text_column(
                '°2θ', editable=True,
                data_func=(get_num, (model.c_x,)),
                edited_callback=(self.on_xy_data_cell_edited, (self.model.experimental_pattern, 0))))
            # Y Column:
            tv.append_column(new_text_column(
                'Intensity', editable=True,
                data_func=(get_num, (model.c_y,)),
                edited_callback=(self.on_xy_data_cell_edited, (self.model.experimental_pattern, 1))))

    def remove_background(self):
        """
            Opens the 'remove background' dialog.
        """
        bg_view = BackgroundView(parent=self.view)
        self._child_ctrl_ref = BackgroundController(model=self.model.experimental_pattern, view=bg_view, parent=self)
        bg_view.present()

    def add_noise(self):
        """
            Opens the 'add noise' dialog.
        """
        an_view = AddNoiseView(parent=self.view)
        self._child_ctrl_ref = AddNoiseController(model=self.model.experimental_pattern, view=an_view, parent=self)
        an_view.present()

    def smooth_data(self):
        """
            Opens the 'smooth data' dialog.
        """
        sd_view = SmoothDataView(parent=self.view)
        self._child_ctrl_ref = SmoothDataController(model=self.model.experimental_pattern, view=sd_view, parent=self)
        sd_view.present()

    def shift_data(self):
        """
            Opens the 'shift data' dialog.
        """
        sh_view = ShiftDataView(parent=self.view)
        self._child_ctrl_ref = ShiftDataController(model=self.model.experimental_pattern, view=sh_view, parent=self)
        sh_view.present()

    def strip_peak(self):
        """
            Opens the 'strip peak' dialog.
        """
        st_view = StripPeakView(parent=self.view)
        self._child_ctrl_ref = StripPeakController(model=self.model.experimental_pattern, view=st_view, parent=self)
        st_view.present()

    def peak_properties(self):
        """
            Opens the 'peak properties' dialog.
        """
        pa_view = CalculatePeakPropertiesView(parent=self.view)
        self._child_ctrl_ref = CalculatePeakPropertiesController(model=self.model.experimental_pattern, view=pa_view, parent=self)
        pa_view.present()

    # ------------------------------------------------------------
    #      GTK Signal handlers
    # ------------------------------------------------------------
    def on_calc_columns_changed(self, *args, **kwargs):
        self.update_calc_treeview(self.view["specimen_calculated_pattern"])

    def on_exp_columns_changed(self, *args, **kwargs):
        self.update_exp_treeview(self.view["specimen_experimental_pattern"])

    def on_btn_ok_clicked(self, event):
        self.parent.pop_status_msg('edit_specimen')
        return super(SpecimenController, self).on_btn_ok_clicked(event)

    def on_exclusion_ranges_tv_cursor_changed(self, tv):
        path, col = tv.get_cursor()  # @UnusedVariable
        self.view["btn_del_exclusion_ranges"].set_sensitive(path is not None)
        return True

    def on_exp_data_tv_cursor_changed(self, tv):
        path, col = tv.get_cursor()  # @UnusedVariable
        self.view["btn_del_experimental_data"].set_sensitive(path is not None)
        return True

    def on_add_experimental_data_clicked(self, widget):
        self.model.experimental_pattern.append(0, 0)
        return True

    def on_add_exclusion_range_clicked(self, widget):
        self.model.exclusion_ranges.append(0, 0)
        return True

    def on_del_experimental_data_clicked(self, widget):
        paths = self.get_selected_paths(self.view["specimen_experimental_pattern"])
        if paths is not None:
            self.model.experimental_pattern.remove_from_indeces(*paths)
        return True

    def on_del_exclusion_ranges_clicked(self, widget):
        paths = self.get_selected_paths(self.view["specimen_exclusion_ranges"])
        if paths is not None:
            self.model.exclusion_ranges.remove_from_indeces(*paths)
        return True

    def on_xy_data_cell_edited(self, cell, path, new_text, model, col):
        try:
            value = float(locale.atof(new_text))
        except ValueError:
            logger.exception("ValueError: Invalid literal for float(): '%s'" % new_text)
        else:
            model.set_value(int(path), col, value)
        return True

    def on_import_exclusion_ranges_clicked(self, widget, data=None):
        def on_confirm(dialog):
            def on_accept(dialog):
                filename = dialog.filename
                parser = dialog.parser
                message = "An unexpected error has occured when trying to parse %s:\n\n<i>" % os.path.basename(filename)
                message += "{}</i>\n\n"
                message += "This is most likely caused by an invalid or unsupported file format."

                with DialogFactory.error_dialog_handler(message, parent=self.view.get_toplevel(), reraise=False):
                    self.model.exclusion_ranges.load_data(parser, filename, clear=True)
            DialogFactory.get_load_dialog(
                title="Import exclusion ranges", parent=self.view.get_top_widget(),
                filters=exc_parsers.get_import_file_filters()
            ).run(on_accept)
        DialogFactory.get_confirmation_dialog(
            "Importing exclusion ranges will erase all current data.\nAre you sure you want to continue?",
            parent=self.view.get_top_widget()
        ).run(on_confirm)

    def on_export_exclusion_ranges_clicked(self, widget, data=None):
        def on_accept(dialog):
            filename = dialog.filename
            parser = dialog.parser
            message = "An unexpected error has occurred when trying to save '%s'.\n" % os.path.basename(filename)
            message += "Contact the developer about this!"
            with DialogFactory.error_dialog_handler(message, parent=self.view.get_toplevel(), reraise=False):
                header = "%s %s" % (self.model.name, self.model.sample_name)
                self.model.exclusion_ranges.save_data(parser, filename, header=header)
        DialogFactory.get_save_dialog(
            "Select file for exclusion ranges export",
            parent=self.view.get_top_widget(), filters=exc_parsers.get_export_file_filters()
        ).run(on_accept)

    def on_replace_experimental_data(self, *args, **kwargs):
        def on_accept(dialog):
            filename = dialog.filename
            parser = dialog.parser
            message = "An unexpected error has occurred when trying to parse '%s'.\n" % os.path.basename(filename)
            message += "This is most likely caused by an invalid or unsupported file format."
            with DialogFactory.error_dialog_handler(message, parent=self.view.get_toplevel(), reraise=False):
                self.model.experimental_pattern.load_data(parser, filename, clear=True)
        DialogFactory.get_load_dialog(
            "Open XRD file for import", parent=self.view.get_top_widget(),
            filters=xrd_parsers.get_import_file_filters()
        ).run(on_accept)
        return True

    def on_btn_import_experimental_data_clicked(self, widget, data=None):
        def on_confirm(dialog):
            self.on_replace_experimental_data()
        DialogFactory.get_confirmation_dialog(
            "Importing a new experimental file will erase all current data.\nAre you sure you want to continue?",
            parent=self.view.get_top_widget()
        ).run(on_confirm)
        return True

    def on_export_experimental_data(self, *args, **kwargs):
        return self._export_data(self.model.experimental_pattern)

    def on_btn_export_experimental_data_clicked(self, widget, data=None):
        return self.on_export_experimental_data()

    def on_btn_export_calculated_data_clicked(self, widget, data=None):
        return self._export_data(self.model.calculated_pattern)

    def _export_data(self, line):
        def on_accept(dialog):
            filename = dialog.filename
            parser = dialog.parser
            message = "An unexpected error has occurred when trying to save to '%s'." % os.path.basename(filename)
            with DialogFactory.error_dialog_handler(message, parent=self.view.get_toplevel(), reraise=False):
                line.save_data(parser, filename, **self.model.get_export_meta_data())
        ext_less_fname = os.path.splitext(self.model.name)[0]
        DialogFactory.get_save_dialog(
            "Select file for export", parent=self.view.get_top_widget(),
            filters=xrd_parsers.get_export_file_filters(), current_name=ext_less_fname
        ).run(on_accept)

    pass # end of class

class StatisticsController(BaseController):

    def register_adapters(self):
        if self.model is not None:
            for name in self.model.get_properties():
                if name in self.model.__have_no_widget__:
                    pass
                else:
                    self.adapt(name)
            return

    pass # end of class
