import bpy
from bpy.types import Context

# --------------------------------- Properties ---------------------------------

class RuleProperty(bpy.types.PropertyGroup):
    expression: bpy.props.StringProperty(
        name="Expression",
        description="The expression of the rule, should follow the following syntax: name=rule"
    )
    enabled: bpy.props.BoolProperty(
        name="Enabled",
        description="Enables the rule to be applied",
        default=True
    )

class RuleCollectionProperty(bpy.types.PropertyGroup):
    pass

# --------------------------------- Pannels ---------------------------------

class LSysRulesPanel(bpy.types.Panel):
    bl_label="Rules"
    bl_idname="PT_LSYS_RULES"
    bl_space_type="VIEW_3D"
    bl_region_type="UI"
    bl_category="SysL"

    def render_rules(self):
        pass

    def draw(self, context: Context):
        layout = self.layout
        layout.label(text="Rules")


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



# --------------------------------- Registration ---------------------------------

def register():
    
    bpy.utils.register_class(LSysRulesPanel)
    bpy.utils.register_class(LSysAxiomPanel)
    bpy.utils.register_class(LSysRenderPanel)

def unregister():

    bpy.utils.unregister_class(LSysRulesPanel)
    bpy.utils.unregister_class(LSysAxiomPanel)
    bpy.utils.unregister_class(LSysRenderPanel)

if __name__ == "__main__":
    register()