import math

import bmesh
import bpy
from mathutils import Vector, Matrix

rules: dict = {}
axioms: list = []

# --------------------------------- Properties ---------------------------------

"""
A rule is an expression that follows the format <name>=<expression> and it is applied to axioms if the name is found in
it.
A rule can be ignored depending on the value of the enabled parameter.
"""

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

"""
A collection of rules for the addon.
"""

class RuleCollectionProperty(bpy.types.PropertyGroup):
    collection: bpy.props.CollectionProperty(type=RuleProperty)

"""
An axiom is a default expression used for rendering. Rules are applied onto it a number of times depending on the 
iteration param.
@var name: The name of the axiom
@var expression: The expression of the axiom
@var enabled: Determines if the axiom should be processed or not
@var iterations: The number of times rules are applied to the expression
@var alpha: The angle in degrees used for operators like +,-,>,<,&,^
@var position: The starting position of the LSystem
@var step: The distance between each segment or the distance of a F operator.
"""

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
    step: bpy.props.FloatProperty(
        name="Step",
        default=1
    )

"""
A collection of axioms for the addon.
"""

class AxiomCollectionProperty(bpy.types.PropertyGroup):
    collection: bpy.props.CollectionProperty(type=AxiomProperty)

"""
Rendering options for the addon.
@var skinned: Whether or not to add a skin modifier to the final result.
@var relative_radius: unused for the moment, should determine if the thinkness of the branch should be proportional to
the depth in the tree.
"""

class RenderOptionsProperty(bpy.types.PropertyGroup):
    skinned: bpy.props.BoolProperty(name="Skinned", default=False)
    relative_radius: bpy.props.BoolProperty(name="Relative radius", default=False)

# --------------------------------- Operators ---------------------------------

"""
An operator to add a rule to the collection.
"""

class OP_add_rule(bpy.types.Operator):
    bl_label = ""
    bl_idname = "op.add_rule"

    def execute(self, context):
        context.scene.rules_collection.collection.add()
        return {"FINISHED"}

"""
An operator to remove a rule from the collection.
"""

class OP_remove_rule(bpy.types.Operator):
    bl_label = ""
    bl_idname = "op.remove_rule"

    def execute(self, context):
        rule_collection = context.scene.rules_collection.collection
        rule_collection.remove(len(rule_collection) - 1)
        return {"FINISHED"}

"""
An operator to clear all rules.
"""

class OP_clear_rules(bpy.types.Operator):
    bl_label = ""
    bl_idname = "op.clear_rules"
    bl_description = "Clear "

    def execute(self, context):
        context.scene.rules_collection.collection.clear()
        return {"FINISHED"}

"""
An operator to add an axiom to the collection.
"""

class OP_add_axiom(bpy.types.Operator):
    bl_label = ""
    bl_idname = "op.add_axiom"

    def execute(self, context):
        axiom_collection = context.scene.axiom_collection.collection.add()
        return {"FINISHED"}

"""
An operator to remove an axiom from the collection.
"""

class OP_remove_axiom(bpy.types.Operator):
    bl_label = ""
    bl_idname = "op.remove_axiom"

    def execute(self, context):
        axiom_collection = context.scene.axiom_collection.collection
        axiom_collection.remove(len(axiom_collection) - 1)
        return {"FINISHED"}

"""
An operator to clear all axioms from the collection.
"""

class OP_clear_axiom(bpy.types.Operator):
    bl_label = ""
    bl_idname = "op.clear_axioms"

    def execute(self, context):
        axiom_collection = context.scene.axiom_collection.collection.clear()

        return {"FINISHED"}

"""
An operator in charge of processing the axioms.
"""

