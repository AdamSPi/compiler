from r1 import *
# rco_ast = P(\
# 	ADD(
# 		ADD(NUM(2), NUM(3)),
# 		LET(VAR('X'), READ(), ADD(VAR('X'), VAR('X'))
# 		)
# 	)
# )
# # import pdb; pdb.set_trace()
# # rco_ast.rcoify().show()

# P(
# 	LET(VAR('rco0'), ADD(NUM(2), NUM(3)),
# 		LET(VAR('rco1'), READ(), 
# 			LET(VAR('rco2'), ADD(VAR('rco1'), VAR('rco1')),
# 				LET(VAR('rco3'), ADD(VAR('rco0'), VAR('rco2')), VAR('rco3'))
# 			)
# 		)
# 	)
# )

# rco_ast.pprint()
# rco_ast.uniqueify().rcoify().pprint()
# rco_ast.to_c().pprint()
# print(rco_ast.interp(True, True))
# print(rco_ast.uniqueify().rcoify().interp(True, True))
# print(rco_ast.to_c().interp(True, True))
# c1 = rco_ast.to_c()
# c1.uncover_locs()
# print(c1.info['locals'])
# c1.pprint()

# p1 = P(ADD(NUM(52), NEG(NUM(10))))
# p1.to_c().select().pprint()
# print()
# p1.to_x().assign_homes().pprint()
# print(p1.to_x().assign_homes().interp(True, True))

# p2 = P(
# 		LET(
# 			VAR('A'), NUM(42),
# 			LET(
# 				VAR('B'), READ(),
# 				VAR('B')
# 			)
# 		)
# 	)

# x = p2.uniqueify().rcoify()
# x.pprint()
# xx = x.expcon()
# xx.pprint()
# print()
# print(p2.to_x().assign_homes().patch_instr().interp(True, True))