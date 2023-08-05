# coding=UTF-8
# ex:ts=4:sw=4:et=on

# Copyright (c) 2013, Mathijs Dumon
# All rights reserved.
# Complete license can be found in the LICENSE file.

import os, locale

import logging
logger = logging.getLogger(__name__)

from mvc.adapters.gtk_support.treemodels.utils import create_treestore_from_directory
from mvc.adapters.gtk_support.dialogs.dialog_factory import DialogFactory

from pyxrd.generic.views.cell_renderer_tools import get_default_renderer
from pyxrd.file_parsers.wld_parsers import wld_parsers
from pyxrd.file_parsers.goniometer_parsers import goniometer_parsers

from pyxrd.data import settings
from pyxrd.generic.controllers import BaseController
from pyxrd.generic.controllers.dialog_controller import DialogController
from pyxrd.generic.controllers.objectliststore_controllers import TreeViewMixin

from pyxrd.generic.views.treeview_tools import setup_treeview, new_text_column

from pyxrd.goniometer.views import WavelengthDistributionView

class InlineGoniometerController(BaseController):
    """
        Goniometer controller. Is not expected to be used with a dialog view,
        but rather in another view. 
    """

    auto_adapt_excluded = [ 'wavelength_distribution', ]


    # ------------------------------------------------------------
    #      Initialisation and other internals
    # ------------------------------------------------------------
    def register_view(self, view):
        self.generate_import_combo()
        
        self.wld_view = WavelengthDistributionView()
        self.wld_ctrl = WavelengthDistributionController(model=self.model, view=self.wld_view, parent=self)
        
        self.update_soller_sensitivity()
        self.update_divergence_label()
        self.update_absorption_sensitivity()     

    def update_soller_sensitivity(self):
        self.view["gonio_soller1_spb"].set_sensitive(self.model.has_soller1)
        self.view["gonio_soller2_spb"].set_sensitive(self.model.has_soller2)

    def update_divergence_label(self):
        if self.model.divergence_mode == "AUTOMATIC":
            self.view["unit_divergence_lbl"].set_markup("<i>[mm]</i>")
        elif self.model.divergence_mode == "FIXED":
            self.view["unit_divergence_lbl"].set_markup("<i>[°]</i>")

    def update_absorption_sensitivity(self):
        self.view["sample_surf_density_spb"].set_sensitive(self.model.has_absorption_correction)
        self.view["absorption_spb"].set_sensitive(self.model.has_absorption_correction)

    def generate_import_combo(self):
        # TODO seperate this more the gtk level...
        self.view.import_combo_box.clear()
        
        path = settings.DATA_REG.get_directory_path("DEFAULT_GONIOS")
        cmb_model = create_treestore_from_directory(path)
        self.view.import_combo_box.set_model(cmb_model)
        cell = get_default_renderer('text')
        self.view.import_combo_box.pack_start(cell, True)
        self.view.import_combo_box.add_attribute(cell, 'text', 0)
        self.view.import_combo_box.add_attribute(cell, 'sensitive', 2)

    # ------------------------------------------------------------
    #      GTK Signal handlers
    # ------------------------------------------------------------
    def on_btn_export_gonio_clicked(self, widget, *args):
        def on_accept(dialog):
            dialog.parser.write(self.model, dialog.filename)
            self.generate_import_combo()
        DialogFactory.get_save_dialog(
            title="Select the goniometer setup file to save to",
            filters=goniometer_parsers.get_export_file_filters(),
            current_folder=settings.DATA_REG.get_directory_path("DEFAULT_GONIOS"),
            parent=self.view.parent.get_top_widget()
        ).run(on_accept)

    def on_cmb_import_gonio_changed(self, combobox, *args):
        model = combobox.get_model()
        itr = combobox.get_active_iter()
        if itr:
            # first column is the name, second column the path and third column
            # a flag indicating if this can be selected
            path = model.get_value(itr, 1)
            if path:
                def on_accept(dialog):
                    self.model.reset_from_file(path)
                DialogFactory.get_confirmation_dialog(
                    "Are you sure?\nYou will loose the current settings!",
                    parent=self.view.get_toplevel()
                ).run(on_accept)
        combobox.set_active(-1) # deselect

    def on_btn_edit_wld_clicked(self, widget, *args):
        self.wld_view.show_all()

    # ------------------------------------------------------------
    #      Notifications of observable properties
    # ------------------------------------------------------------
    @BaseController.observe("has_soller1", assign=True, after=True)
    def notif_has_soller1(self, model, prop_name, info):
        self.update_soller_sensitivity()

    @BaseController.observe("has_soller2", assign=True, after=True)
    def notif_has_soller2(self, model, prop_name, info):
        self.update_soller_sensitivity()
    
    @BaseController.observe("divergence_mode", assign=True, after=True)
    def notif_divergence(self, model, prop_name, info):
        self.update_divergence_label()
        
    @BaseController.observe("has_absorption_correction", assign=True, after=True)
    def notif_absorption(self, model, prop_name, info):
        self.update_absorption_sensitivity()

    pass # end of class

