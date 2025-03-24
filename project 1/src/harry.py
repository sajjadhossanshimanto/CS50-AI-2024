from logic import *

rain = Symbol("rain")# it is rainning
hagrid = Symbol("hagrid")# harry visit hagrid
dumbledore = Symbol("dumbledore")# harry visit dumbledore

knowledge = And(
    Implication(Not(rain), hagrid),# if it is not rains, then harry will visit hagrid
    Or(hagrid, dumbledore),# harry will visit hagrid or dumledore
    Not(And(hagrid, dumbledore)),# but not both
    dumbledore# harry viisted dumleedore
)

# print(model_check(knowledge, rain))
# print(Not(And(hagrid, dumbledore)).parenthesize())
print(knowledge.formula())
