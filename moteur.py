#coding:utf-8
version=1.1
print("Moteur version : "+str(version))

def inp(txt):
    if 1:
        return raw_input(txt)
    else:
        return input(txt)


class Evenement:
    def __init__(self):
        self.tipe='evenement'
        self.texte=""
        self.condition=[]
        self.deja_fait=False
        self.actions=[]
        self.tdd=[]
        self.act=True
    def cond(self):
        if self.condition!=[]:
            if len(self.condition) == 3:
                if self.condition[1]=="in":
                    if self.condition[2].tipe!='perso':
                        if self.condition[0] in self.condition[2].objs:
                            return True
                    else:
                        if self.condition[0] in self.condition[2].inventaire:
                            return True
            return False
        else: return True
    def action(self,lieu_actu,perso):
      if self.cond():
        self.deja_fait=True
        for aa in self.tdd:
            if aa[0]==1:
               print(self.texte)
               aa[1].parler.append(aa[2])
            elif aa[0]==2:
                perso.inventaire.append(aa[1])
            elif aa[0]==3:
                lieu_actu.objs.append(aa[1])
 
class Lieu:
    def __init__(self):
        self.tipe='lieu'
        self.nom=''
        self.autre_noms=[]
        self.nord=None
        self.est=None
        self.sud=None
        self.ouest=None
        self.bas=None
        self.haut=None
        self.objs=[]
        self.etat=[]
        self.evenements=[]
        self.deverouille=[]
        self.description=''
        self.deja_ete=False

class  Enemi:
    def __init__(self):
        self.tipe='enemi'
        self.nom=""
        self.vie=1
        self.att=1
        self.description=""
        self.examination=""
        self.etat=[]
        self.objs=[]
        

class Obj:
    def __init__(self):
        self.tipe='obj'
        self.nom=''
        self.autre_noms=[]
        self.etat=[]
        self.objs=[]
        self.description="Rien de spécial à propos de cet objet"
        self.examination=""
        self.fouille=[]  #objets caché
        self.utilisable=[] #[0]=objet utilisable sur lui,[1]action qui s'en suit
        self.actions=[] #[0]=nom de l'action ,[1]=action
        self.parler=[] #[0]=ce qu'il faut dire ''=il n'y a besoin de rien dire , [1]=ce que le personnage(ou objet ou animal) dit
    def action(self,obj):
        acf=False
        for u in self.utilisable:
            if u[0]==obj:
                acf=True
                if u[1]=="dévérouille":
                    if 'verouille' in self.etat:
                        del(self.etat[self.etat.index('verouille')])
                elif u[1]=='traduire':
                    if 'traduisable' in obj.etat:
                        print("Vous remarquez, à votre plus grande stupeur que vous êtes maintenant capable de comprendre ce qui est écrit.")
                        for a in obj.actions:
                            if a[1]=='lire': del(obj.actions[obj.actions.index(a)])
                        obj.actions.append(['lire',obj.traduction])
        return acf             
    def action2(self,act):
        for a in self.actions:
            if act == a[0]:
                if a[0]=="casser":
                    if "cassable" in self.etats:
                        self.etat.append("cassé")
                    else:
                        print("Ce n'est pas bien de vouloir tout casser!")
                elif a[0] == "lire" :
                    print("Vous lisez : "+a[1])
    def parle(self,aa):
        for p in self.parler:
            if aa == p[0]:
                print(self.nom+" dit : "+p[1])

class Perso:
    def __init__(self):
        self.tipe='perso'
        self.nom=''
        self.description=None
        self.inventaire=[]
        self.jeufini=False
        self.vie=1
        self.att=1
        self.lieu_actu=Lieu()

def rol(no,lieu,perso):
    for o in lieu.objs+perso.inventaire:
        if no==o.nom or no in o.autre_noms:
            return o
    return None

aide="""
AIDE :
    
Ceci est un jeu textuel, pour y jouer vous devez taper des commandes.
Voici les differents types de commandes:
    -aller vers le nord : h,haut
    -aller vers le sud : s,sud
    -aller vers la gauche : g,gauche
    -aller vers la droite : d,droite
    -aller vers le haut : h,haut
    -aller vers le bas : b,bas
    -examiner un objet : x objet , examiner objet
    -prendre un objet : prendre objet
    -fouiller un objet : fouiller objet
    -voir son inventaire : i,inventaire
    -dire qqch a qqn : dire qqn qqch
    -voir là où vous êtes : v,voir
    -regarder qqch : r qqch , regarder qqch
    -utiliser qqch sur qqch : u qchh sur qqch, utiliser qqch qqch
    -parler de qqch a qqn : parler qqn qqch , dire qqn qqch
    -quitter la partie : q,quitter
    -sauvegarder : save , sauvegarder
    -charger : load , charger
    -donner qqch à qqn : donner dqch qqn
    -poser qqch : poser qqch , jeter qqch
    -deverouiller qqch(ou lieu) avec qqch : ouvrir qqch avec qqch , deverouiller lieu avec qqch
    -voler qqn : voler qqn , piquer qqn
    -aide : aide , help

Pour gagner la partie , il vous faudra prendre un objet.
"""
print(aide)


