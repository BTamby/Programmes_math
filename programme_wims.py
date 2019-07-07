#!/usr/bin/env python
# coding: utf-8
import os, sys

def inserer_codejs(prog_edite):
	texte = '!if $jquery_defined=yes'+'\n\
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
	return texte

def info_entete(f_txt,dico):
	"""Création du dictionnaire d'informations qui constituent l'entête du fichier html du programme créé. """
	for cle in dico:
		tag = tag='@'+cle
		f=open(f_txt,'r')
		continuer = True
		while continuer :
			lign = f.readline()
			liste = lign.split(':')
			test_tag = lign.split(':')[0]
			if test_tag == tag or lign == '':
				continuer = False
		f.close()
		#print('Le tag ',tag,' et la li ',liste)
		index_2pt = lign.index(':')
		info_lu = lign[index_2pt+1:-1]
		#print("info_lu = ",info_lu)
		dico[cle]=info_lu

def begin_html(dico):
	"""Début du fichier html avec les informations générales"""
	texte='<h2 class="wims_title">'+dico['titreniveau']+'</h2>\n<h3 class="wims_title">\n\t<a href='+'"'+dico['lienprogramme']+'" target="wims_external">\n\t\t'+dico['dateprogramme']+'\n\t</a>\n</h3>\n\
<div class="wims_msg info program_desc">\n\t'+\
dico['datewims']+'\n\
</div>\n<div>\n'
	return texte

def creer_intro(f_txt):
	tag ='@intro'
	texte = ''
	continuer = True
	f=open(f_txt,'r')
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
			texte = texte + lign
	#print("Intro = \n",texte)
	f.close()
	return texte

def ressource_euler(dico):
	texte = '<div class="wimscenter">\n\t\
<a class ="external_link" href="'+dico['ressources']+'" target="wims_external" title="Ressources complémentaires sur le site Euler">\
	\n\t\tRessources complémentaires\n\t</a>\n</div>\n\t</div>\n'
	return texte
def mise_a_jour_themes(path_fichier,fichier):
	flux = open(path_fichier)
	tag_theme = '@theme'
	tag_fin = '@end'
	continuer = True
	liste_themes = []
	while continuer:
		lign = flux.readline()
		tag= lign.split(':')[0]
		if tag == tag_theme :
			nom =lign[len(tag)+1:-1]
			liste_themes.append(nom)
			#print("Theme : ",nom)
		if tag == tag_fin :
			continuer = False
	flux.close()
	return liste_themes
def creer_menu(l_theme):
	texte = '\n\t<ul class="wims_summary">\n'
	for i,e in enumerate(l_theme) :
		texte = texte +'\t\t<li><a href="#c_'+str(i)+'">'+e+'</a></li>\n'
	texte = texte + '\t</ul>\n'
	return texte
def creer_objectif(path_fichier,them):
	text =''
	f = open(path_fichier,'r')
	continuer = True
	while continuer :
		ligne =f.readline()
		first_word = ligne.split(':')[0]
		if first_word == '@theme' :
			theme_lu = ligne[len(first_word)+1:-1]
			if theme_lu == them :
				print("On est dans le thème : ",theme_lu)
				objectif = ''
				lign = f.readline()
				text = lign[len('@objectif')+1:-1]
				objectif = objectif+text
				test_tag = '@histoire'
				lign = f.readline()
				while lign.split(':')[0] != test_tag :
					objectif = objectif + lign
					lign = f.readline()
				continuer = False
	f.close()
	print("Objectif = ",objectif)
	return objectif

def creer_un_programme(path_fichier,fichier):
	#Dictionnaire contenant les informations de l'entête
	elements_info={'titreniveau':'','dateprogramme':'','lienprogramme':'','datewims':'','level':'','ressources':''}
	program_adress ='/home/wims/public_html/modules/help/teacher/program.fr/fr/'
	out_phtml =open(program_adress+fichier+'.phtml','w',encoding='Windows 1252')
	#Mise à jour du dictionnaire d'informations générales pour l'entête
	info_entete(path_fichier,elements_info)
	#Entête du fichier html
	content=begin_html(elements_info)
	#Création de l'introduction
	content=content+creer_intro(path_fichier)
	#Insertion lien vers ressources complémentaires sur le site Euler
	content=content+ressource_euler(elements_info)
	#Enregistrement des noms des thèmes dans une liste
	themes = mise_a_jour_themes(path_fichier,fichier)
	allmenu = creer_menu(themes)
	alltext = '<div id="widget_'+fichier.replace('.','')+'">'+allmenu+'\n'
	fin_alltext='</div><!--Fin de widget_'+fichier.replace('.','')+'-->\n'
	content=content+alltext
	#Pour chaque thème créer le bloc contenu
	for ind,them in enumerate(themes) :
		begin_div = '\t<div id="c_'+str(ind)+'"><!--Begin thème '+them+'-->\n\t\
	<h3 class="program_theme">'+them+'</h3>\n'
		content = content+begin_div
		objectif = creer_objectif(path_fichier,them)
		begin_div_objectif = '\t\t<div class="accordion">\n\t\t\t<h4>Objectifs</h4>\n\t\t\t<div>\n'
		content = content+begin_div_objectif
		content = content+objectif
		end_div_objectif = '\t\t\t</div>\n\t\t</div><!--Fin présentation-->\n'
		content = content + end_div_objectif
		end_div='\t</div><!--End thème '+them+'-->\n'
		content = content + end_div
	content=content+fin_alltext

	code_prog=fichier.replace('.','')
	content =content+'\n'+inserer_codejs(code_prog)
	#Ecriture du contenu dans le fichier de sorite .phtml
	out_phtml.write(content)
	out_phtml.close()



work_directory = os.getcwd()
dossier_matiere = work_directory+'/math/'
fichier_txt ='math.test'
path_fichier_txt = dossier_matiere+fichier_txt
creer_un_programme(path_fichier_txt,fichier_txt)
