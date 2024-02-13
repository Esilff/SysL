import bpy
import sys
from SysL import SysL

sysl = SysL()


class RuleProperty(bpy.types.PropertyGroup):
    expression: bpy.props.StringProperty(
        name="",
        description="The expression of the rule, should follow the following syntax: name=rule"
    )


class RuleCollectionProperty(bpy.types.PropertyGroup):
    list: bpy.props.CollectionProperty(type=RuleProperty)


class AxiomProperty(bpy.types.PropertyGroup):
    expression: bpy.props.StringProperty(
        name="",
        description="The base expression used for generation"
    )
    iterations: bpy.props.IntProperty(
        name="Iterations",
        default=1
    )


class AxiomCollectionProperty(bpy.types.PropertyGroup):
    list: bpy.props.CollectionProperty(type=AxiomProperty)


class AddRule(bpy.types.Operator):
    bl_label = ""
    bl_idname = "op.add_rule"

    def execute(self, context):
        context.scene.rules.list.add()
        return {"FINISHED"}


class ClearRules(bpy.types.Operator):
    bl_label = ""
    bl_idname = "op.clear_rules"

    def execute(self, context):
        context.scene.rules.list.clear()
        return {"FINISHED"}


class AddAxiom(bpy.types.Operator):
    bl_label = ""
    bl_idname = "op.add_axiom"

    def execute(self, context):
        context.scene.axioms.list.add()
        return {"FINISHED"}


class ClearAxioms(bpy.types.Operator):
    bl_label = ""
    bl_idname = "op.clear_axioms"

    def execute(self, context):
        context.scene.axioms.list.clear()
        return {"FINISHED"}

class DllCallOperator(bpy.types.Operator):
    bl_label = ""
    bl_idname = "op.call_dll"

    def execute(self, context):
        rules = context.scene.rules.list
        axioms = context.scene.axioms.list

        tortoise = sysl.get_tortoise()

        for index, rule in enumerate(rules):
            sysl.add_rule(tortoise, rule.expression)

        sysl.generate_axiom(tortoise, axioms[0].expression, axioms[0].iterations)
        print("Tortoise generated")
        return {"FINISHED"}


class SysLRulesPanel(bpy.types.Panel):
    bl_label = "Rules"
    bl_idname = "_PT_SYSL_RULES"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "SysL"

    def render_rules(self, layout, rules):
        for index, rule in enumerate(rules):
            layout.prop(rule, "expression")

    def render_operators(self, layout):
        layout.operator("op.add_rule", icon="ADD")
        layout.operator("op.clear_rules", icon="X")

    def draw(self, context):
        layout = self.layout
        rules = context.scene.rules.list

        layout.label(text="Rules")

        split_box = layout.box().split(factor=0.85)

        self.render_rules(split_box.column(), rules)
        self.render_operators(split_box.column())

class SysLAxiomPanel(bpy.types.Panel):
    bl_label = "Axioms"
    bl_idname = "_PT_SYSL_AXIOMS"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "SysL"

    def render_axioms(self, layout, axioms):
        for index, axiom in enumerate(axioms):
            layout.prop(axiom, "expression")
            layout.prop(axiom, "iterations")

    def render_operators(self, layout):
        layout.operator("op.add_axiom", icon="ADD")
        layout.operator("op.clear_axioms", icon="X")

    def draw(self, context):
        layout = self.layout
        axioms = context.scene.axioms.list

        layout.label(text="Axioms")

        split_box = layout.box().split(factor=0.85)

        self.render_axioms(split_box.column(), axioms)
        self.render_operators(split_box.column())



class SysLRenderingPanel(bpy.types.Panel):
    bl_label = "Render"
    bl_idname = "_PT_SYSL_RENDER"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "SysL"

    def draw(self, context):
        layout = self.layout
        layout.operator("op.call_dll", text="Render")


def define_props():
    bpy.types.Scene.rules = bpy.props.PointerProperty(type=RuleCollectionProperty)
    bpy.types.Scene.axioms = bpy.props.PointerProperty(type=AxiomCollectionProperty)


def register():
    bpy.utils.register_class(RuleProperty)
    bpy.utils.register_class(RuleCollectionProperty)
    bpy.utils.register_class(AxiomProperty)
    bpy.utils.register_class(AxiomCollectionProperty)

    bpy.utils.register_class(AddRule)
    bpy.utils.register_class(ClearRules)
    bpy.utils.register_class(AddAxiom)
    bpy.utils.register_class(ClearAxioms)
    bpy.utils.register_class(DllCallOperator)

    bpy.utils.register_class(SysLRulesPanel)
    bpy.utils.register_class(SysLAxiomPanel)
    bpy.utils.register_class(SysLRenderingPanel)

    define_props()


if __name__ == "__main__":

    register()