def commande(coms,perso,lieu_actu,eee):
    com_nord=['se déplacer vers le nord','aller nord','nord','n']
    com_sud=['se déplacer vers le sud','aller sud','sud','s']
    com_est=["se déplacer vers l'est",'aller est','est','e']
    com_bas=["aller bas","bas","b"]
    com_haut=["aller haut","haut","h"]
    com_ouest=['aller ouest','ouest','o']
    com_examiner=['examiner','x']
    com_fouiller=['fouiller','ouvrir']
    com_prendre=['prendre']
    com_inventaire=['inventaire','i']
    com_dire=['dire','crier']
    com_voir=["voir","v"]
    com_regarder=["regarder","r",'look']
    com_utiliser=["utiliser","u"]
    coms_parler=['parler','dire','discuter']
    com_quitter=['quitter','q','arreter']
    com_donner=["donner"]
    com_poser=['poser','jeter','lacher']
    com_deverouiller=['dévérouiller','déverouiller','deverouiller','ouvrir']
    com_voler=['voler','dérober','piquer']
    coms_save=['save','sauvegarder']
    coms_load=['load','charger']
    coms_aide=['aide','help','guide']
    com=coms[0]
    if com in com_quitter: exit()
    elif com in coms_save: print("Vous sauvegardez votre partie.")
    elif com in coms_load: print("Vous chargez votre partie.")
    elif com in coms_aide:
        print(aide)            
    elif com in com_nord:
        if lieu_actu.nord!=None:
            if 'vérouillé' in lieu_actu.nord.etat:
                print("Vous ne pouvez pas aller par là, c'est vérouillé.")
            else:
                lieu_actu=lieu_actu.nord
                print("Vous allez vers le Nord.")
        else:
            print(" Vous ne pouvez pas aller par là.")
    elif com in com_sud:
        if lieu_actu.sud!=None:
            if 'vérouillé' in lieu_actu.sud.etat:
                print("Vous ne pouvez pas aller par là, c'est vérouillé.")
            else:
                lieu_actu=lieu_actu.sud
                print("Vous allez vers le Sud.")
        else:
            print(" Vous ne pouvez pas aller par là.")
    elif com in com_est:
        if lieu_actu.est!=None:
            if 'vérouillé' in lieu_actu.est.etat:
                print("Vous ne pouvez pas aller par là, c'est vérouillé.")
            else:
                lieu_actu=lieu_actu.est
                print("Vous allez vers l'Est.")
        else:
            print(" Vous ne pouvez pas aller par là.")
    elif com in com_ouest:
        if lieu_actu.ouest!=None:
            if 'vérouillé' in lieu_actu.ouest.etat:
                print("Vous ne pouvez pas aller par là, c'est vérouillé.")
            else:
                lieu_actu=lieu_actu.ouest
                print("Vous allez vers l'Ouest.")
        else:
            print(" Vous ne pouvez pas aller par là.")
    elif com in com_bas:
        if lieu_actu.bas!=None:
            if 'vérouillé' in lieu_actu.bas.etat:
                print("Vous ne pouvez pas aller par là, c'est vérouillé.")
            else:
                lieu_actu=lieu_actu.bas
                print("Vous allez vers le Bas.")
        else:
            print(" Vous ne pouvez pas aller par là.")
    elif com in com_haut:
        if lieu_actu.haut!=None:
            if 'vérouillé' in lieu_actu.haut.etat:
                print("Vous ne pouvez pas aller par là, c'est vérouillé.")
            else:
                lieu_actu=lieu_actu.haut
                print("Vous allez vers le haut.")
        else:
            print(" Vous ne pouvez pas aller par là.")
    elif com in com_voler:
        if len(coms) >= 2:
            oo=rol(coms[1],lieu_actu,perso)
            if oo != None:
                if not 'non volable' in oo.etat and 'humain' in oo.etat and len(oo.objs) > 0:
                    ob=oo.objs[0]
                    perso.inventaire.append(ob)
                    del(oo.objs[0])
                    print("Vous volez à "+oo.nom+" "+ob.nom+".")
                else: print("Vous ne pouvez pas voler "+oo.nom)
            else: print("Je ne vois pas très bien ce que vous voulez voler.")
    elif com in com_deverouiller:
        if len(coms) >= 3:
            oa=None
            if lieu_actu.nord != None and lieu_actu.nord.nom==coms[1]:
                oa=lieu_actu.nord
            elif lieu_actu.sud != None and lieu_actu.sud.nom==coms[1]:
                oa=lieu_actu.sud
            elif lieu_actu.ouest != None and lieu_actu.ouest.nom==coms[1]:
                oa=lieu_actu.ouest
            elif lieu_actu.est != None and lieu_actu.est.nom==coms[1]:
                oa=lieu_actu.est
            elif lieu_actu.haut != None and lieu_actu.haut.nom==coms[1]:
                oa=lieu_actu.haut
            elif lieu_actu.bas != None and lieu_actu.bas.nom==coms[1]:
                oa=lieu_actu.bas
            if oa!=None:
                oo=None
                if len(coms)==3:
                    oo=rol(coms[2],lieu_actu,perso)
                elif len(coms)==4:
                    oo=rol(coms[3],lieu_actu,perso)
                if oo!= None:
                    if 'vérouillé' in oa.etat:
                        if oo in oa.deverouille:
                            print('Vous dévérouillez '+oa.nom)
                            del(oa.etat[oa.etat.index('vérouillé')])
                        else: print("Vous ne pouvez pas dévérouiller "+oa.nom+" avec "+oo.nom)
                    else:print(oa.nom+" n'est pas vérouillé.")
                else: print("Je ne vois pas avec quoi vous voulez dévérouiller "+oa.nom)
            else: print(" Je ne vois pas ce que vous voulez dévérouiller.")
    elif com in com_donner:
      if len(coms) >= 3:
        od=rol(coms[1],lieu_actu,perso)
        if od != None and (not 'décors' in od.etat) and (not 'fixé' in od.etat) and (not 'caché' in od.etat):
            odd=None
            if len(coms)>=4 and (coms[2] == 'à' or coms[2] == 'a'):
                odd=rol(coms[3],lieu_actu,perso)
            else:
                odd=rol(coms[2],lieu_actu,perso)
            if odd!=None:
                print("Vous donner "+od.nom+" à "+odd.nom)
                odd.objs.append(od)
                if od in lieu_actu.objs:
                    del(lieu_actu.objs[lieu_actu.objs.index(od)])
                elif od in perso.inventaire:
                    del(perso.inventaire[perso.inventaire.index(od)])
            else: print("Je ne vois pas très bien avec qui vous voulez donner cela.")
        else: print("Vous ne pouvez pas  donner cela.")
    elif com in com_poser:
        for o in perso.inventaire:
            if o.nom == coms[1] or coms[1] in o.autre_noms:
                print("Vous posez "+o.nom)
                lieu_actu.objs.append(o)
                del(perso.inventaire[perso.inventaire.index(o)])
                break
    elif com in com_inventaire:
        print("voici votre inventaire :")
        for i in perso.inventaire:
            print("  - "+i.nom)
    elif com in com_prendre:
        if len(coms)>1:
            oo=rol(coms[1],lieu_actu,perso)
            if oo != None:
                if (not('humain' in oo.etat)) and (not("fixé" in oo.etat)) and (not("décors" in oo.etat)):
                    print("Vous prenez "+oo.nom)
                    perso.inventaire.append(oo)
                    del(lieu_actu.objs[lieu_actu.objs.index(oo)])
            else: print("Vous ne pouvez pas prendre cet objet.")            
        else: print("Pouvez vous être plus précis ?")
    elif com in com_examiner:
        if len(coms) > 1:
            oo=rol(coms[1],lieu_actu,perso)
            if oo!= None and (not "caché" in oo.etat):
                if oo.examination=="": print(oo.description)
                else: print(oo.examination)
            else: print("Vous ne pouvez pas examiner cet objet")
        else: print("Pouvez vous être plus précis ?")
    elif com in com_fouiller:
        if len(coms)>1:
            oo=rol(coms[1],lieu_actu,perso)
            if oo != None  and (not "caché" in oo.etat):
                if oo.fouille!=[]:
                    for f in oo.fouille:
                        print("Vous découvrez "+f.nom)
                        lieu_actu.objs.append(f)
                        del(oo.fouille[oo.fouille.index(f)])
                else: print("Vous fouillez cet objet sans grand succès.")
            else: print(" Vous ne pouvez pas fouiller cet objet")
        else: print("Pouvez vous être plus précis ?")
    elif com in com_voir:
        print("Vous êtes dans "+lieu_actu.nom)
        print("-----------------------------")
        print(lieu_actu.description)
    elif com in com_regarder:
        if len(coms) > 1:
            oo=rol(coms[1],lieu_actu,perso)       
            if oo != None:
                print(oo.description)
            else: print("Vous ne pouvez pas regarder cet objet.")
        else: print("Pouvez vous être plus préci ?")
    elif com in com_utiliser:
        if len(coms)==4:
            o1=rol(coms[1],lieu_actu,perso)
            o2=rol(coms[3],lieu_actu,perso)
            if o1!=None and o2!=None:
                a=o1.action(o2)
                if not a:
                    o2.actions(o1)
            else: print("Ca ne marche pas.")
        else:
            print("Vous ne pouvez pas faire ça")
            print("Si vous voulez utiliser un objet sur un autre objet, utilisez la commande : utiliser obj1 sur obj2")
    elif com in coms_parler:
        if len(coms)==2 or (len(coms)==3 and coms[1]=="avec"):
            oo=rol(coms[len(coms)-1],lieu_actu,perso)
            if oo != None and oo.parler != []:
                oo.parle('')
            else: print("Je ne vois pas très bien avc qui vous voulez parler.")
        elif len(coms)>=3 and coms[1] != 'avec':
            oo=rol(coms[1],lieu_actu,perso)
            if oo != None and oo.parler != []:
                txt=""
                for c in coms[2:]:
                    if c != coms[2:][0]:txt+=c
                    else: txt+=c
                oo.parle(txt)
            else: print("Je ne vois pas très bien avec qui vous voulez parler.")
        elif len(coms)>=4 and coms[1] == 'avec':
            oo=rol(coms[2],lieu_actu,perso)
            if oo != None and oo.parler != []:
                txt=""
                for c in coms[3:]:
                    if c != coms[3:][0]:txt+=c
                    else: txt+=c
                oo.parle(txt)
            else: print("Je ne vois pas très bien avec qui vous voulez parler.")
    
    elif len(coms) >= 2:
        oo=rol(coms[1],lieu_actu,perso)
        if oo != None:
            oo.action2(com)
        else: print("Vous ne pouvez pas faire ça.")
    else:
        print("Je n'ai pas compris.")
    if eee: inp("")
    return lieu_actu,perso

