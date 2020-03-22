from r1 import *
rco_ast = P(\
	ADD(
		ADD(NUM(2), NUM(3)),
		LET(VAR('X'), READ(), ADD(VAR('X'), VAR('X'))
		)
	)
)
# import pdb; pdb.set_trace()
# rco_ast.rcoify().show()

P(
	LET(VAR('rco0'), ADD(NUM(2), NUM(3)),
		LET(VAR('rco1'), READ(), 
			LET(VAR('rco2'), ADD(VAR('rco1'), VAR('rco1')),
				LET(VAR('rco3'), ADD(VAR('rco0'), VAR('rco2')), VAR('rco3'))
			)
		)
	)
)

rco_ast.pprint()
rco_ast.uniqueify().rcoify().pprint()
rco_ast.to_c().pprint()
print(rco_ast.interp(True, True))
print(rco_ast.uniqueify().rcoify().interp(True, True))
print(rco_ast.to_c().interp(True, True))