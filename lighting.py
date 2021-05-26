################################################################################
# Imports
################################################################################


import pymel.core as pm


################################################################################
# Yucatan info
################################################################################


yucatan_info = [
    {
        "name": "Really Remove Mattes",
        "function": "really_remove_mattes",
        "annotation": "Removes the Arnold matte attribute.",
        "icon": ""
    },
    {
        "name": "Set Arnold Translator to Polymesh",
        "function": "translator_to_polymesh",
        "annotation": "Sets the Arnold translator to Polymesh to allow overrides on Alembic caches.",
        "icon": ""
    }
]


################################################################################
# Tools
################################################################################


def really_remove_mattes(*args):
    """"""
    meshes = pm.listRelatives(ad = True, typ = "mesh")
    for i in meshes:
        pm.editRenderLayerAdjustment("{}.aiMatte".format(i), remove = True)


def translator_to_polymesh(*args):
    """"""
    meshes = pm.listRelatives(ad = True, typ = "mesh")
    for i in meshes:
        pm.setAttr("{}.ai_translator".format(i), "polymesh")
