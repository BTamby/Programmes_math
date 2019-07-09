#!/usr/bin/env python
# coding: utf-8
import os, sys
################################################################################
def inserer_codejs(prog_edite):
	txt = '!if $jquery_defined=yes'+'\n\
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
	return txt

def begin_html():

	# Enregistrer les infos générales dans un dictionnaire
	dico={'titreniveau':'','dateprogramme':'','lienprogramme':'','datewims':'','level':'','ressources':''}
	for cle in dico:
		tag = tag='@'+cle
		f=open(path_fichier_txt,'r')
		continuer = True
		while continuer :
			lign = f.readline()
			liste = lign.split(':')
			test_tag = lign.split(':')[0]
			if test_tag == tag or lign == '':
				continuer = False
		#print('Le tag ',tag,' et la li ',liste)
		index_2pt = lign.index(':')
		info_lu = lign[index_2pt+1:-1]
		#print("info_lu = ",info_lu)
		dico[cle]=info_lu
	# Construire la partie de présentation générale du progrmme.
	txt ='!set email=$responsable_math_1G<br/>\n<h2 class="wims_title">'+dico['titreniveau']+'</h2>\n<h3 class="wims_title">\n\t<a href='+'"'+dico['lienprogramme']+'" target="wims_external">\n\t\t'+dico['dateprogramme']+'\n\t</a>\n</h3>\n\
<div class="wims_msg info program_desc">\n\t'+\
dico['datewims']+'\n\
</div>\n<div id ="intro" class ="accordion">\n<h3>Préambule</h3>\n<div id="preambule">'
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

def creer_les_titres():

	for them in dico_all :
		flux = open(path_fichier_txt)
		les_titres =[]
		tag ='@theme'
		continuer = True
		#Avancer au prochain tag @theme
		while continuer :
			lign = flux.readline()
			test_tag = lign.split(':')[0]
			if test_tag == tag and lign[len(tag)+1:-1] == them:
				continuer = False
		continuer = True
		#theme = lign[len(tag)+1:-1]
		while continuer :
			lign = flux.readline()
			test_tag = lign.split(':')[0]
			if test_tag == tag or lign =='':
				continuer = False
			else :
				if test_tag == '@titre':
					les_titres.append(lign[len('@titre')+1:-1])
		dico_all[them]['titres']=les_titres
		#print("Les titres :",les_titres)
		flux.close()
def creer_les_contenus():
	for them in dico_all :
		flux = open(path_fichier_txt)
		les_contenus = []
		tag ='@theme'
		continuer = True
		#Avancer au prochain tag @theme
		while continuer :
			lign = flux.readline()
			test_tag = lign.split(':')[0]
			if test_tag == tag and lign[len(tag)+1:-1] == them:
				continuer = False
		continuer = True
		#theme = lign[len(tag)+1:-1]
		while continuer :
			lign = flux.readline()
			test_tag = lign.split(':')[0]
			if test_tag == tag or lign =='':
				continuer = False
			else :
				if test_tag == '@contenu':
					txt = lign[len('@contenu')+1:-1]
					lign = flux.readline()
					while lign[0] != '@':
						txt=txt+lign
						lign = flux.readline()

					les_contenus.append(txt)
		dico_all[them]['contenu']=les_contenus
		#print("Les titres :",les_titres)
		flux.close()

def creer_les_themes():
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
			#Ajouter objectif et histoire dans le dictionnaire
			creer_presentation(flux,nom)
		if tag == tag_fin :
			continuer = False
	flux.close()
def creer_presentation(flux,them):
	txt_objectif = ''
	lign = flux.readline()
	texte = lign[len('@objectif')+1:-1]
	txt_objectif = txt_objectif+texte
	test_tag = '@histoire'
	lign = flux.readline()
	while lign.split(':')[0] != test_tag :
		txt_objectif = txt_objectif + lign
		lign = flux.readline()
	dico_all[them]['objectif']=txt_objectif
	txt_histoire = lign[len(test_tag)+1:-1]
	lign = flux.readline()
	end_realine = '@titre'
	while lign.split(':')[0] != end_realine :
		txt_histoire = txt_histoire +lign
		lign =flux.readline()
	#print("Dernière ligne de présentation : ",lign)
	dico_all[them]['histoire']=txt_histoire