def aff(lieu_actu,perso):
    print(' ')
    print("Vous êtes dans "+lieu_actu.nom)
    print("-------------")
    if not lieu_actu.deja_ete:
        print(lieu_actu.description)
        lieu_actu.deja_ete=True
    print(' ')
    for o in lieu_actu.objs:
        if not 'caché' in o.etat and not 'cassé' in o.etat and not 'mort' in o.etat:
            print("vous pouvez voir "+o.nom)   
    print(' ')
    if lieu_actu.nord != None and not 'caché' in lieu_actu.nord.etat: print(lieu_actu.nord.nom+" se trouve au nord.")
    if lieu_actu.est != None and not 'caché' in lieu_actu.est.etat: print(lieu_actu.est.nom+" se trouve à l'est.")
    if lieu_actu.sud != None and not 'caché' in lieu_actu.sud.etat: print(lieu_actu.sud.nom+" se trouve au sud.")
    if lieu_actu.ouest != None and not 'caché' in lieu_actu.ouest.etat: print(lieu_actu.ouest.nom+" se trouve à l'ouest.")
    if lieu_actu.bas != None and not "caché" in lieu_actu.bas.etat: print(lieu_actu.bas.nom+" se trouve vers le bas.")
    if lieu_actu.haut != None and not "caché" in lieu_actu.haut.etat: print(lieu_actu.haut.nom+" se trouve vers le haut.")
    print(' ')
    for e in lieu_actu.evenements:
        if not e.deja_fait:
            if e.act:
                e.action(lieu_actu,perso)
            
def main(perso,ef):
    perso.hc=[] #historique commandes
    while not perso.jeufini:
        aff(perso.lieu_actu,perso)
        com=inp("--> ")
        coms=com.split()
        if len(coms) >= 1:
            perso.lieu_actu,perso=commande(coms,perso,perso.lieu_actu,True)
            perso.hc.append(com)
        com_save=['save','sauveguarder']
        com_load=['load','charger']
        if com in com_save:
            txt=''
            for h in perso.hc:
                txt+=h
                if perso.hc.index(h)<len(perso.hc)-1:txt+=" \n"
            f=open("save","w")
            f.write(txt)
            f.close()
        elif com in com_load:
            if "save" in os.listdir("./"):
                ch=open("save",'r').readlines()
                perso.hc=[]
                for c in ch:
                    try:
                        perso.lieu_actu,perso=commande(c.split(),perso,perso.lieu_actu,False)
                        perso.hc.append(c)
                    except: pass
            else: print("vous ne pouvez pas charger votre partie.")
        if ef in perso.inventaire:
            perso.jeufini=True
            break



