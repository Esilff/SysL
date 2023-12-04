import bpy
from bpy.types import Context

def remove_rule():
    pass

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

# --------------------------------- Operators ---------------------------------

class OP_add_rule(bpy.types.Operator):
    bl_label=""
    bl_idname="op.add_rule"

    def execute(self, context):
        context.scene.rules_collection.collection.add()
        return {"FINISHED"}

class OP_remove_rule(bpy.types.Operator):
    bl_label=""
    bl_idname="op.remove_rule"

    def execute(self, context):
        rule_collection = context.scene.rules_collection.collection
        rule_collection.remove(len(rule_collection) - 1)
        return {"FINISHED"}
    
class OP_clear_rules(bpy.types.Operator):
    bl_label=""
    bl_idname="op.clear_rules"
    bl_description="Clear "

    def execute(self,context):
        context.scene.rules_collection.collection.clear()
        return {"FINISHED"}

    
# --------------------------------- Pannels ---------------------------------

class LSysRulesPanel(bpy.types.Panel):
    bl_label="Rules"
    bl_idname="PT_LSYS_RULES"
    bl_space_type="VIEW_3D"
    bl_region_type="UI"
    bl_category="SysL"

    def render_rules(self,layout, rules):
        for index, rule in enumerate(rules):
            row = layout.row()
            row.prop(rule, "expression")
            row.prop(rule, "enabled", icon="HIDE_OFF")

    def render_operators(self, layout):
        layout.operator("op.add_rule", icon="ADD")
        layout.operator("op.remove_rule", icon="REMOVE")
        layout.operator("op.clear_rules", icon="X")

    def draw(self, context: Context):
        layout = self.layout
        rules = context.scene.rules_collection.collection

        layout.label(text="Expressions")

        split_box = layout.box().split(factor=0.85)
        
        self.render_rules(split_box.column(), rules)
        self.render_operators(split_box.column())


class LSysAxiomPanel(bpy.types.Panel):
    bl_label="Axioms"
    bl_idname="PT_LSYS_AXIOMS"
    bl_space_type="VIEW_3D"
    bl_region_type="UI"
    bl_category="SysL"

    def render_axioms(self):
        pass

    def draw(self, context: Context):
        layout = self.layout

class LSysRenderPanel(bpy.types.Panel):
    bl_label="Render"
    bl_idname="PT_LSYS_RENDER"
    bl_space_type="VIEW_3D"
    bl_region_type="UI"
    bl_category="SysL"

    def draw(self, context: Context):
        layout = self.layout

def define_props():
    bpy.types.Scene.rules_collection = bpy.props.PointerProperty(type=RuleCollectionProperty)

# --------------------------------- Registration ---------------------------------

def register():
    # REGISTERING PROPERTIES

    bpy.utils.register_class(RuleProperty)
    bpy.utils.register_class(RuleCollectionProperty)

    # REGISTERING OPERATORS
    
    bpy.utils.register_class(OP_add_rule)
    bpy.utils.register_class(OP_remove_rule)
    bpy.utils.register_class(OP_clear_rules)

    # REGISTERING PANELS
    bpy.utils.register_class(LSysRulesPanel)
    bpy.utils.register_class(LSysAxiomPanel)
    bpy.utils.register_class(LSysRenderPanel)
    define_props()

def unregister():
    # UNREGISTERING PROPERTIES

    bpy.utils.unregister_class(RuleProperty)
    bpy.utils.unregister_class(RuleCollectionProperty)

    # UNREGISTERING PROPERTIES

    bpy.utils.unregister_class(OP_add_rule)
    bpy.utils.unregister_class(OP_remove_rule)
    bpy.utils.unregister_class(OP_clear_rules)
    
    # UNREGISTERING PANELS
    bpy.utils.unregister_class(LSysRulesPanel)
    bpy.utils.unregister_class(LSysAxiomPanel)
    bpy.utils.unregister_class(LSysRenderPanel)



if __name__ == "__main__":
    register()

