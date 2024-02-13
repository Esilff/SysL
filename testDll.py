import SysL

sysl: SysL = SysL()

tortoise = sysl.get_tortoise()
axiom = "F-F"
rule = "F=F+F"
sysl.add_rule(tortoise, rule)

print(f"Processing Axiom({axiom}) : {sysl.generate_axiom(tortoise, axiom, 1)}")

sysl.add_rule(tortoise, rule)


