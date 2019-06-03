#coding:utf-8
from moteur import *
	
mversion=[1.1]

titre=""
description=""
intro="debut"
fin="fin"

########

objet=Obj()
objet.nom='objet'

Endroit=Lieu()
Endroit.nom='endroit'
Endroit.objs.append(objet)

########

perso=Perso()
perso.nom=""
perso.lieu_actu=Endroit

print(intro)
inp("")
main(perso,objet)
inp("")
print(fin)
