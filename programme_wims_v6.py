#!/usr/bin/env python
# coding: utf-8
import os, sys
################################################################################


def inserer_codejs(prog_edite):
	"""Insère à la fin du fichier le script js pour les boutons-accordéons"""
	code = '!if $jquery_defined=yes'+'\n\
		<script>\n'+'\
			jQuery(function($$){'+'\n'+'\
				$$(".accordion").accordion({'+'\n'+'\
					collapsible: true,\n'+'\
					active: false,\n'+'\
				});\n'+'\
			} );\n'+'\
		</script>\n'+'\
		!read tabscript '+ prog_edite+'\n'+\
'!endif\n'+'\
!tail'
	return code
def begin_html():
	# Enregistrer les infos générales dans un dictionnaire
	info_gen={'titreniveau':'','dateprogramme':'','lienprogramme':'','datewims':'','level':'','ressources':''}
	for cle in info_gen:
		tag = tag='@'+cle
		f=open(path_fichier_txt,'r')
		continuer = True
		while continuer :
			lign = f.readline()
			liste = lign.split(':')
			test_tag = lign.split(':')[0]
			if test_tag == tag or lign == '':
				continuer = False
		#print('Le tag ',tag,' et la liste ',liste)
		index_2pt = lign.index(':')
		info_lu = lign[index_2pt+1:-1]
		#print("info_lu = ",info_lu)
		info_gen[cle]=info_lu
	# Le css à déporter
	style_css ="""<style>\n\
	ul.bullets >li{
		color:blue;
	}
	ul.tirets {
       list-style: none; /* Remove HTML bullets */
       padding: 0;
       margin: 0;
       }
       ul.tirets li {
       padding-left: 1em;
       }
       ul.tirets li::before {
       content: "\\2014"; /* Insérer tiret*/
       padding-right: 0.5em;
       color: blue;
       }
	.titre_colonne{color: #c52d2d; text-align: center;}
	.program_h4{color : blue;}
	.program_colonne{
    display: block;
    background-color: #fff;
    margin: 0;
    padding: 0.5em;
    clear: both;
    border-top-color: $wims_ref_bgcolor;
    border-top-width: 5px;
    border-top-style: solid;
    border-right-color: rgb(187, 187, 187);
    border-right-style: solid;
    border-right-width: 1px;
    border-left-color: rgb(187, 187, 187);
    border-left-style: solid;
    border-left-width: 1px;
    border-image-outset: 0;
    border-image-repeat: stretch;
    border-image-slice: 100%;
    border-image-source: none;
    border-image-width: 1;
    border-radius: 10px 10px 5px 5px;
    min-height: 6em;
    box-sizing: border-box;
}\n</style>\n"""
	Fichier = path_fichier_txt.split('/')[-1]
	Fichier = Fichier.replace('.','_')
	txt =style_css+'!set email=$responsable_'+Fichier+'\n<h2 class="wims_title">'+info_gen['titreniveau']+'</h2>\n<h3 class="wims_title">\n\t<a href='+'"'+info_gen['lienprogramme']+'" target="wims_external">\n\t\t'+info_gen['dateprogramme']+'\n\t</a>\n</h3>\n\
<div class="wims_msg info program_desc">\n\t'+\
info_gen['datewims']+'\n\
</div>\n<div id ="intro" class ="accordion">\n<h3>Préambule</h3>\n<div id="preambule">\n'
	# Construire l'ntroduction du programme créé
	tag ='@intro'
	continuer = True
	#Avancer au tag @intro
	while continuer :
		lign = f.readline()
		test_tag = lign.split(':')[0]
		if test_tag == tag :
			continuer = False
	continuer = True
	while continuer:
		lign = f.readline()
		#print("Ligne lue =")
		test_tag_suiv = lign[0]
		if test_tag_suiv == '@' or lign =='':
			continuer = False
		else :
			txt = txt + lign
	f.close()
	return txt+'\n</div><!-- Fin accordion -->\n</div><!-- Fin du préambule-->\n'

