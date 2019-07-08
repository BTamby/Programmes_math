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
			creer_presentation(flux,nom)
		if tag == tag_fin :
			continuer = False
	flux.close()
	#return themes

def creer_presentation(f,them):
	txt_objectif = ''
	lign = f.readline()
	texte = lign[len('@objectif')+1:-1]
	txt_objectif = txt_objectif+texte
	test_tag = '@histoire'
	lign = f.readline()
	while lign.split(':')[0] != test_tag :
		txt_objectif = txt_objectif + lign
		lign = f.readline()
	dico_all[them]['objectif']=txt_objectif
	txt_histoire = lign[len(test_tag)+1:-1]
	#print("Test = ",txt_histoire)
	lign = f.readline()
	end_realine = '@titre'
	while lign.split(':')[0] != end_realine :
		txt_histoire = txt_histoire +lign
		lign =f.readline()
	#print("Test = ",txt_histoire)
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
les_themes = creer_les_themes()
print("Les thèmes : ", les_themes)
print(dico_all)
# Création du nom du fichier à mettre dans var proc
nom_du_prog=fichier_txt.replace('.','')
allhtml = allhtml+'\n'+inserer_codejs(nom_du_prog)



#Ecriture du contenu dans le fichier de sorite .phtml
out_phtml.write(allhtml)
out_phtml.close()
# Ouvrir le fichier de sortie phtml en écriture
#creer_un_programme(fichier_txt)