class OP_Render_system(bpy.types.Operator):
    bl_label = ""
    bl_idname = "op.render_sys"

    """
    Parse the rules and stores them in a dictionary that is later used to replace the name with the relative expression.
    """

    def parse_rules(self, rules_list):
        rules.clear()
        for index, value in enumerate(rules_list):
            if not value.enabled:
                continue
            name, exp = value.expression.split("=")
            rules[name] = exp

    """
       Iterates over an axiom expression to find and apply rules.
    """

    def iterate_axiom(self, axiom, iterations):
        axioms.clear()
        for i in range(iterations):
            for key in rules.keys():
                axiom = axiom.replace(key, rules[key])
        print("Processed axiom : ", axiom)
        axioms.append(axiom)

    """
       Iterates over all axioms to start the axiom processing.
    """

    def iterate(self, axioms):
        for index, value in enumerate(axioms):
            if not value.enabled:
                continue
            self.iterate_axiom(value.expression, value.iterations)

    """
       Renders the axioms based on the expressions and operators.
    """

    def render_axiom(self, expression, axiom, options):
        name = axiom.name or f"axiom_{axiom.index}"
        vec = Vector((axiom.step, 0.0, 0.0))
        radians = math.radians(axiom.alpha)
        p_rot_mat = Matrix.Rotation(radians, 4, 'Z')  # Turn right
        n_rot_mat = Matrix.Rotation(-radians, 4, 'Z')  # Turn left
        up_rot_mat = Matrix.Rotation(radians, 4, 'Y')  # Turn upwards
        down_rot_mat = Matrix.Rotation(-radians, 4, 'Y')  # Turn downwards
        ri_rot_mat = Matrix.Rotation(radians, 4, 'X')  # Turn right on itself (ri)
        li_rot_mat = Matrix.Rotation(-radians, 4, 'X')  # Turn left on itself (li)
        state_stack = []
        source = None
        # Creating the base point
        self.create_point(name, axiom.position)
        # Applying operations
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
            if char == '>':
                vec = ri_rot_mat @ vec
            if char == '<':
                vec = li_rot_mat @ vec
            if char == '[':
                state_stack.append(self.last_extrude(name))
            if char == ']':
                source = state_stack.pop()
        # Apply skin modifier if True
        if options.skinned:
            self.add_skin_modifier(name, options)

    """
    Create an object with a name an a single point.
    @param name: the name of the object
    @param position: the position of the object
    """
    def create_point(self, name, position):
        mesh = bpy.data.meshes.new('SingleVertex')
        obj = bpy.data.objects.new(name, mesh)
        bpy.context.collection.objects.link(obj)
        obj.location = position
        mesh.from_pydata([position], [], [])

    """
    Retrieve the last extruded position of the object. Only used for the [ operator in order to save a point.
    @param name: the name of the object
    """
    def last_extrude(self, object_name):
        obj = bpy.data.objects.get(object_name)
        if not obj or obj.type != 'MESH' or not obj.data.vertices:
            print("Invalid object.")
            return None
        return obj.data.vertices[-1].co.copy()  # Return the position of the last vertex

    """
    Extrudes a single point from the current object.
    @param name: the name of the object
    @param extrusion_vector: the direction of the extrusion
    @param source_position: a position to retrieve a point from the object, it is defined when the ] is used in order
    to go back to the saved position.
    """

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

    """
    Adds a skin modifier to the object.
    @param object_name: The name of the object
    """

    def add_skin_modifier(self, object_name, options):
        obj = bpy.data.objects.get(object_name)
        if obj is None and obj.type != 'MESH':
            return
        obj.modifiers.new(name="Skin", type="SKIN")
        bpy.context.view_layer.update()

    """
    Execute the operator
    """

    def execute(self, context):
        rules_collection = context.scene.rules_collection.collection
        axiom_collection = context.scene.axiom_collection.collection
        options = context.scene.options

        self.parse_rules(rules_collection)
        self.iterate(axiom_collection)

        # --- Rendering stage ---
        for index, value in enumerate(axioms):
            axiom_prop = axiom_collection[index]
            if not axiom_prop.enabled:
                continue
            self.render_axiom(
                value,
                axiom_prop,
                options
            )

        return {"FINISHED"}


# --------------------------------- Pannels ---------------------------------

"""
Renders the rule pannel.
"""

class LSysRulesPanel(bpy.types.Panel):
    bl_label = "Rules"
    bl_idname = "PT_LSYS_RULES"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "SysL"

    """
    Renders the left part of the expression box where rules fields are displayed.
    """

    def render_rules(self, layout, rules):
        for index, rule in enumerate(rules):
            row = layout.row()
            row.prop(rule, "expression")
            row.prop(rule, "enabled", icon="HIDE_OFF")

    """
    Renders the right part of the expression box where buttons are displayed
    """

    def render_operators(self, layout):
        layout.operator("op.add_rule", icon="ADD")
        layout.operator("op.remove_rule", icon="REMOVE")
        layout.operator("op.clear_rules", icon="X")

    def draw(self, context):
        layout = self.layout
        rules = context.scene.rules_collection.collection

        layout.label(text="Expressions")

        split_box = layout.box().split(factor=0.85)  # Spliting a box into 2

        self.render_rules(split_box.column(), rules)
        self.render_operators(split_box.column())

"""
Renders the axiom pannel.
"""

class LSysAxiomPanel(bpy.types.Panel):
    bl_label = "Axioms"
    bl_idname = "PT_LSYS_AXIOMS"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "SysL"

    """
        Renders the left part of the axiom box where axiom fields are displayed.
    """

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
            layout.prop(axiom, "step")

    """
        Renders the right part of the axiom box where buttons are displayed
    """

    def render_operators(self, layout):
        layout.operator("op.add_axiom", icon="ADD")
        layout.operator("op.remove_axiom", icon="REMOVE")
        layout.operator("op.clear_axioms", icon="X")

    def draw(self, context):
        layout = self.layout
        axioms = context.scene.axiom_collection.collection

        split_box = layout.box().split(factor=0.85)  # Splitting a box in 2
        self.render_axioms(split_box.column(), axioms)
        self.render_operators(split_box.column())

"""
Renders the rendering pannel.
"""

class LSysRenderPanel(bpy.types.Panel):
    bl_label = "Render"
    bl_idname = "PT_LSYS_RENDER"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "SysL"

    def draw(self, context):
        layout = self.layout
        options = context.scene.options
        layout.prop(options, "skinned")
        if options.skinned:
            layout.prop(options, "relative_radius")
        layout.operator("op.render_sys", text="Render")


"""
Define the scene props.
"""

def define_props():
    bpy.types.Scene.rules_collection = bpy.props.PointerProperty(type=RuleCollectionProperty)
    bpy.types.Scene.axiom_collection = bpy.props.PointerProperty(type=AxiomCollectionProperty)
    bpy.types.Scene.options = bpy.props.PointerProperty(type=RenderOptionsProperty)

# --------------------------------- Registration ---------------------------------

def register():
    # REGISTERING PROPERTIES

    bpy.utils.register_class(RuleProperty)
    bpy.utils.register_class(RuleCollectionProperty)
    bpy.utils.register_class(AxiomProperty)
    bpy.utils.register_class(AxiomCollectionProperty)
    bpy.utils.register_class(RenderOptionsProperty)

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
    bpy.utils.unregister_class(RenderOptionsProperty)
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