####################################
work_directory = os.getcwd()
dossier_matiere = work_directory+'/math/'
fichier_txt ='math.1G_test'
path_fichier_txt = dossier_matiere+fichier_txt
allhtml = ''
program_adress ='/home/wims/public_html/modules/help/teacher/program.fr/fr/'
out_phtml =open(program_adress+fichier_txt+'.phtml','w',encoding='Windows 1252')
txt_html = begin_html()
allhtml = allhtml + txt_html
dico_all = {}
#Creer le contenu de chaque thème
creer_les_themes()
creer_les_titres()
creer_les_contenus()
#print("Les thèmes : ", les_themes)
for them in dico_all :
	print(them,' : ',dico_all[them])
#Insérer le menu dans  le fichier .phtml
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
for cle,val in dico_all.items():
	begin_div = '\t<div id="c_'+str(i)+'"><!--Begin thème '+cle+'-->\n\t\
	<h3 class="program_theme">'+cle+'</h3>\n'
	allhtml = allhtml+begin_div
	#objectif = creer_objectif(them)
	begin_div_objectif = '\t\t<div class="accordion">\n\t\t\t<h4>Objectifs</h4>\n\t\t\t<div>\n'
	allhtml = allhtml+begin_div_objectif
	allhtml = allhtml+val['objectif']
	end_div_objectif = '\t\t\t</div>\n\t\t</div><!--Fin objectifs-->\n'
	allhtml = allhtml + end_div_objectif

	begin_div_histoire = '\t\t<div class="accordion">\n\t\t\t<h4>Histoire des mathématiques</h4>\n\t\t\t<div>\n'
	allhtml = allhtml+begin_div_histoire
	allhtml = allhtml+val['histoire']
	end_div_histoire = '\t\t\t</div>\n\t\t</div><!--Fin histoire des maths-->\n'
	allhtml = allhtml + end_div_histoire
	
	
	allhtml = allhtml +'\t<h4>Sommaire du thème '+cle+'</h4><!-- Sommaire-->\n'
	allhtml = allhtml+'<ul class="program_submenu">\n\t'
	for num,t in enumerate(dico_all[cle]['titres']):
		allhtml = allhtml+'<li><a href="#t_'+str(i)+str(num)+'">'+t+'</a></li>\n\t'
	allhtml = allhtml+'\n</ul>\n'
	#Contenus, capacités, commentaires
	for num,val in enumerate(dico_all[cle]['contenu']):
		begin_div_bloc = '<div id = "t_'+str(i)+str(num)+'">\n'
		allhtml = allhtml +begin_div_bloc+'<h4 class="program_titre">'+dico_all[cle]['titres'][num]+'</h4>\n'
		allhtml = allhtml +'<div class = "small-4">\n'
		allhtml = allhtml +val
		allhtml = allhtml + '</div><!-- Fin class small-->\n'
		end_div_bloc ='</div><!-- Fin du bloc -->\n'
		allhtml = allhtml + end_div_bloc
	#Fin du thème
	end_div='\t</div><!--End thème '+cle+'-->\n'
	allhtml = allhtml + end_div
	i += 1
#Créer le sommaire

# Fin du fichier phtml
allhtml = allhtml+'</div><!-- id = widget_'+fichier_txt.replace('.','')+'-->'
# Création du nom du fichier à mettre dans var proc
nom_du_prog=fichier_txt.replace('.','')
allhtml = allhtml+'\n'+inserer_codejs(nom_du_prog)
#Ecriture du contenu dans le fichier de sorite .phtml
out_phtml.write(allhtml)
out_phtml.close()

# Ouvrir le fichier de sortie phtml en écriture
#creer_un_programme(fichier_txt)

