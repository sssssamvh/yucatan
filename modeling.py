################################################################################
# Imports
################################################################################


import pymel.core as pm
import pymel.core.datatypes as dt
import math


################################################################################
# Yucatan info
################################################################################


yucatan_info = [
    {
        "name": "Flatten Along X",
        "function": "flatten_x",
        "annotation": "Squeezes the selection along the X axis.",
        "icon": ""
    },
    {
        "name": "Flatten Along Y",
        "function": "flatten_y",
        "annotation": "Squeezes the selection along the Y axis.",
        "icon": ""
    },
    {
        "name": "Flatten Along Z",
        "function": "flatten_z",
        "annotation": "Squeezes the selection along the Z axis.",
        "icon": ""
    },
    {
        "name": "Instance Along Curve",
        "function": "instance_along_curve",
        "annotation": "",
        "icon": ""
    },
    {
        "name": "Mirror Instance",
        "function": "mirror_instance",
        "annotation": "",
        "icon": ""
    },
    {
        "name": "Mirror Shell",
        "function": "mirror_shell",
        "annotation": "",
        "icon": ""
    },
    {
        "name": "Rail Relax",
        "function": "rail_relax",
        "annotation": "Evenly spreads the selected edges along their enclosing edge loops. Original MEL version by Wim Coene.",
        "icon": ""
    },
    {
        "submenu": "Select Anomalies",
        "tools": [
            {
                "name": "N-gons",
                "function": "select_ngons",
                "annotation": "",
                "icon": ""
            },
            {
                "name": "Six-poles",
                "function": "select_sixpoles",
                "annotation": "",
                "icon": ""
            },
            {
                "name": "Triangles",
                "function": "select_triangles",
                "annotation": "",
                "icon": ""
            }
        ]
    },
    {
        "name": "Snap Vertices to Surface",
        "function": "snap_vertices",
        "annotation": "",
        "icon": ""
    },
    {
        "name": "spPaint3D",
        "function": "sp_paint_3d",
        "annotation": "",
        "icon": ""
    },
    {
        "submenu": "Transfer UVs",
        "tools": [
            {
                "name": "Component Space",
                "function": "transfer_uvs_component",
                "annotation": "",
                "icon": ""
            },
            {
                "name": "Topology Space",
                "function": "transfer_uvs_topology",
                "annotation": "",
                "icon": ""
            },
            {
                "name": "Topology Space (Inverted)",
                "function": "transfer_uvs_topology_inverted",
                "annotation": "",
                "icon": ""
            },
            {
                "name": "World Space",
                "function": "transfer_uvs_world",
                "annotation": "",
                "icon": ""
            }
        ]
    },
    {
        "name": "UV Deluxe",
        "function": "uv_deluxe",
        "annotation": "",
        "icon": ""
    },
    {
        "name": "UV Islands to Meshes",
        "function": "uv_islands_to_meshes",
        "annotation": "Converts an unwrapped mesh's UV layout to actual polygons.",
        "icon": ""
    },
    {
        "name": "UV Texture",
        "function": "uv_texture",
        "annotation": "",
        "icon": ""
    }
]


################################################################################
# Helper functions
################################################################################


def _get_center():
    """Get the world space center point using the bounding box."""
    bounding_box = pm.polyEvaluate(boundingBoxComponent = True, accurateEvaluation = True)
    center_x = bounding_box[0][0] + (bounding_box[0][1] - bounding_box[0][0]) / 2
    center_y = bounding_box[1][0] + (bounding_box[1][1] - bounding_box[1][0]) / 2
    center_z = bounding_box[2][0] + (bounding_box[2][1] - bounding_box[2][0]) / 2
    return (center_x, center_y, center_z)


################################################################################
# Tools
################################################################################


def flatten_x(*args):
    """"""
    pm.polyMoveVertex(scale=(0,1,1), pivot=_get_center())


def flatten_y(*args):
    """"""
    pm.polyMoveVertex(scale=(1,0,1), pivot=_get_center())


def flatten_z(*args):
    """"""
    pm.polyMoveVertex(scale=(1,1,0), pivot=_get_center())


def instance_along_curve(*args):
    """"""
    pass


def mirror_instance(*args):
    """"""
    pass


def mirror_shell(*args):
    """"""
    pass


