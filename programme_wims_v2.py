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
	# Construire la partie de présentation g>énérale du progrmme.
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
       content: "\\2014"; /* Insert content that looks like bullets */
       padding-right: 0.5em;
       color: blue; /* Or a color you prefer */
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
	txt =style_css+'!set email=$responsable_math_1G<br/>\n<h2 class="wims_title">'+dico['titreniveau']+'</h2>\n<h3 class="wims_title">\n\t<a href='+'"'+dico['lienprogramme']+'" target="wims_external">\n\t\t'+dico['dateprogramme']+'\n\t</a>\n</h3>\n\
<div class="wims_msg info program_desc">\n\t'+\
dico['datewims']+'\n\
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
		#if tag_elt == '@wims':
			#print("Thème : ",them," et exercices : ",les_elts)
		dico_all[them][elt]=les_elts
		#print("Les exercices du thème  ",them, " :",les_elts)
		flux.close()
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
	end_readline = '@titre'
	while lign.split(':')[0] != end_readline :
		txt_histoire = txt_histoire +lign
		lign =flux.readline()
	dico_all[them]['histoire']=txt_histoire
def creer_lien_exo(ex):
	lien = ''
	split_ex = ex.split(',')
	print("split_ex = ",split_ex)
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

		print("Module = ",mod)
		print("Nom de l'exercice = ",exo)
		print("Titre modifié de l'exercice = ",titre_mod)
		print("Extra url = ",extra0)
		print("Picto = ",picto)
		print("Description visible en tooltip = ",desc)
		lien = "<li>"+picto+desc+"\n!href target=wims_exo module="+mod+"&exo="+exo+extra+" "+titre_mod+"\n</li>"
		print("Le lien :\n",lien)
	else :
		print("Pas d'exercices")
	return lien

def creer_liste_exo(them,pt_de_prog,ex):
	print("Thème : ",them,"\nPoint de programme : ",pt_de_prog,"\nListe exercices : ",ex)
	l_exo = ex.split('\n')
	fichier_phtml = nom_fichier[them]
	flux = open(fichier_phtml,'a',encoding='Windows 1252')
	flux.write('Point de programme : '+pt_de_prog+'\n')
	print("Taille de l_exo : ", len(l_exo))
	les_liens = []
	for e in l_exo :
		lien = creer_lien_exo(e)
		flux.write(lien+'\n')
		les_liens.append(lien)
	flux.close()
	return les_liens
####################################
work_directory = os.getcwd()
dossier_matiere = work_directory+'/math/'
fichier_txt ='math.1G_test'
path_fichier_txt = dossier_matiere+fichier_txt
#allhtml = ''
program_adress ='/home/wims/public_html/modules/help/teacher/program.fr/fr/'
out_phtml =open(program_adress+fichier_txt+'.phtml','w',encoding='Windows 1252')
#txt_html = begin_html()
#allhtml = allhtml + txt_html
allhtml = begin_html()
dico_all = {}
#Creer le contenu de chaque thème
creer_les_themes()
creer_les_titres()
creer_elements('contenu')
creer_elements('capacite')
creer_elements('commentaire')
creer_elements('wims')
#print("Test exercice =  ", dico_all['Algèbre'])
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
nom_fichier = {'Algèbre':'algebre.phtml','Analyse':'analyse.phtml','Géométrie':'geometrie.phtml'}
for cle,val in dico_all.items():
	f_phtml_them = open(nom_fichier[cle],'w',encoding='Windows 1252')
	f_phtml_them.write('Exercices du thème '+cle+'\n')
	f_phtml_them.close()
	begin_div = '\t<div id="c_'+str(i)+'"><!--Begin thème '+cle+'-->\n\t\
	<h3 class="program_theme">'+cle+'</h3>\n'
	allhtml = allhtml+begin_div
	#objectif = creer_objectif(them)
	begin_div_objectif = '\t\t<div class="accordion">\n\t\t\t<h4>Objectifs</h4>\n\t\t\t<div>\n'
	allhtml = allhtml+begin_div_objectif
	allhtml = allhtml+val['objectif']
	end_div_objectif = '\n\t\t\t</div><!--Fin objectifs-->\n\t\t</div><!--Fin accordion-->\n'
	allhtml = allhtml + end_div_objectif

	begin_div_histoire = '\t\t<div class="accordion">\n\t\t\t<h4>Histoire des mathématiques</h4>\n\t\t\t<div>\n'
	allhtml = allhtml+begin_div_histoire
	allhtml = allhtml+val['histoire']
	end_div_histoire = '\n\t\t\t</div><!--Fin histoire des maths-->\n\t\t</div><!--Fin accordion-->\n'
	allhtml = allhtml + end_div_histoire
	allhtml = allhtml +'\t<h4>Sommaire du thème '+cle+'</h4><!-- Sommaire-->\n'
	allhtml = allhtml+'<ul class="program_submenu">\n\t'
	for num,t in enumerate(dico_all[cle]['titres']):
		allhtml = allhtml+'<li><a href="#t_'+str(i)+str(num)+'">'+t+'</a></li>\n\t'
	allhtml = allhtml+'\n</ul>\n'
	#Contenus, capacités, commentaires
	for num,val in enumerate(dico_all[cle]['contenu']):
		allhtml = allhtml+'<h4 class="program_titre">'+dico_all[cle]['titres'][num]+'</h4>\n'
		begin_div_bloc = '<div id = "t_'+str(i)+str(num)+'" class="grid-x grid-margin-x small-margin-collapse"><!-- Début bloc -->\n'
		allhtml = allhtml +begin_div_bloc
		#Colonne des contenus
		allhtml = allhtml +'<div class="b small-4 medium-4 large-4 cell program_colonne"><!--Colonne contenu-->\n<h4 class="titre_colonne">Contenus</h4>\n'
		#Test 

		allhtml = allhtml +val
		allhtml = allhtml + '</div><!-- Fin colonne contenu-->\n'
		#colonne des cpacités
		allhtml = allhtml +'<div class="box_content2 small-4 medium-4 large-4 cell program_colonne"><!--Colonne capacités-->\n<h4 class="titre_colonne">Capacités atendues</h4>\n'
		allhtml = allhtml +dico_all[cle]['capacite'][num]
		allhtml = allhtml + '</div><!-- Fin colonne capacites-->\n'
		#Colonnes compléments
		allhtml = allhtml +'<div class="box_content2 small-4 medium-4 large-4 cell program_colonne"><!--Colonne commentaires-->\n<h4 class="titre_colonne">Démonstrations-Algorithmes-Approfondissements</h4>\n'
		allhtml = allhtml +dico_all[cle]['commentaire'][num]
		allhtml = allhtml + '\n</div><!-- Fin colonne commentaires-->\n'
		exercices = dico_all[cle]['wims'][num]
		if len(exercices) != 0 :
			liste_de_lien = creer_liste_exo(cle,dico_all[cle]['titres'][num],exercices)
		#print("Thème : ",cle," Titre : ",dico_all[cle]['titres'][num],"\nExercices n° ",num ," : \n",dico_all[cle]['wims'][num])
		allhtml = allhtml +'<div class="box_content2 small-12 cell"><!-- Les exercices -->\
		\nInsérer ici les exercices du paragraphe '+ dico_all[cle]['titres'][num]+'\n<ul class=program_list>\n'
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


