################################################################################
# Imports
################################################################################


import pymel.core as pm
import random as r


################################################################################
# Yucatan info
################################################################################


yucatan_info = [
    {
        "name": "Flatten Hierarchy",
        "function": "flatten_hierarchy",
        "annotation": "Ungroups everything.",
        "icon": ""
    },
    {
        "name": "Group By Topology",
        "function": "group_by_topology",
        "annotation": "",
        "icon": ""
    },
    {
        "name": "Reset Subdivision (Arnold)",
        "function": "reset_subdiv_arnold",
        "annotation": "",
        "icon": ""
    },
    {
        "name": "Reset Subdivision (RenderMan)",
        "function": "reset_subdiv_renderman",
        "annotation": "",
        "icon": ""
    },
    {
        "name": "Sort Alphabetically",
        "function": "sort_alphabet",
        "annotation": "",
        "icon": ""
    },
    {
        "name": "Sort Randomly",
        "function": "sort_random",
        "annotation": "Scrambles the selection's order in the Outliner. Useful in conjunction with Batch Align.",
        "icon": ""
    },
    {
        "name": "Unlock Transforms",
        "function": "unlock_transforms",
        "annotation": "Unlocks the selection's transforms.",
        "icon": ""
    }
]


################################################################################
# Tools
################################################################################


def flatten_hierarchy(*args):
    """"""
    transforms = pm.ls(type='transform')
    for t in transforms:
        pm.setAttr("{}.tx".format(t), lock = False)
        pm.setAttr("{}.ty".format(t), lock = False)
        pm.setAttr("{}.tz".format(t), lock = False)
        pm.setAttr("{}.rx".format(t), lock = False)
        pm.setAttr("{}.ry".format(t), lock = False)
        pm.setAttr("{}.rz".format(t), lock = False)
        pm.setAttr("{}.sx".format(t), lock = False)
        pm.setAttr("{}.sy".format(t), lock = False)
        pm.setAttr("{}.sz".format(t), lock = False)
        pm.setAttr("{}.translate".format(t), lock = False)
        pm.setAttr("{}.rotate".format(t), lock = False)
        pm.setAttr("{}.scale".format(t), lock = False)
        pm.parent(t, w=True)

    # Delete empty groups
    transforms = pm.ls(type='transform')
    for t in transforms:
        children = pm.listRelatives(t, c=True)
        if children == None:
            pm.delete(t)


def group_by_topology(*args):
    """"""
    pass


def reset_subdiv_arnold(*args):
    """"""
    pass


def reset_subdiv_renderman(*args):
    """"""
    pass


def sort_alphabet(*args):
    """"""
    selection = sorted(pm.selected())
    for i in selection:
        pm.reorder(i, back = True)


def sort_random(*args):
    """"""
    selection = pm.selected()
    r.shuffle(selection)
    for i in selection:
        pm.reorder(i, back = True)


def unlock_transforms(*args):
    """"""
    selection = pm.selected()
    for i in selection:
        if pm.objectType(i) == "transform":
            pm.setAttr("{}.tx".format(i), lock = False)
            pm.setAttr("{}.ty".format(i), lock = False)
            pm.setAttr("{}.tz".format(i), lock = False)
            pm.setAttr("{}.rx".format(i), lock = False)
            pm.setAttr("{}.ry".format(i), lock = False)
            pm.setAttr("{}.rz".format(i), lock = False)
            pm.setAttr("{}.sx".format(i), lock = False)
            pm.setAttr("{}.sy".format(i), lock = False)
            pm.setAttr("{}.sz".format(i), lock = False)
            pm.setAttr("{}.translate".format(i), lock = False)
            pm.setAttr("{}.rotate".format(i), lock = False)
            pm.setAttr("{}.scale".format(i), lock = False)