def creer_elements(elt):
	global dico_all
	tag_elt ='@'+elt
	for them in dico_all :
		flux = open(path_fichier_txt)
		les_elts = []
		tag ='@theme'
		continuer = True
		#Avancer au prochain tag @theme
		while continuer :
			lign = flux.readline()
			test_tag = lign.split(':')[0]
			if test_tag == tag and lign[len(tag)+1:-1] == them:
				continuer = False
		continuer = True
		while continuer :
			lign = flux.readline()
			test_tag = lign.split(':')[0]
			if test_tag == tag or lign =='':
				continuer = False
			else :
				if test_tag == tag_elt:
					txt = lign[len(tag_elt)+1:-1]
					lign = flux.readline()
					while lign[0] != '@':
						txt=txt+lign
						lign = flux.readline()
					les_elts.append(txt)
		dico_all[them][elt]=les_elts
		flux.close()

def creer_les_themes():
	global dico_all
	flux = open(path_fichier_txt)
	tag_test = '@theme'
	tag_fin = '@end'
	continuer = True
	themes = []
	while continuer:
		lign = flux.readline()
		tag= lign.split(':')[0]
		if tag == tag_test :
			nom =lign[len(tag)+1:-1]
			themes.append(nom)
			dico_all[nom]={}
		if tag == tag_fin :
			continuer = False
	flux.close()

def creer_lien_exo(ex):
	lien = ''
	split_ex = ex.split(',')
	if len(split_ex) > 1:
		mod=split_ex[0]
		exo=split_ex[1]
		titre_mod=split_ex[2]
		extra0=split_ex[3]
		if exo != '':
			extra = extra0+"&+cmd=new"
			nom = mod+"&exo"
		else :
			extra =extr0+"&+cmd=intro"
		picto=split_ex[4]
		if picto != '':
			picto = "\n!set wims_ref_class=text_icon icon_"+picto
		desc=split_ex[5]
		if desc != '':
			desc = "\n!set wims_ref_title="+desc
		lien = "<li>"+picto+desc+"\n!href target=wims_exo module="+mod+"&exo="+exo+extra+" "+titre_mod+"\n</li>"
	else :
		print("Pas d'exercices")
	return lien

def creer_liste_exo(them,pt_de_prog,ex):
	global nom_fichier
	l_exo = ex.split('\n')
	#fichier_phtml = nom_fichier[them]
	#flux = open(fichier_phtml,'a',encoding='Windows 1252')
	#flux.write('Point de programme : '+pt_de_prog+'\n')
	les_liens = []
	for e in l_exo :
		lien = creer_lien_exo(e)
		#flux.write(lien+'\n')
		les_liens.append(lien)
	#flux.close()
	return les_liens