class WavelengthDistributionController(DialogController, TreeViewMixin):
    """
        Wavelength distribution controller.
    """
    
    auto_adapt_included = [ "wavelength_distribution", ]
 
    widget_handlers = {
        'custom':  'custom_handler',
    }

    # ------------------------------------------------------------
    #      Initialization and other internals
    # ------------------------------------------------------------
    @staticmethod
    def custom_handler(self, intel, widget):
        print("CUSTOM HANDLER CALLED FOR %s" % intel.name)
 
    # ------------------------------------------------------------
    #      Initialisation and other internals
    # ------------------------------------------------------------
    def setup_wavelength_distribution_tree_view(self, store, widget):
        """
            Creates the wavelength distribution TreeView layout and behavior
        """      
        setup_treeview(widget, store,
            on_cursor_changed=self.on_wld_tv_cursor_changed,
            sel_mode='MULTIPLE')
        widget.set_model(store)
        
        def data_func(col, cell, model, iter, colnr):
            cell.set_property("text", "%g" % model.get(iter, colnr)[0])
            
        # X Column:
        widget.append_column(new_text_column(
            'Wavelength (nm)', text_col=store.c_x, editable=True,
            data_func = (data_func, (store.c_x,)),
            edited_callback=(self.on_xy_data_cell_edited, (self.model.wavelength_distribution, 0))))
        # Y Column:
        widget.append_column(new_text_column(
            'Fraction', text_col=store.c_y, editable=True,
            data_func = (data_func, (store.c_y,)),
            edited_callback=(self.on_xy_data_cell_edited, (self.model.wavelength_distribution, 1))))   
         
    # ------------------------------------------------------------
    #      GTK Signal handlers
    # ------------------------------------------------------------
    def on_xy_data_cell_edited(self, cell, path, new_text, model, col):
        try:
            value = float(locale.atof(new_text))
        except ValueError:
            logger.exception("ValueError: Invalid literal for float(): '%s'" % new_text)
        else:
            model.set_value(int(path), col, value)
        return True
        
    def on_wld_tv_cursor_changed(self, tv):
        path, col = tv.get_cursor()  # @UnusedVariable
        self.view["btn_del_wavelength_distribution"].set_sensitive(path is not None)
        return True
    
    def on_add_wavelength_distribution_clicked(self, widget):
        self.model.wavelength_distribution.append(0, 0)
        return True
    
    def on_del_wavelength_distribution_clicked(self, widget):
        paths = self.get_selected_paths(self.view["wld_wavelength_distribution"])
        if paths is not None:
            self.model.wavelength_distribution.remove_from_indeces(*paths)
        return True
    
    def on_import_wavelength_distribution_clicked(self, widget, data=None):
        def on_confirm(dialog):
            def on_accept(dialog):
                filename = dialog.filename
                parser = dialog.parser
                message = "An unexpected error has occurred when trying to parse %s:\n\n<i>" % os.path.basename(filename)
                message += "{}</i>\n\n"
                message += "This is most likely caused by an invalid or unsupported file format."

                with DialogFactory.error_dialog_handler(message, parent=self.view.get_toplevel(), reraise=False):
                    self.model.wavelength_distribution.load_data(parser, filename, clear=True)
            DialogFactory.get_load_dialog(
                title="Import wavelength distribution", parent=self.view.get_top_widget(),
                filters=wld_parsers.get_import_file_filters(),
                current_folder=settings.DATA_REG.get_directory_path("DEFAULT_WL_DISTR")
            ).run(on_accept)
        DialogFactory.get_confirmation_dialog(
            "Importing a wavelength distribution will erase all current data.\nAre you sure you want to continue?",
            parent=self.view.get_top_widget()
        ).run(on_confirm)
    
    def on_export_wavelength_distribution_clicked(self, widget, data=None):
        def on_accept(dialog):
            filename = dialog.filename
            parser = dialog.parser
            message = "An unexpected error has occurred when trying to save '%s'.\n" % os.path.basename(filename)
            message += "Contact the developer about this!"
            with DialogFactory.error_dialog_handler(message, parent=self.view.get_toplevel(), reraise=False):
                header = "%s, %s" % ("Wavelength", "Factor")
                self.model.wavelength_distribution.save_data(parser, filename, header=header)
        DialogFactory.get_save_dialog(
            "Select file for wavelength distribution export",
            parent=self.view.get_top_widget(), 
            filters=wld_parsers.get_export_file_filters(),
            current_folder=settings.DATA_REG.get_directory_path("DEFAULT_WL_DISTR")
        ).run(on_accept)
    
    pass # end of class