def rail_relax(*args):
    """Evenly spreads the selected edges along their enclosing edge loops. Original MEL version by Wim Coene."""
    all_edges = pm.ls(pm.polyListComponentConversion(te = True), fl = True, sl = True)
    for edge in all_edges:
        edge = pm.ls(edge)[0]
        adjacent_faces = pm.ls(pm.polyListComponentConversion(edge, tf = True), fl = True)
        face_edges = pm.ls(pm.polyListComponentConversion(adjacent_faces, te = True), fl = True)
        edge_vertices = pm.ls(pm.polyListComponentConversion(edge, tv = True), fl = True)
        vertex_edges = pm.ls(pm.polyListComponentConversion(edge_vertices, te = True), fl = True)
        rail_edges = [i for i in face_edges if i not in vertex_edges]
        rail_edges = [i for i in face_edges if i not in rail_edges]
        rail_edges.remove(edge)
        for edge_vertex in edge_vertices:
            edges_surrounding_vertex = pm.ls(pm.polyListComponentConversion(edge_vertex, te = True), fl = True)
            unnecessary_edges = [i for i in edges_surrounding_vertex if i not in rail_edges]
            vertex_rail_edges = [i for i in edges_surrounding_vertex if i not in unnecessary_edges]
            if len(vertex_rail_edges) == 2:
                rail_edge_a_vertices = pm.ls(pm.polyListComponentConversion(vertex_rail_edges[0], tv = True), fl = True)
                rail_edge_a_vertex = [i for i in rail_edge_a_vertices if i not in edge_vertices][0]
                rail_edge_b_vertices = pm.ls(pm.polyListComponentConversion(vertex_rail_edges[1], tv = True), fl = True)
                rail_edge_b_vertex = [i for i in rail_edge_b_vertices if i not in edge_vertices][0]
                if vertex_rail_edges[0].getLength() > vertex_rail_edges[1].getLength():
                    rail_edge_a_vertex, rail_edge_b_vertex = rail_edge_b_vertex, rail_edge_a_vertex
                cor_a = dt.Vector(pm.xform(rail_edge_a_vertex, q = True, t = True, ws = True))
                cor_b = dt.Vector(pm.xform(rail_edge_b_vertex, q = True, t = True, ws = True))
                cor_c = dt.Vector(pm.xform(edge_vertex, q = True, t = True, ws = True))
                ab = cor_b - cor_a
                bc = cor_c - cor_b
                ac = cor_c - cor_a
                cos = (ab * -1).dot(bc) / (ab.length() * bc.length())
                if cos >= 1:
                    cos = 1
                alpha = math.acos(cos)
                n = ab / 2 + cor_a + ab.cross(bc).normal().cross(ab).normal() * (ab.length() / 2) * math.tan(alpha)
                pm.xform(edge_vertex, ws = True, t = (n[0], n[1], n[2]))


def select_ngons(*args):
    """"""
    pass


def select_triangles(*args):
    """"""
    pass


def select_sixpoles(*args):
    """"""
    pass


def snap_vertices(*args):
    """"""
    pass


def sp_paint_3d(*args):
    """"""
    pass


def transfer_uvs_component(*args):
    """"""
    pass


def transfer_uvs_topology(*args):
    """"""
    pass


def transfer_uvs_topology_inverted(*args):
    """"""
    pass


def transfer_uvs_world(*args):
    """"""
    pass


def uv_deluxe(*args):
    """"""
    pass


def uv_islands_to_meshes(*args):
    """"""
    this_selection = pm.ls(sl = True)
    this_object = this_selection[0]
    pm.runtime.ConvertSelectionToUVs()
    pm.polySelectConstraint(type = 0x0010, where = 1, mode = 2)
    pm.polySelectConstraint(mode = 0)
    pm.polyListComponentConversion(toVertex = True)
    pm.polySplitVertex()
    vertex_count = pm.polyEvaluate(this_object, vertex = True)
    pm.select("{}.vtx[0:{}]".format(this_object, vertex_count), replace = True)
    vertices = pm.ls(sl = True, flatten = True)
    multiplier = 10
    for vertex in vertices:
        pm.select(vertex)
        uv = pm.polyListComponentConversion(tuv = True)
        pm.select(uv)
        pos = pm.polyEditUV(query = True, vValue = True)
        pos[0] *= multiplier
        pos[1] *= multiplier
        pm.select(vertex)
        pm.xform(ws = True, a = True, t = (pos[0], pos[1], 0))
    pm.polyMergeVertex(this_object, d = 0.001, ch = 1, tx = 0)


def uv_texture(*args):
    """"""
    pass
