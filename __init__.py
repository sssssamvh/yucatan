##############################################################################
# Imports
##############################################################################


if "cleanup" in locals():
    reload(cleanup)
    reload(lighting)
    reload(modeling)
    reload(setdress)
    reload(utilities)
    print("[Yucatan] Reloaded package modules\n"),

else:
    from . import cleanup, lighting, modeling, setdress, utilities
    print("[Yucatan] Reloaded package modules\n"),

import pymel.core as pm


##############################################################################
# Menu
##############################################################################


def main():

    main_window = pm.MelGlobals()["gMainWindow"]
    if pm.menu("yucatan_menu", exists=True):
        yucatan_menu = pm.menu("yucatan_menu", edit=True, deleteAllItems=True)
    else:
        yucatan_menu = pm.menu("yucatan_menu", label="Yucatan", parent=main_window, tearOff=True)
    pm.menuItem(divider=True, dividerLabel="Update", parent=yucatan_menu)
    pm.menuItem(label="Reload Yucatan", parent=yucatan_menu, command="reload(yucatan)", annotation="Reloads the toolbox.")

    modules = [cleanup, lighting, modeling, setdress, utilities]
    for m in modules:
        module_name = m.__name__.split(".")[1]
        items = m.yucatan_info
        pm.menuItem(divider=True, dividerLabel=module_name.capitalize(), parent=yucatan_menu)
        for i in items:
            if "submenu" in i.keys():
                submenu = pm.menuItem(label=i["submenu"], parent=yucatan_menu, subMenu = True)
                for t in i["tools"]:
                    command = getattr(m, t["function"])
                    print("[Yucatan] Found tool {}.{}\n".format(module_name, t["function"])),
                    pm.menuItem(label=t["name"], command=command, annotation=t["annotation"], image=t["icon"])
            else:
                command = getattr(m, i["function"])
                print("[Yucatan] Found tool {}.{}\n".format(module_name, i["function"])),
                pm.menuItem(label=i["name"], parent=yucatan_menu, command=command, annotation=i["annotation"], image=i["icon"])
    print("[Yucatan] Ready.\n"),


main()
