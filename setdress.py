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
        "name": "Batch Align",
        "function": "batch_align",
        "annotation": "Batch aligns the first half of the selection to the center points of the second half.",
        "icon": ""
    },
    {
        "name": "Generate Placeholders",
        "function": "generate_placeholders",
        "annotation": "Creates placeholder locators at the selection's geometry centers or pivot points. Useful for setdress.",
        "icon": ""
    },
    {
        "name": "Instance Shape For n Transforms",
        "function": "instance_for_transforms",
        "annotation": "Instances the first selected mesh for as many other selected transforms.",
        "icon": ""
    },
    {
        "name": "Randomise Transforms...",
        "function": "randomise_transforms",
        "annotation": "Randomise rotation and scale with a variety of options.",
        "icon": ""
    },
    {
        "name": "Swap Location",
        "function": "swap_location",
        "annotation": "Swaps two transforms' places.",
        "icon": ""
    },
    {
        "name": "Transfer Transforms",
        "function": "transfer_transforms",
        "annotation": "Transfers the transformation values of the selection's first half to the second.",
        "icon": ""
    }
]


################################################################################
# Tools
################################################################################


def batch_align(*args):
    """"""
    selection = pm.selected()
    count = len(selection) // 2
    originals = selection[count:] # second half of selection
    new = selection[:count] # first half of selection
    for i in xrange(0, count):
        # first select each pair of objects
        o = originals[i]
        n = new[i]
        pm.select([n, o], replace = True)
        # unlock transforms
        pm.setAttr("{}.tx".format(n), lock = False)
        pm.setAttr("{}.ty".format(n), lock = False)
        pm.setAttr("{}.tz".format(n), lock = False)
        pm.setAttr("{}.rx".format(n), lock = False)
        pm.setAttr("{}.ry".format(n), lock = False)
        pm.setAttr("{}.rz".format(n), lock = False)
        pm.setAttr("{}.sx".format(n), lock = False)
        pm.setAttr("{}.sy".format(n), lock = False)
        pm.setAttr("{}.sz".format(n), lock = False)
        # perform the alignment
        try:
            pm.align(x = "mid", y = "mid", z = "mid", atl = True)
        except:
            pass
    pm.select(selection)


def generate_placeholders(*args):
    """"""
    translate_base = pm.confirmDialog(title="Generate Locators", message="Match pivot or geometry center?", button=["Pivot", "Geometry Center"], defaultButton="Pivot", dismissString="Cancel")
    selection = pm.selected()
    for each in selection:
        group_name = "{}_locators".format(str(each).split(":")[-1].split("_")[0])
        if not pm.objExists(group_name):
            pm.group(em = True, name = group_name)
        locatr = pm.spaceLocator(a = True, p = (0,0,0))
        if translate_base == "Pivot":
            pos = pm.xform(each, piv = True, ws = True, q = True)
        else:
            pos = each.getBoundingBox(space="world").center()
        rot = each.getRotation()
        scl = each.getScale()
        locatr.setTranslation((pos[0], pos[1], pos[2]), space="world")
        locatr.setRotation((rot[0], rot[1], rot[2]), space="world")
        locatr.setScale((scl[0], scl[1], scl[2]))
        pm.parent(locatr, group_name)


def instance_for_transforms(*args):
    """"""
    transforms_reference_point = pm.confirmDialog(title="Instance Shape for n Transforms", message="Match transforms' pivots or world space coordinates?", button=["Pivots", "Coordinates"], defaultButton="Pivots", dismissString="Cancel")
    selection = pm.selected()
    shape = pm.listRelatives(selection[0], children = True, shapes = True)
    transforms = selection[1:]

    for t in transforms:
        d = pm.duplicate(shape, rr = True, instanceLeaf = True)[0]

        if transforms_reference_point == "Pivots":
            pos = pm.xform(t, piv = True, ws = True, q = True)
        else:
            pos = t.getTranslation(space = "world")
        # Regardless of the points to move it to, the instance should always be grabbed by its pivot (rpr = True)
        pm.move(d, (pos[0], pos[1], pos[2]), rpr = True, ws = True)
        d.setRotation(t.getRotation(space="world"), space="world")
        d.setScale(t.getScale())
        pm.delete(t)


def randomise_transforms(*args):
    """"""
    RandomiseTransforms()


