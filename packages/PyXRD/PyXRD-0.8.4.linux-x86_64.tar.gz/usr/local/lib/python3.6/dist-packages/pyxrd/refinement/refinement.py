# coding=UTF-8
# ex:ts=4:sw=4:et=on

# Copyright (c) 2013, Mathijs Dumon
# All rights reserved.
# Complete license can be found in the LICENSE file.

import logging
logger = logging.getLogger(__name__)

import random

from mvc.models.properties import (
    LabeledProperty, ListProperty, IntegerChoiceProperty, BoolProperty,
    ReadOnlyMixin
)
from mvc.models import TreeNode

from pyxrd.generic.models.event_context_manager import EventContextManager
from pyxrd.generic.models.properties import InheritableMixin
from pyxrd.generic.models import ChildModel

from .refinables.mixins import RefinementValue, RefinementGroup
from .refinables.wrapper import RefinableWrapper
from .refine_method_manager import RefineMethodManager
from .refiner import Refiner

class Refinement(ChildModel):
    """
        A simple model that plugs onto the Mixture model. It provides
        the functionality related to refinement of parameters.
    """

    # MODEL INTEL:
    class Meta(ChildModel.Meta):
        store_id = "Refinement"

    mixture = property(ChildModel.parent.fget, ChildModel.parent.fset)

    #: Flag, True if after refinement plots should be generated of the parameter space
    make_psp_plots = BoolProperty(
        default=False, text="Make parameter space plots",
        tabular=False, visible=True, persistent=True
    )

    #: TreeNode containing the refinable properties
    refinables = ListProperty(
        default=None, text="Refinables",
        tabular=True, persistent=False, visible=True, 
        data_type=RefinableWrapper,
        cast_to=None, widget_type="object_tree_view"
    )

    #: A dict containing an instance of each refinement method
    refine_methods = None


    #: An integer describing which method to use for the refinement
    refine_method_index = IntegerChoiceProperty(
        default=0, text="Refinement method index",
        tabular=True, persistent=True, visible=True,
        choices={ key: method.name for key, method in RefineMethodManager.get_all_methods().items() }
    )

    #: A dict containing the current refinement options
    @LabeledProperty(
        default=None, text="Refine options",
        persistent=False, visible=False,
        mix_with=(ReadOnlyMixin,)
    )
    def refine_options(self):
        return self.get_refinement_method().get_options()
    
    #: A dict containing all refinement options
    @property
    def all_refine_options(self):
        return {
            method.index : method.get_options()
            for method in list(self.refine_methods.values())
        }

    def __init__(self, *args, **kwargs):
        my_kwargs = self.pop_kwargs(kwargs,
            "refine_method_index", "refine_method", "refine_options"
        )
        super(Refinement, self).__init__(*args, **kwargs)
        kwargs = my_kwargs

        # Setup the refinables treestore
        self.refinables = TreeNode()
        self.update_refinement_treestore()

        # Setup the refine methods
        try:
            self.refine_method_index = int(self.get_kwarg(kwargs, None, "refine_method_index", "refine_method"))
        except ValueError:
            self.refine_method_index = self.refine_method_index
            pass # ignore faulty values, these indices change from time to time.

        self.refine_methods = RefineMethodManager.initialize_methods(
            self.get_kwarg(kwargs, None, "refine_options")
        )

    # ------------------------------------------------------------
    #      Refiner methods
    # ------------------------------------------------------------
    def get_refiner(self):
        """
            This returns a Refiner object which can be used to refine the
            selected properties using the selected algorithm.
            Just call 'refine(stop)' on the returned object, with stop a
            threading.Event or multiprocessing.Event which you can use to stop
            the refinement before completion.
            The Refiner object also has a RefineHistory and RefineStatus object
            that can be used to track the status and history of the refinement.
        """ 
       
        return Refiner(
            method            = self.get_refinement_method(),
            data_callback     = lambda: self.mixture.data_object,
            refinables        = self.refinables,
            event_cmgr        = EventContextManager(self.mixture.needs_update, self.mixture.data_changed),
            metadata          = dict(
                phases          = self.mixture.phases,
                num_specimens   = len(self.mixture.specimens),
            )
        )

    # ------------------------------------------------------------
    #      Refinement Methods Management
    # ------------------------------------------------------------
    def get_refinement_method(self):
        """
            Returns the actual refinement method by translating the 
            `refine_method` attribute
        """
        return self.refine_methods[self.refine_method_index]

    # ------------------------------------------------------------
    #      Refinables Management
    # ------------------------------------------------------------
    # TODO set a restrict range attribute on the PropIntels, so we can use custom ranges for each property
    def auto_restrict(self):
        """
            Convenience function that restricts the selected properties 
            automatically by setting their minimum and maximum values.
        """
        with self.mixture.needs_update.hold():
            for node in self.refinables.iter_children():
                ref_prop = node.object
                if ref_prop.refine and ref_prop.refinable:
                    ref_prop.value_min = ref_prop.value * 0.8
                    ref_prop.value_max = ref_prop.value * 1.2

    def randomize(self):
        """
            Convenience function that randomize the selected properties.
            Respects the current minimum and maximum values.
            Executes an optimization after the randomization.
        """
        with self.mixture.data_changed.hold_and_emit():
            with self.mixture.needs_update.hold_and_emit():
                for node in self.refinables.iter_children():
                    ref_prop = node.object
                    if ref_prop.refine and ref_prop.refinable:
                        ref_prop.value = random.uniform(ref_prop.value_min, ref_prop.value_max)

    def update_refinement_treestore(self):
        """
            This creates a tree store with all refinable properties and their
            minimum, maximum and current value.
        """
        if self.parent is not None: # not linked so no valid phases!
            self.refinables.clear()

            def add_property(parent_node, obj, prop, is_grouper):
                rp = RefinableWrapper(obj=obj, prop=prop, parent=self.mixture, is_grouper=is_grouper)
                return parent_node.append(TreeNode(rp))

            def parse_attribute(obj, prop, root_node):
                """
                    obj: the object
                    attr: the attribute of obj or None if obj contains attributes
                    root_node: the root TreeNode new iters should be put under
                """
                if prop is not None:
                    if isinstance(prop, InheritableMixin):
                        value = prop.get_uninherited(obj)
                    else:
                        value = getattr(obj, prop.label)
                else:
                    value = obj

                if isinstance(value, RefinementValue): # AtomRelation and UnitCellProperty
                    new_node = add_property(root_node, value, prop, False)
                elif hasattr(value, "__iter__"): # List or similar
                    for new_obj in value:
                        parse_attribute(new_obj, None, root_node)
                elif isinstance(value, RefinementGroup): # Phase, Component, Probability
                    if len(value.refinables) > 0:
                        new_node = add_property(root_node, value, prop, True)
                        for prop in value.refinables:
                            parse_attribute(value, prop, new_node)
                else: # regular values
                    new_node = add_property(root_node, obj, prop, False)

            for phase in self.mixture.project.phases:
                if phase in self.mixture.phase_matrix:
                    parse_attribute(phase, None, self.refinables)


    pass # end of class