def creer_program(prog):
	global dico_all,nom_fichier
	dico_all = {}
	out_phtml =open(prog,'w',encoding='Windows 1252')
	allhtml = begin_html()
	ens_tag = ['objectif','histoire','titre','contenu','capacite','commentaire','presentation','wims']
	#Creer le contenu de chaque thème
	creer_les_themes()
	for tag_cur in ens_tag :
		creer_elements(tag_cur)
	allhtml=allhtml+'<div id="widget_'+fichier_txt.replace('.','')+'"><!-- Début de id = widget_'+fichier_txt.replace('.','')+'-->'
	allhtml = allhtml+'\n\t<ul class="wims_summary"><!-- Début du menu -->\n'
	i = 0
	for cle,val in dico_all.items() :
		allhtml = allhtml +'\t\t<li><a href="#c_'+str(i)+'">'+cle+'</a></li>\n'
		i += 1
	allhtml = allhtml+'\t</ul><!-- Fin du menu -->\n'
	# Insérer le contenu de chaque thème :
	# D'abord les les objectifs et les histoires
	i = 0
	"""nom_fichier = {'Algèbre':'algebre.phtml','Analyse':'analyse.phtml','Géométrie':'geometrie.phtml',\
	'Probabilités et statistiques':'proba_stat.phtml','Algorithmique et programmation':'algo_prog.phtml',\
	'Vocabulaire ensembliste et logique':'voc_ens_logique.phtml'}"""
	#Pour chaque thème, création du bloc des colonnes (1,2 ou 3)
	for cle,val in dico_all.items():
		# Création d'un fichier d'exercices pour chaque thème
		#f_phtml_them = open(nom_fichier[cle],'w',encoding='Windows 1252')
		#f_phtml_them.write('Exercices du thème '+cle+'\n')
		#f_phtml_them.close()
		#Début du code html du thème
		begin_div = '\t<div id="c_'+str(i)+'"><!--Begin thème '+cle+'-->\n\t\
		<h3 class="program_theme">'+cle+'</h3>\n'
		allhtml = allhtml+begin_div
		#objectif = creer_objectif(them)
		if val['objectif'] != ['']:
			begin_div_objectif = '\t\t<div class="accordion">\n\t\t\t<h4 class="program_h4">Objectifs</h4>\n\t\t\t<div>\n'
			allhtml = allhtml+begin_div_objectif
			allhtml = allhtml+val['objectif'][0]
			end_div_objectif = '\n\t\t\t</div><!--Fin objectifs-->\n\t\t</div><!--Fin accordion-->\n'
			allhtml = allhtml + end_div_objectif
		if val['histoire'] != ['']:
			begin_div_histoire = '\t\t<div class="accordion">\n\t\t\t<h4 class="program_h4">Histoire des mathématiques</h4>\n\t\t\t<div>\n'
			allhtml = allhtml+begin_div_histoire
			allhtml = allhtml+val['histoire'][0]
			end_div_histoire = '\n\t\t\t</div><!--Fin histoire des maths-->\n\t\t</div><!--Fin accordion-->\n'
			allhtml = allhtml + end_div_histoire
		#print("dico_all[cle]['titre'] = ",dico_all[cle]['titre'],"\n")
		if dico_all[cle]['titre'] != ['']:
			allhtml = allhtml +'\t<h4 class="program_h4">Sommaire</h4><!-- Sommaire-->\n'
			allhtml = allhtml+'<ul class="program_submenu">\n\t'
			for num,t in enumerate(dico_all[cle]['titre']):
				if t != '':
					allhtml = allhtml+'<li><a href="#t_'+str(i)+str(num)+'">'+t+'</a></li>\n\t'
			allhtml = allhtml+'\n</ul>\n'
		#Dans le cas où il y a 3 colonnes
		if dico_all[cle]['contenu'] != [''] and dico_all[cle]['capacite'] != [''] and dico_all[cle]['commentaire'] != ['']:
			#print("Il y a 3 colonnes dans le thème : ",cle)
			class_col = '"box_content2 small-4 medium-4 large-4 cell program_colonne"'

		for num,valeur in enumerate(dico_all[cle]['contenu']):
			# Titre du point de programme
			allhtml = allhtml+'<h4 class="program_h4">'+dico_all[cle]['titre'][num]+'</h4>\n'
			#Des compléments pour certains points de programme
			if dico_all[cle]['presentation'][num] != '' :
				allhtml = allhtml+dico_all[cle]['presentation'][num]
			# Début du bloc formé par les colonnes (3, 2 ou 1 ?)
			begin_div_bloc = '<div id = "t_'+str(i)+str(num)+'" class="grid-x grid-margin-x small-margin-collapse"><!-- Début bloc -->\n'
			allhtml = allhtml +begin_div_bloc
			#Création du bloc de colonnes
			#### TEST
			print("Thème = ", cle)
			print("Titre = ",dico_all[cle]['titre'][num])
			print("Colonne contenu = ",dico_all[cle]['contenu'][num], " type = ", type(dico_all[cle]['contenu'][num]))
			print("Colonne capacite = ",dico_all[cle]['capacite'][num]," type = ", type(dico_all[cle]['capacite'][num]))
			print("Colonne commentaire = ",dico_all[cle]['commentaire'][num]," type = ", type(dico_all[cle]['commentaire'][num]))
			#Il y a les trois colonnes
			if dico_all[cle]['contenu'][num] != [''] and dico_all[cle]['capacite'][num] != [''] and dico_all[cle]['commentaire'][num]!= '':
				print("Les trois colonnes du titre ",dico_all[cle]['titre'][num]," du thème ",cle," ne sont pas vides !\n")
				class_col = '"box_content2 small-4 medium-4 large-4 cell program_colonne"'
				bloc_col = '<div class='+class_col+'><!--Colonne contenu-->\n<h4 class="titre_colonne">Contenus</h4>\n'+\
				valeur+'</div><!-- Fin colonne contenu-->\n'+'<div class='+class_col+'><!--Colonne capacités-->\n<h4 class="titre_colonne">Capacités atendues</h4>\n'+\
				dico_all[cle]['capacite'][num]+'</div><!-- Fin colonne capacites-->\n'+'<div class='+class_col+'><!--Colonne commentaires-->\n<h4 class="titre_colonne">Démonstrations-Algorithmes-Approfondissements</h4>\n'+\
				dico_all[cle]['commentaire'][num]+'\n</div><!-- Fin colonne commentaires-->\n'
				allhtml = allhtml +bloc_col
			#Il y a une seule colonne : capacités attendues
			elif dico_all[cle]['contenu'][num] == '' and dico_all[cle]['capacite'][num] != '' and dico_all[cle]['commentaire'][num] == '':
				print("Les colonnes contenu et commentaire du titre ",dico_all[cle]['titre'][num]," du thème ",cle," sont vides !\n")
				class_col = '"box_content2 small-12 cell program_colonne"'
				bloc_col = '<div class='+class_col+'><!--Colonne capacités-->\n<h4 class="titre_colonne">Capacités atendues</h4>\n'+\
				dico_all[cle]['capacite'][num]+'</div><!-- Fin colonne capacites-->\n'
				allhtml = allhtml +bloc_col
			elif dico_all[cle]['contenu'][num] != '' and dico_all[cle]['capacite'][num] != '' and dico_all[cle]['commentaire'][num] == '':
				print("La colonne commentaire est vide !")
				class_col = '"box_content2 small-6 small-6 cell program_colonne"'
				bloc_col = '<div class='+class_col+'><!--Colonne contenu-->\n<h4 class="titre_colonne">Contenus</h4>\n'+\
				valeur+'</div><!-- Fin colonne contenu-->\n'+'<div class='+class_col+'><!--Colonne capacités-->\n<h4 class="titre_colonne">Capacités atendues</h4>\n'+\
				dico_all[cle]['capacite'][num]+'</div><!-- Fin colonne capacites-->\n'
				allhtml = allhtml +bloc_col
			# Insertion des exercices
			exercices = dico_all[cle]['wims'][num]
			liste_de_lien = []
			if len(exercices) != 0 :
				liste_de_lien = creer_liste_exo(cle,dico_all[cle]['titre'][num],exercices)
			allhtml = allhtml +'<div class="box_content2 small-12 cell program_colonne"><!-- Les exercices -->\
			\nInsérer ici les exercices du paragraphe '+ dico_all[cle]['titre'][num]+'\n<ul class=program_list>\n'
			for e in liste_de_lien :
				allhtml = allhtml+e+'\n'
			allhtml = allhtml+'</ul>\n</div><!-- Fin exercices -->\n'
			end_div_bloc ='</div><!-- Fin bloc -->\n'
			allhtml = allhtml + end_div_bloc
		#Fin du thème
		end_div='\t</div><!--End thème '+cle+'-->\n'
		allhtml = allhtml + end_div
		i += 1
	# Fin du fichier phtml
	allhtml = allhtml+'</div><!-- id = widget_'+fichier_txt.replace('.','')+'-->'
	# Création du nom du fichier à mettre dans var proc
	nom_du_prog=fichier_txt.replace('.','')
	allhtml = allhtml+'\n'+inserer_codejs(nom_du_prog)
	#Ecriture du contenu dans le fichier de sorite .phtml
	out_phtml.write(allhtml)
	out_phtml.close()

####################################


work_directory = os.getcwd()
dossier_matiere = work_directory+'/math/Lycee/'
for fichier_txt in os.listdir(dossier_matiere):
	path_fichier_txt = dossier_matiere+fichier_txt
	program_adress ='/home/wims/public_html/modules/help/teacher/program.fr/fr/'
	prog_niveau = program_adress+fichier_txt+'.phtml'
	creer_program(prog_niveau)