def swap_location(*args):
    """"""
    selection = pm.selected()
    if len(selection) != 2:
        pm.error("Please only select two transforms.")
    else:
        location_a = selection[0].getTranslation(space="world")
        location_b = selection[1].getTranslation(space="world")
        selection[0].setTranslation(location_b)
        selection[1].setTranslation(location_a)


def transfer_transforms(*args):
    """"""
    selection = pm.selected()
    count = len(selection)
    originals = selection[:count/2]
    new = selection[count/2:]
    for i in xrange(0, count/2):
        o = originals[i]
        n = new[i]
        n.setTranslation(o.getTranslation(space="world"), space="world")
        n.setRotation(o.getRotation(space="world"), space="world")
        n.setScale(o.getScale())


################################################################################
# Classes
################################################################################


class RandomiseTransforms(object):
    """Randomly scales and/or rotates selection, with settings."""


    def __init__(self):
        """Draws the user interface"""
        super(RandomiseTransforms, self).__init__()

        if pm.dockControl("RandomiseTransforms", exists=True):
            pm.deleteUI("RandomiseTransforms")

        # Window, layout and dockControl

        win_rnd = pm.window()
        col_rnd = pm.columnLayout(
            width=250,
            columnWidth=250,
            columnAttach = ('both', 0),
            # rowSpacing = 30,
            parent = win_rnd)
        pm.dockControl("RandomiseTransforms", area='left', content=win_rnd, allowedArea=['left', 'right'], label="Randomise Transforms", width=250, sizeable=False)

        # Buttons

        frm_btn = pm.frameLayout(cll=True, cl=False, fn='boldLabelFont', parent=col_rnd, width=200, l="Randomise Transforms")
        col_btn = pm.columnLayout(
            width = 250,
            parent = frm_btn)
        self.chk_pos = pm.checkBox(label = "Randomise Position", parent = col_btn, value = True, changeCommand = self.ui_toggle_pos)
        self.chk_rot = pm.checkBox(label = "Randomise Rotation", parent = col_btn, value = True, changeCommand = self.ui_toggle_rot)
        self.chk_scl = pm.checkBox(label = "Randomise Scale", parent = col_btn, value = True, changeCommand = self.ui_toggle_scl)
        pm.button(label = "Go", parent = col_btn, command = self.execute)
        pm.button(label = "Freeze Transforms", parent = col_btn, command = "pm.makeIdentity(apply = True, t = True, r = True, s = True)")

        # Randomise Position

        frm_pos = pm.frameLayout(cll=True, cl=True, fn='boldLabelFont', parent=col_rnd, width=200, l="Position")
        col_pos = pm.columnLayout(
            columnAttach = ('both', 0),
            width = 250,
            columnWidth = 250,
            rowSpacing = 10,
            parent = frm_pos)
        self.chk_pos_worldspace = pm.checkBox(label = "World Space", parent = col_pos, value = False)
        self.chk_pos_relative = pm.checkBox(label = "Relative to Current", parent = col_pos, value = False)
        row_pos_x = pm.rowLayout(
            numberOfColumns = 5,
            columnWidth5 = [40, 40, 60, 40, 60],
            parent = col_pos)
        self.chk_pos_x = pm.checkBox(label = "X", parent = row_pos_x, value = True, changeCommand = self.ui_toggle_pos_x)
        pm.text(label="Min:", align='right')
        self.fld_pos_x_min = pm.floatField(value = -5, parent = row_pos_x, precision = 3)
        pm.text(label="Max:", align='right')
        self.fld_pos_x_max = pm.floatField(value = 5, parent = row_pos_x, precision = 3)
        row_pos_y = pm.rowLayout(
            numberOfColumns = 5,
            columnWidth5 = [40, 40, 60, 40, 60],
            parent = col_pos)
        self.chk_pos_y = pm.checkBox(label = "Y", parent = row_pos_y, value = True, changeCommand = self.ui_toggle_pos_y)
        pm.text(label="Min:", align='right')
        self.fld_pos_y_min = pm.floatField(value = -5, parent = row_pos_y, precision = 3)
        pm.text(label="Max:", align='right')
        self.fld_pos_y_max = pm.floatField(value = 5, parent = row_pos_y, precision = 3)
        row_pos_z = pm.rowLayout(
            numberOfColumns = 5,
            columnWidth5 = [40, 40, 60, 40, 60],
            parent = col_pos)
        self.chk_pos_z = pm.checkBox(label = "Z", parent = row_pos_z, value = True, changeCommand = self.ui_toggle_pos_z)
        pm.text(label="Min:", align='right')
        self.fld_pos_z_min = pm.floatField(value = -5, parent = row_pos_z, precision = 3)
        pm.text(label="Max:", align='right')
        self.fld_pos_z_max = pm.floatField(value = 5, parent = row_pos_z, precision = 3)

        # Randomise Rotation

        frm_rot = pm.frameLayout(cll=True, cl=True, fn='boldLabelFont', parent=col_rnd, width=200, l="Rotation")
        col_rot = pm.columnLayout(
            columnAttach = ('both', 0),
            width = 250,
            columnWidth = 250,
            rowSpacing = 10,
            parent = frm_rot)
        self.chk_rot_stepped = pm.checkBox(label = "90-degree Steps", parent = col_rot, value = False, changeCommand = self.ui_toggle_rot_stepped)
        self.chk_rot_relative = pm.checkBox(label = "Relative to Current", parent = col_rot, value = False)
        row_rot_x = pm.rowLayout(
            numberOfColumns = 5,
            columnWidth5 = [40, 40, 60, 40, 60],
            parent = col_rot)
        self.chk_rot_x = pm.checkBox(label = "X", parent = row_rot_x, value = True, changeCommand = self.ui_toggle_rot_x)
        pm.text("Min:")
        self.fld_rot_x_min = pm.floatField(value = -5, minValue = -360, maxValue = 360, parent = row_rot_x, precision = 3)
        pm.text("Max:")
        self.fld_rot_x_max = pm.floatField(value = 5, minValue = -360, maxValue = 360, parent = row_rot_x, precision = 3)
        row_rot_y = pm.rowLayout(
            numberOfColumns = 5,
            columnWidth5 = [40, 40, 60, 40, 60],
            parent = col_rot)
        self.chk_rot_y = pm.checkBox(label = "Y", parent = row_rot_y, value = True, changeCommand = self.ui_toggle_rot_y)
        pm.text("Min:")
        self.fld_rot_y_min = pm.floatField(value = 0, minValue = -360, maxValue = 360, parent = row_rot_y, precision = 3)
        pm.text("Max:")
        self.fld_rot_y_max = pm.floatField(value = 360, minValue = -360, maxValue = 360, parent = row_rot_y, precision = 3)
        row_rot_z = pm.rowLayout(
            numberOfColumns = 5,
            columnWidth5 = [40, 40, 60, 40, 60],
            parent = col_rot)
        self.chk_rot_z = pm.checkBox(label = "Z", parent = row_rot_z, value = True, changeCommand = self.ui_toggle_rot_z)
        pm.text("Min:")
        self.fld_rot_z_min = pm.floatField(value = -5, minValue = -360, maxValue = 360, parent = row_rot_z, precision = 3)
        pm.text("Max:")
        self.fld_rot_z_max = pm.floatField(value = 5, minValue = -360, maxValue = 360, parent = row_rot_z, precision = 3)

        # Randomise Scale

        frm_scl = pm.frameLayout(cll=True, cl=True, fn='boldLabelFont', parent=col_rnd, width=200, l="Scale")
        col_scl = pm.columnLayout(
            columnAttach = ('both', 0),
            width = 250,
            columnWidth = 250,
            rowSpacing = 10,
            parent = frm_scl)
        self.chk_scl_uniform = pm.checkBox(label = "Uniform XYZ", parent = col_scl, value = True, changeCommand = self.ui_toggle_scl_uniform)
        self.chk_scl_relative = pm.checkBox(label = "Relative to Current", parent = col_scl, value = False)
        row_scl_x = pm.rowLayout(
            numberOfColumns = 5,
            columnWidth5 = [40, 40, 60, 40, 60],
            parent = col_scl)
        self.chk_scl_x = pm.checkBox(label = "X", parent = row_scl_x, value = True, changeCommand = self.ui_toggle_scl_x, enable = False)
        pm.text("Min:")
        self.fld_scl_x_min = pm.floatField(value = 0.5, parent = row_scl_x, precision = 3)
        pm.text("Max:")
        self.fld_scl_x_max = pm.floatField(value = 1.5, parent = row_scl_x, precision = 3)
        row_scl_y = pm.rowLayout(
            numberOfColumns = 5,
            columnWidth5 = [40, 40, 60, 40, 60],
            parent = col_scl)
        self.chk_scl_y = pm.checkBox(label = "Y", parent = row_scl_y, value = False, changeCommand = self.ui_toggle_scl_y, enable = False)
        pm.text("Min:")
        self.fld_scl_y_min = pm.floatField(value = 0.5, parent = row_scl_y, precision = 3, enable = False)
        pm.text("Max:")
        self.fld_scl_y_max = pm.floatField(value = 1.5, parent = row_scl_y, precision = 3, enable = False)
        row_scl_z = pm.rowLayout(
            numberOfColumns = 5,
            columnWidth5 = [40, 40, 60, 40, 60],
            parent = col_scl)
        self.chk_scl_z = pm.checkBox(label = "Z", parent = row_scl_z, value = False, changeCommand = self.ui_toggle_scl_z, enable = False)
        pm.text("Min:")
        self.fld_scl_z_min = pm.floatField(value = 0.5, parent = row_scl_z, precision = 3, enable = False)
        pm.text("Max:")
        self.fld_scl_z_max = pm.floatField(value = 1.5, parent = row_scl_z, precision = 3, enable = False)


    def execute(self, *args):
        """Executes the command"""
        pos_x, pos_y, pos_z = 0, 0, 0
        rot_x, rot_y, rot_z = 0, 0, 0
        scl_x, scl_y, scl_z = 0, 0, 0
        selection = pm.selected()
        for i in selection:
            if self.chk_pos.getValue(): # Position
                pos_x = r.uniform(self.fld_pos_x_min.getValue(), self.fld_pos_x_max.getValue())
                pos_y = r.uniform(self.fld_pos_y_min.getValue(), self.fld_pos_y_max.getValue())
                pos_z = r.uniform(self.fld_pos_z_min.getValue(), self.fld_pos_z_max.getValue())
                print str(pos_x) + " - " + str(pos_y) + " - " + str(pos_z)
                world_space = self.chk_pos_worldspace.getValue()
                relative = self.chk_pos_relative.getValue()
                if self.chk_pos_x.getValue() and self.chk_pos_y.getValue() and self.chk_pos_z.getValue(): # xyz
                    pm.move(i, [pos_x, pos_y, pos_z], moveXYZ = True, ws = world_space, os = not world_space, wd = True, relative = relative)
                elif self.chk_pos_x.getValue() and self.chk_pos_y.getValue(): # xy
                    pm.move(i, [pos_x, pos_y], moveXY = True, ws = world_space, os = not world_space, wd = True, relative = relative)
                elif self.chk_pos_x.getValue() and self.chk_pos_z.getValue(): # xz
                    pm.move(i, [pos_x, pos_z], moveXZ = True, ws = world_space, os = not world_space, wd = True, relative = relative)
                elif self.chk_pos_y.getValue() and self.chk_pos_z.getValue(): # yz
                    pm.move(i, [pos_y, pos_z], moveYZ = True, ws = world_space, os = not world_space, wd = True, relative = relative)
                elif self.chk_pos_x.getValue(): # x
                    pm.move(i, [pos_x], moveX = True, ws = world_space, os = not world_space, wd = True, relative = relative)
                elif self.chk_pos_y.getValue(): # y
                    pm.move(i, [pos_y], moveY = True, ws = world_space, os = not world_space, wd = True, relative = relative)
                elif self.chk_pos_z.getValue(): # z
                    pm.move(i, [pos_z], moveZ = True, ws = world_space, os = not world_space, wd = True, relative = relative)
            if self.chk_rot.getValue(): # Rotation
                if self.chk_rot_stepped.getValue():
                    x_rand = r.uniform(0, 1)
                    y_rand = r.uniform(0, 1)
                    z_rand = r.uniform(0, 1)
                    if x_rand >= 0.25:    rot_x = 90
                    if x_rand >= 0.5:     rot_x = 180
                    if x_rand >= 0.75:    rot_x = 270
                    if y_rand >= 0.25:    rot_y = 90
                    if y_rand >= 0.5:     rot_y = 180
                    if y_rand >= 0.75:    rot_y = 270
                    if z_rand >= 0.25:    rot_z = 90
                    if z_rand >= 0.5:     rot_z = 180
                    if z_rand >= 0.75:    rot_z = 270
                else:
                    rot_x = r.uniform(self.fld_rot_x_min.getValue(), self.fld_rot_x_max.getValue())
                    rot_y = r.uniform(self.fld_rot_y_min.getValue(), self.fld_rot_y_max.getValue())
                    rot_z = r.uniform(self.fld_rot_z_min.getValue(), self.fld_rot_z_max.getValue())
                relative = self.chk_rot_relative.getValue()
                if self.chk_rot_x.getValue() and self.chk_rot_y.getValue() and self.chk_rot_z.getValue(): # xyz
                    pm.rotate(i, [rot_x, rot_y, rot_z], os = True, rotateXYZ = True, relative = relative)
                elif self.chk_rot_x.getValue() and self.chk_rot_y.getValue(): # xy
                    pm.rotate(i, [rot_x, rot_y], os = True, rotateXY = True, relative = relative)
                elif self.chk_rot_x.getValue() and self.chk_rot_z.getValue(): # xz
                    pm.rotate(i, [rot_x, rot_z], os = True, rotateXZ = True, relative = relative)
                elif self.chk_rot_y.getValue() and self.chk_rot_z.getValue(): # yz
                    pm.rotate(i, [rot_y, rot_z], os = True, rotateYZ = True, relative = relative)
                elif self.chk_rot_x.getValue(): # x
                    pm.rotate(i, [rot_x], os = True, rotateX = True, relative = relative)
                elif self.chk_rot_y.getValue(): # y
                    pm.rotate(i, [rot_y], os = True, rotateY = True, relative = relative)
                elif self.chk_rot_z.getValue(): # z
                    pm.rotate(i, [rot_z], os = True, rotateZ = True, relative = relative)
            if self.chk_scl.getValue(): # Scale
                scl_x = r.uniform(self.fld_scl_x_min.getValue(), self.fld_scl_x_max.getValue())
                scl_y = r.uniform(self.fld_scl_y_min.getValue(), self.fld_scl_y_max.getValue())
                scl_z = r.uniform(self.fld_scl_z_min.getValue(), self.fld_scl_z_max.getValue())
                relative = self.chk_scl_relative.getValue()
                if self.chk_scl_uniform.getValue():
                    pm.scale(i, [scl_x, scl_x, scl_x], scaleXYZ = True, relative = relative)
                elif self.chk_scl_x.getValue() and self.chk_scl_y.getValue() and self.chk_scl_z.getValue(): #xyz
                    pm.scale(i, [scl_x, scl_y, scl_z], scaleXYZ = True, relative = relative)
                elif self.chk_scl_x.getValue() and self.chk_scl_y.getValue(): #xy
                    pm.scale(i, [scl_x, scl_y], scaleXY = True, relative = relative)
                elif self.chk_scl_x.getValue() and self.chk_scl_z.getValue(): #xz
                    pm.scale(i, [scl_x, scl_z], scaleXZ = True, relative = relative)
                elif self.chk_scl_y.getValue() and self.chk_scl_z.getValue(): #yz
                    pm.scale(i, [scl_y, scl_z], scaleYZ = True, relative = relative)
                elif self.chk_scl_x.getValue(): #x
                    pm.scale(i, [scl_x], scaleX = True, relative = relative)
                elif self.chk_scl_y.getValue(): #y
                    pm.scale(i, [scl_y], scaleY = True, relative = relative)
                elif self.chk_scl_z.getValue(): #z
                    pm.scale(i, [scl_z], scaleZ = True, relative = relative)


    def ui_toggle_pos(self, value):
        """Enables or disables the randomise position UI"""
        self.chk_pos_worldspace.setEnable(val = value)
        self.chk_pos_x.setEnable(val = value)
        self.chk_pos_y.setEnable(val = value)
        self.chk_pos_z.setEnable(val = value)
        self.chk_pos_relative.setEnable(val = value)
        self.fld_pos_x_min.setEnable(val = value)
        self.fld_pos_x_max.setEnable(val = value)
        self.fld_pos_y_min.setEnable(val = value)
        self.fld_pos_y_max.setEnable(val = value)
        self.fld_pos_z_min.setEnable(val = value)
        self.fld_pos_z_max.setEnable(val = value)


    def ui_toggle_rot(self, value):
        """Enables or disables the randomise rotation UI"""
        self.chk_rot_stepped.setEnable(val = value)
        self.chk_rot_x.setEnable(val = value)
        self.chk_rot_y.setEnable(val = value)
        self.chk_rot_z.setEnable(val = value)
        self.chk_rot_relative.setEnable(val = value)
        self.fld_rot_x_min.setEnable(val = value)
        self.fld_rot_x_max.setEnable(val = value)
        self.fld_rot_y_min.setEnable(val = value)
        self.fld_rot_y_max.setEnable(val = value)
        self.fld_rot_z_min.setEnable(val = value)
        self.fld_rot_z_max.setEnable(val = value)


    def ui_toggle_rot_stepped(self, value):
        """Enables or disables the randomise stepped rotation UI"""
        self.fld_rot_x_min.setEnable(val = not value)
        self.fld_rot_x_max.setEnable(val = not value)
        self.fld_rot_y_min.setEnable(val = not value)
        self.fld_rot_y_max.setEnable(val = not value)
        self.fld_rot_z_min.setEnable(val = not value)
        self.fld_rot_z_max.setEnable(val = not value)


    def ui_toggle_pos_x(self, value):
        """"""
        self.fld_pos_x_min.setEnable(val = value)
        self.fld_pos_x_max.setEnable(val = value)


    def ui_toggle_pos_y(self, value):
        """"""
        self.fld_pos_y_min.setEnable(val = value)
        self.fld_pos_y_max.setEnable(val = value)


    def ui_toggle_pos_z(self, value):
        """"""
        self.fld_pos_z_min.setEnable(val = value)
        self.fld_pos_z_max.setEnable(val = value)


    def ui_toggle_rot_x(self, value):
        """"""
        if not self.chk_rot_stepped.getValue():
            self.fld_rot_x_min.setEnable(val = value)
            self.fld_rot_x_max.setEnable(val = value)


    def ui_toggle_rot_y(self, value):
        """"""
        if not self.chk_rot_stepped.getValue():
            self.fld_rot_y_min.setEnable(val = value)
            self.fld_rot_y_max.setEnable(val = value)


    def ui_toggle_rot_z(self, value):
        """"""
        if not self.chk_rot_stepped.getValue():
            self.fld_rot_z_min.setEnable(val = value)
            self.fld_rot_z_max.setEnable(val = value)


    def ui_toggle_scl_x(self, value):
        """"""
        self.fld_scl_x_min.setEnable(val = value)
        self.fld_scl_x_max.setEnable(val = value)


    def ui_toggle_scl_y(self, value):
        """"""
        self.fld_scl_y_min.setEnable(val = value)
        self.fld_scl_y_max.setEnable(val = value)


    def ui_toggle_scl_z(self, value):
        """"""
        self.fld_scl_z_min.setEnable(val = value)
        self.fld_scl_z_max.setEnable(val = value)


    def ui_toggle_scl(self, value):
        """Enables or disables the randomise scale UI"""
        # Toggle uniform and its value
        self.chk_scl_uniform.setEnable(val = value)
        self.chk_scl_uniform.setValue(val = value)
        self.chk_scl_relative.setEnable(val = value)
        # Toggle XYZ and their values
        self.chk_scl_x.setEnable(val = False)
        self.chk_scl_y.setEnable(val = False)
        self.chk_scl_z.setEnable(val = False)
        self.chk_scl_x.setValue(val = True)
        self.chk_scl_y.setValue(val = False)
        self.chk_scl_z.setValue(val = False)
        # Toggle XYZ min and max fields
        self.fld_scl_x_min.setEnable(val = value)
        self.fld_scl_x_max.setEnable(val = value)
        self.fld_scl_y_min.setEnable(val = False)
        self.fld_scl_y_max.setEnable(val = False)
        self.fld_scl_z_min.setEnable(val = False)
        self.fld_scl_z_max.setEnable(val = False)


    def ui_toggle_scl_uniform(self, value):
        """Enables or disables uniform scaling"""
        # Toggle XYZ and their values
        self.chk_scl_x.setEnable(val = not value)
        self.chk_scl_y.setEnable(val = not value)
        self.chk_scl_z.setEnable(val = not value)
        self.chk_scl_x.setValue(val = True)
        self.chk_scl_y.setValue(val = not value)
        self.chk_scl_z.setValue(val = not value)
        # Toggle XYZ min and max fields
        self.fld_scl_x_min.setEnable(val = True)
        self.fld_scl_x_max.setEnable(val = True)
        self.fld_scl_y_min.setEnable(val = not value)
        self.fld_scl_y_max.setEnable(val = not value)
        self.fld_scl_z_min.setEnable(val = not value)
        self.fld_scl_z_max.setEnable(val = not value)
