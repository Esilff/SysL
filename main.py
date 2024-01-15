import math

import bmesh
import bpy
from mathutils import Vector, Matrix

rules: dict = {}
axioms: list = []

# --------------------------------- Properties ---------------------------------

class RuleProperty(bpy.types.PropertyGroup):
    expression: bpy.props.StringProperty(
        name="",
        description="The expression of the rule, should follow the following syntax: name=rule"
    )
    enabled: bpy.props.BoolProperty(
        name="",
        description="Enables the rule to be applied",
        default=True
    )


class RuleCollectionProperty(bpy.types.PropertyGroup):
    collection: bpy.props.CollectionProperty(type=RuleProperty)


class AxiomProperty(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(
        name="Name",
        description="The name used in the scene"
    )
    expression: bpy.props.StringProperty(
        name="",
        description="The expression of the axiom"
    )
    enabled: bpy.props.BoolProperty(
        name="",
        description="Enables the axiom to be processed",
        default=True
    )
    iterations: bpy.props.IntProperty(
        name="Iterations",
        default=1
    )
    alpha: bpy.props.FloatProperty(
        name="Alpha",
        default=45
    )
    position: bpy.props.FloatVectorProperty(
        name="Position"
    )


class AxiomCollectionProperty(bpy.types.PropertyGroup):
    collection: bpy.props.CollectionProperty(type=AxiomProperty)


# --------------------------------- Operators ---------------------------------

class OP_add_rule(bpy.types.Operator):
    bl_label = ""
    bl_idname = "op.add_rule"

    def execute(self, context):
        context.scene.rules_collection.collection.add()
        return {"FINISHED"}


class OP_remove_rule(bpy.types.Operator):
    bl_label = ""
    bl_idname = "op.remove_rule"

    def execute(self, context):
        rule_collection = context.scene.rules_collection.collection
        rule_collection.remove(len(rule_collection) - 1)
        return {"FINISHED"}


class OP_clear_rules(bpy.types.Operator):
    bl_label = ""
    bl_idname = "op.clear_rules"
    bl_description = "Clear "

    def execute(self, context):
        context.scene.rules_collection.collection.clear()
        return {"FINISHED"}


class OP_add_axiom(bpy.types.Operator):
    bl_label = ""
    bl_idname = "op.add_axiom"

    def execute(self, context):
        axiom_collection = context.scene.axiom_collection.collection.add()
        return {"FINISHED"}


class OP_remove_axiom(bpy.types.Operator):
    bl_label = ""
    bl_idname = "op.remove_axiom"

    def execute(self, context):
        axiom_collection = context.scene.axiom_collection.collection
        axiom_collection.remove(len(axiom_collection) - 1)
        return {"FINISHED"}


class OP_clear_axiom(bpy.types.Operator):
    bl_label = ""
    bl_idname = "op.clear_axioms"

    def execute(self, context):
        axiom_collection = context.scene.axiom_collection.collection.clear()

        return {"FINISHED"}


class OP_Render_system(bpy.types.Operator):
    bl_label = ""
    bl_idname = "op.render_sys"


    def parse_rules(self, rules_list):
        rules.clear()
        for index, value in enumerate(rules_list):
            if not value.enabled:
                continue
            name, exp = value.expression.split("=")
            rules[name] = exp

    def iterate_axiom(self, axiom, iterations):
        axioms.clear()
        for i in range(iterations):
            for key in rules.keys():
                axiom = axiom.replace(key, rules[key])
        print("Processed axiom : ", axiom)
        axioms.append(axiom)

    def iterate(self, axioms):
        for index, value in enumerate(axioms):
            if not value.enabled:
                continue
            self.iterate_axiom(value.expression, value.iterations)

    # def render_points(self):

    def render_axiom(self, expression, axiom):
        name = axiom.name or f"axiom_{axiom.index}"
        vec = Vector((1.0, 0.0, 0.0))
        radians = math.radians(axiom.alpha)
        p_rot_mat = Matrix.Rotation(radians, 4, 'Z')
        n_rot_mat = Matrix.Rotation(-radians, 4, 'Z')
        up_rot_mat = Matrix.Rotation(radians, 4, 'Y')
        down_rot_mat = Matrix.Rotation(-radians, 4, 'Y')
        state_stack = []
        source = None
        self.create_point(name, axiom.position)
        for char in expression:
            if char == 'F':
                self.extrude_object(name, vec, source)
            if char == '+':
                vec = p_rot_mat @ vec
            if char == '-':
                vec = n_rot_mat @ vec
            if char == '^':
                vec = up_rot_mat @ vec
            if char == '&':
                vec = down_rot_mat @ vec
            if char == '[':
                state_stack.append(self.last_extrude(name))
            if char == ']':
                source = state_stack.pop()

            print(f"Vector: {vec}")

    def create_point(self, name, position):
        mesh = bpy.data.meshes.new('SingleVertex')
        obj = bpy.data.objects.new(name, mesh)
        bpy.context.collection.objects.link(obj)
        obj.location = position
        mesh.from_pydata([position], [], [])

    def last_extrude(self, object_name):
        obj = bpy.data.objects.get(object_name)
        if not obj or obj.type != 'MESH' or not obj.data.vertices:
            print("Invalid object.")
            return None
        return obj.data.vertices[-1].co.copy()  # Return the position of the last vertex

    def extrude_object(self, object_name, extrusion_vector, source_position=None):
        obj = bpy.data.objects.get(object_name)
        if not obj or obj.type != 'MESH' or not obj.data.vertices:
            print("Invalid object.")
            return

        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.mode_set(mode='EDIT')
        bm = bmesh.from_edit_mesh(obj.data)
        bm.verts.ensure_lookup_table()

        if source_position is not None:
            closest_vert = min(bm.verts, key=lambda v: (v.co - source_position).length)
            closest_vert.select = True
        else:
            bm.verts[-1].select = True

        bmesh.update_edit_mesh(obj.data)
        bpy.ops.mesh.extrude_vertices_move(TRANSFORM_OT_translate={"value": extrusion_vector})
        bpy.ops.object.mode_set(mode='OBJECT')

    def execute(self, context):
        rules_collection = context.scene.rules_collection.collection
        axiom_collection = context.scene.axiom_collection.collection

        self.parse_rules(rules_collection)
        self.iterate(axiom_collection)

        # --- Rendering stage ---
        for index, value in enumerate(axioms):
            axiom_prop = axiom_collection[index]
            if not axiom_prop.enabled:
                continue
            self.render_axiom(
                value,
                axiom_prop
            )

        return {"FINISHED"}


# --------------------------------- Pannels ---------------------------------

class LSysRulesPanel(bpy.types.Panel):
    bl_label = "Rules"
    bl_idname = "PT_LSYS_RULES"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "SysL"

    def render_rules(self, layout, rules):
        for index, rule in enumerate(rules):
            row = layout.row()
            row.prop(rule, "expression")
            row.prop(rule, "enabled", icon="HIDE_OFF")

    def render_operators(self, layout):
        layout.operator("op.add_rule", icon="ADD")
        layout.operator("op.remove_rule", icon="REMOVE")
        layout.operator("op.clear_rules", icon="X")

    def draw(self, context):
        layout = self.layout
        rules = context.scene.rules_collection.collection

        layout.label(text="Expressions")

        split_box = layout.box().split(factor=0.85)

        self.render_rules(split_box.column(), rules)
        self.render_operators(split_box.column())


class LSysAxiomPanel(bpy.types.Panel):
    bl_label = "Axioms"
    bl_idname = "PT_LSYS_AXIOMS"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "SysL"

    def render_axioms(self, layout, axioms):
        for index, axiom in enumerate(axioms):
            layout.prop(axiom, "name")
            row = layout.row()
            row.prop(axiom, "expression")
            row.prop(axiom, "enabled", icon="HIDE_OFF")
            layout.prop(axiom, "iterations")
            layout.prop(axiom, "alpha")
            position_row = layout.row()
            position_row.prop(axiom, "position")

    def render_operators(self, layout):
        layout.operator("op.add_axiom", icon="ADD")
        layout.operator("op.remove_axiom", icon="REMOVE")
        layout.operator("op.clear_axioms", icon="X")

    def draw(self, context):
        layout = self.layout
        axioms = context.scene.axiom_collection.collection

        layout.label(text="Axioms")

        split_box = layout.box().split(factor=0.85)
        self.render_axioms(split_box.column(), axioms)
        self.render_operators(split_box.column())


class LSysRenderPanel(bpy.types.Panel):
    bl_label = "Render"
    bl_idname = "PT_LSYS_RENDER"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "SysL"

    def draw(self, context):
        layout = self.layout
        layout.operator("op.render_sys", text="Render")


def define_props():
    bpy.types.Scene.rules_collection = bpy.props.PointerProperty(type=RuleCollectionProperty)
    bpy.types.Scene.axiom_collection = bpy.props.PointerProperty(type=AxiomCollectionProperty)


# --------------------------------- Registration ---------------------------------

def register():
    # REGISTERING PROPERTIES

    bpy.utils.register_class(RuleProperty)
    bpy.utils.register_class(RuleCollectionProperty)
    bpy.utils.register_class(AxiomProperty)
    bpy.utils.register_class(AxiomCollectionProperty)

    # REGISTERING OPERATORS

    bpy.utils.register_class(OP_add_rule)
    bpy.utils.register_class(OP_remove_rule)
    bpy.utils.register_class(OP_clear_rules)

    bpy.utils.register_class(OP_add_axiom)
    bpy.utils.register_class(OP_remove_axiom)
    bpy.utils.register_class(OP_clear_axiom)

    bpy.utils.register_class(OP_Render_system)

    # REGISTERING PANELS
    bpy.utils.register_class(LSysRulesPanel)
    bpy.utils.register_class(LSysAxiomPanel)
    bpy.utils.register_class(LSysRenderPanel)
    define_props()


def unregister():
    # UNREGISTERING PROPERTIES

    bpy.utils.unregister_class(RuleProperty)
    bpy.utils.unregister_class(RuleCollectionProperty)
    bpy.utils.unregister_class(AxiomProperty)
    bpy.utils.unregister_class(AxiomCollectionProperty)

    # UNREGISTERING PROPERTIES

    bpy.utils.unregister_class(OP_add_rule)
    bpy.utils.unregister_class(OP_remove_rule)
    bpy.utils.unregister_class(OP_clear_rules)

    bpy.utils.unregister_class(OP_add_axiom)
    bpy.utils.unregister_class(OP_remove_axiom)
    bpy.utils.unregister_class(OP_clear_axiom)

    bpy.utils.unregister_class(OP_Render_system)

    # UNREGISTERING PANELS
    bpy.utils.unregister_class(LSysRulesPanel)
    bpy.utils.unregister_class(LSysAxiomPanel)
    bpy.utils.unregister_class(LSysRenderPanel)


if __name__ == "__main__":
    register()
