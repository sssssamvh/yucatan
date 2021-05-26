################################################################################
# Imports
################################################################################


import pymel.core as pm
from pymel.core.language import Mel as mel


################################################################################
# Yucatan info
################################################################################


yucatan_info = [
    {
        "name": "Delete All Vertex Colours",
        "function": "delete_colours",
        "annotation": "Deletes all vertex colour sets from the scene.",
        "icon": ""
    },
    {
        "name": "Full Cleanup (Modeling)",
        "function": "full_cleanup",
        "annotation": "Performs a full cleanup of the scene.",
        "icon": ""
    },
    {
        "name": "-- Delete History and Namespaces",
        "function": "delete_history_namespaces",
        "annotation": "Removes all history and namespaces.",
        "icon": ""
    },
    {
        "name": "-- Fix All Shader Connections",
        "function": "fix_shaders",
        "annotation": "Fixes multiple, looping or non-existent shader connections. Uses lambert1 if no shader is linked.",
        "icon": ""
    },
    {
        "name": "-- Fix All Shape Names",
        "function": "fix_shape_names",
        "annotation": "Fixes all oddly named shape nodes.",
        "icon": ""
    },
    {
        "name": "-- Fix All Vertex Colours",
        "function": "fix_colours",
        "annotation": "Enables the display colour mode and sets the channel to Diffuse for all meshes in the scene.",
        "icon": ""
    },
    {
        "name": "-- Remove Drawing Overrides",
        "function": "remove_overrides",
        "annotation": "Disables drawing overrides on the shape node.",
        "icon": ""
    },
    {
        "name": "-- Select Unsubdivided",
        "function": "select_unsubdiv",
        "annotation": "Selects shape nodes that are not set to catclark subdivision at rendertime (Arnold).",
        "icon": ""
    }
]


################################################################################
# Tools
################################################################################


def delete_colours(*args):
    """"""
    selection = pm.ls(ni = True, type="mesh")
    for i in selection:
    	pm.select(i)
        try:
            pm.polyColorSet(allColorSets=True, delete=True)
        except:
            pass


def delete_history_namespaces(*args):
    """"""
    # History
    print "Removing all history nodes... ",
    pm.delete(all=True, ch=True)
    print "Done.\n",

    # Namespaces
    print "Removing all namespaces... ",
    defaults = ['UI', 'shared']
    pm.namespace(setNamespace=":")
    all_namespaces = [n for n in pm.namespaceInfo(lon=True, recurse=True) if n not in defaults]
    all_namespaces.reverse()
    for i in all_namespaces:
        pm.namespace(removeNamespace=i, mergeNamespaceWithRoot=True)
    print "Done.\n",


def fix_shaders(*args):
    """"""
    selection = pm.ls(ni = True, type="mesh")
    for i in selection:
        transform = pm.listRelatives(i, type = "transform", parent = True)[0]
        shapeNode = i
        try:
            shadingGroup = pm.listConnections(pm.listHistory(transform, future = True), type = "shadingEngine")[0]
        except:
            shadingGroup = pm.ls("initialShadingGroup")[0]
        pm.disconnectAttr(shapeNode)
        pm.sets(shadingGroup, forceElement = transform)


def fix_shape_names(*args):
    """"""
    selection = pm.ls(ni = True, type="mesh")
    for i in selection:
        transform = pm.listRelatives(i, type = "transform", parent = True)[0]
        shapeNode = i
        shapeName = "{}Shape".format(transform)
        pm.rename(shapeNode, shapeName)


def fix_colours(*args):
    """"""
    selection = pm.ls(ni = True, type="mesh")
    for i in selection:
        pm.polyOptions(i, colorShadedDisplay=True)
        pm.polyOptions(i, colorMaterialChannel="DIFFUSE")
        try:
            pm.setAttr("{}.aiExportColors".format(i), True)
        except:
            pass


def remove_overrides(*args):
    """"""
    selection = pm.selected()
    for i in selection:
        pm.setAttr("{}.ove".format(i), 0)
        m = pm.listRelatives(c = True, s = True, type = "mesh")[0]
        pm.setAttr("{}.ove".format(m), 0)


def select_unsubdiv(*args):
    """Selects all shape nodes that are not set to MtoA catclark subdivision."""
    if not pm.pluginInfo("mtoa.mll", loaded=True, query=True):
        try:
            pm.loadPlugin("mtoa.mll")
        except:
            pm.error("Could not load MtoA.")
    try:
        pm.select(clear=True)
        all_meshes = pm.ls(ni = True, type="mesh")
        count = 0
        for i in all_meshes:
            if pm.getAttr("{}.aiSubdivType".format(i)) == 0 or pm.getAttr("{}.aiSubdivIterations".format(i)) == 0:
                count = count + 1
                t = pm.listRelatives(i, type = "transform", parent = True)[0]
                pm.select(t, add=True)
        print "{} meshes without MtoA subdivision.\n".format(count),
    except:
        pass


def full_cleanup(*args):
    """"""
    delete_history_namespaces()
    fix_shaders()
    fix_shape_names()
    fix_colours()
    remove_overrides()
    unlock_gmod()
    select_unsubdiv()
