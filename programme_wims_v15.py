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
################################################################################
def creer_intro(texte):
	"""Création de l'introduction générale du programme. Peut contenir plusieurs parties présentées avec des accordéons.
	Le titre de chaque partie doit être précédé du caractère £.""" 
	t = texte.split('\n')
	t.remove(t[-1])
	nb_partie = 0
	titre_partie = []
	dico_intro ={}
	for i,e in enumerate(t) :
		if e[0] == '£':
			nb_partie += 1
			titre_partie.append((i,e[1:]))
	for k in range(len(titre_partie)-1) :
		indice1 = titre_partie[k][0]
		indice2 = titre_partie[k+1][0]
		texte = ''.join(t[indice1+1:indice2])
		dico_intro[titre_partie[k][1]]=texte
	fin_texte = ''.join(t[indice2+1:])
	dico_intro[titre_partie[k+1][1]]=fin_texte
	return dico_intro
################################################################################
def begin_html():
	global allhtml, info_gen
	# Enregistrement des informations générales dans un dictionnaire
	info_gen={'titreniveau':'','datewims':'','level':'','ressources':''}
	for cle in info_gen:
		tag = tag='@'+cle
		f=open(path_base_program,'r')
		continuer = True
		while continuer :
			lign = f.readline()
			liste = lign.split(':')
			test_tag = lign.split(':')[0]
			if test_tag == tag or lign == '':
				continuer = False
		index_2pt = lign.index(':')
		info_lu = lign[index_2pt+1:-1]
		info_gen[cle]=info_lu
	Fichier = path_base_program.split('/')[-1]
	Fichier = Fichier.replace('.','_')
	print('Ficj=hier = ',Fichier)
	#Ajout du responsable du programme créé
	txt ='!set email=$responsable_'+Fichier+'\n<h2 class="wims_title">'+info_gen['titreniveau']+\
	'</h2>\n<div class="wims_msg info program_desc"><!--Début info-->\n\t'+info_gen['datewims']+'\n<br/>Ressources complémentaires : <a href ="'+info_gen['ressources']+'" target="_blank">Euler Versailles</a>\n</div><!--Fin info-->\n'
	allhtml = allhtml +txt
	# Construire l'ntroduction du programme créé
	tag ='@intro'
	continuer = True
	while continuer :
		lign = f.readline()
		test_tag = lign.split(':')[0]
		if test_tag == tag :
			continuer = False
	continuer = True
	intro = ''
	dico_intro ={}
	while continuer:
		lign = f.readline()
		test_tag_suiv = lign[0]
		if test_tag_suiv == '@' or lign =='':
			continuer = False
		else :
			intro = intro + lign
	f.close()
	txt_intro = creer_intro(intro)
	for cle,val in txt_intro.items() :
		allhtml = allhtml+'<div class ="accordion"><!--Début accordéon intro-->\n'
		allhtml = allhtml+'<h3>'+cle+'</h3>\n'
		allhtml = allhtml+'<div>'+val+'</div>'
		allhtml = allhtml+'</div><!--Fin accordéon intro-->\n'
################################################################################
def creer_elements(elt):
	global dico_all
	tag_elt ='@'+elt
	for them in dico_all :
		flux = open(path_base_program)
		les_elts = []
		tag ='@theme'
		continuer = True
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
################################################################################
def creer_les_themes():
	global dico_all
	flux = open(path_base_program)
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
################################################################################
def creer_lien_exo(ex):
	lien = ''
	split_ex = ex.split(',')
	print("Test split_ex = ",split_ex)
	#S'il y a des exercices...
	if len(split_ex) > 1:
		mod=split_ex[0]
		exo=split_ex[1]
		titre_modifie=split_ex[2]
		extra0=split_ex[3]
		if exo != '':
			extra = extra0+"&+cmd=new"
		else :
			extra ="&+cmd=intro"
		if titre_modifie =='':
			titre_modifie = exo
		picto=split_ex[4]
		if picto != '':
			picto = "\n\t\t\t\t\t!set wims_ref_class=text_icon icon_"+picto
		desc=split_ex[5]
		if desc != '':
			desc = "\n\t\t\t\t\t!set wims_ref_title="+desc
		lien = "\t\t\t\t<li>"+picto+desc+"\n\t\t\t\t\t!href target=wims_exo module="+mod+"&exo="+exo+extra+" "+titre_modifie+"\n\t\t\t\t</li>\n"
		print('Le lien : ',lien)
	return lien
################################################################################
def creer_liste_exo(them,pt_de_prog,ex):
	global nom_fichier
	l_exo = ex.split('\n')
	les_liens = []
	for e in l_exo :
		lien = creer_lien_exo(e)
		les_liens.append(lien)
	return les_liens
################################################################################
def creer_sommaire(titres,theme,i):
	global allhtml
	print("Thème : ",theme," titres = ",titres)
	titres1 = []
	for e in titres :
	    separer_e = e.split('-')
	    titres1.append(separer_e)
	nb_titres = len(titres1)
	n = 0
	while n<nb_titres :
		if len(titres1[n])==1 :
			allhtml = allhtml + '\t<li><a href="#pt_prog_'+str(i)+str(n)+'">'+titres1[n][0]+'</a></li>\n'
			n += 1
		else :
			continuer = True
			titre_test = titres1[n][0]
			allhtml = allhtml+'\t<li>'+titre_test+'</li>\n'
			allhtml = allhtml+'\t\t<ul class="tirets">\n'
			while continuer and n < nb_titres :
				titre_en_cours = titres1[n][0]
				if titre_en_cours != titre_test :
					continuer = False
					n = n-1
				else :
					allhtml = allhtml + '\t\t\t<li><a href="#pt_prog_'+str(i)+str(n)+'">'+titres1[n][1]+'</a></li>\n'
				n += 1
			allhtml = allhtml+'\t\t</ul>\n'

################################
def creer_program(prog):
	print("Création du programme : ",prog)
	global allhtml, dico_all,fichier_exo
	dico_all = {}
	#Fichier de sortie au format .phtml
	out_phtml =open(prog,'w',encoding='Windows 1252')
	#Contenu du dictionnaire écrit dans allhtml
	allhtml =''
	#Création du début de la page phtml
	begin_html()
	ens_tag = ['objectif','histoire','titre','contenu','capacite','commentaire','presentation','wims','conclusion']
	#Construction du dictionnaire avec le contenu de chaque thème
	creer_les_themes()
	#Mettre les différentes parties du contenu du fichier texte du programme à créer dans le dictionnaire
	for tag_cur in ens_tag :
		creer_elements(tag_cur)
	#Création du code html pour le fichier .phtml
	allhtml=allhtml+'<div id="widget_'+base_programm.replace('.','')+'"><!-- Début de widget_'+base_programm.replace('.','')+'-->'
	allhtml = allhtml+'\n\t<ul class="wims_summary"><!-- Début des onglets des thèmes-->\n'
	i = 0
	for cle,val in dico_all.items() :
		allhtml = allhtml +'\t\t<li><a href="#theme_'+str(i)+'">'+cle+'</a></li>\n'
		i += 1
	allhtml = allhtml+'\t</ul><!-- Fin des onglets des thèmes-->\n'
	# Insérer le contenu de chaque thème :
	i = 0
	#Pour chaque thème, création du bloc des colonnes (1,2 ou 3)
	for cle,val in dico_all.items():
		#print("Test conclusion : \nThème ",cle," Conclusion ",dico_all[cle]['conclusion'])
		# Création d'un fichier d'exercices pour chaque thème
		fichier_exo.write("Thème : "+cle+'\n\n')
		#Début du code du bloc html du thème
		begin_div = '\t<div id="theme_'+str(i)+'"><!--Début du thème '+cle+'-->\n\t\t<h3 class="program_theme">'+cle+'</h3>\n'
		allhtml = allhtml+begin_div
		if info_gen['level'] == '0' :
			sommaire = 'Attendus de fin de cycle'
			objectif = "Présentation"
			titre_col1 = 'CM1'
			titre_col2 = 'CM2'
			titre_col3 = '6<sup>e</sup>'
		elif info_gen['level'] == '1':
			sommaire = 'Attendus de fin de cycle'
			objectif = "Présentation"
			if i != 4 :
				titre_col1 = '5<sup>e</sup>'
				titre_col2 = '4<sup>e</sup>'
				titre_col3 = '3<sup>e</sup>'
			else :
				titre_col1 = '1<sup>er</sup> niveau'
				titre_col2 = '2<sup>e</sup> niveau'
				titre_col3 = '3<sup>e</sup> niveau'
		else :
			sommaire = 'Sommaire'
			objectif = "Objectifs"
			titre_col1 = 'Contenus'
			titre_col2 = 'Capacités attendues'
			titre_col3 = 'Démonstrations-Algorithmes-Approfondissements'
		if val['objectif'] != ['']:
			begin_div_objectif = '\t\t<div class="accordion"><!--Début accordéon objectifs-->\n\t\t\t<h4 class="program_h4">'+objectif+'</h4>\n\t\t\t<div><!--Début objectifs-->\n'
			allhtml = allhtml+begin_div_objectif
			allhtml = allhtml+val['objectif'][0]
			end_div_objectif = '\n\t\t\t</div><!--Fin objectifs-->\n\t\t</div><!--Fin accordéon objectifs-->\n'
			allhtml = allhtml + end_div_objectif
		#print("Histoire = ",val['histoire'])
		if val['histoire'] != ['']:
			begin_div_histoire = '\t\t<div class="accordion"><!--Début accordéon histoire-->\n\t\t\t<h4 class="program_h4">Histoire des mathématiques</h4>\n\t\t\t<div><!--Début histoire-->\n'
			allhtml = allhtml+begin_div_histoire
			allhtml = allhtml+val['histoire'][0]
			end_div_histoire = '\n\t\t\t</div><!--Fin histoire des maths-->\n\t\t</div><!--Fin accordion histroire-->\n'
			allhtml = allhtml + end_div_histoire
		if dico_all[cle]['titre'] != ['']:
			#print("Ensemble des titres du thème ",cle," : ",dico_all[cle]['titre'])
			allhtml = allhtml +'\t\t<div class="program_sommaire">\n<h4 class="program_h4">'+sommaire+'</h4><!-- Début sommaire du thème '+cle+'-->\n'
			allhtml = allhtml+'\t\t<ul class="program_submenu">\n\t\t'
			creer_sommaire(dico_all[cle]['titre'],cle,i)
			allhtml = allhtml+'\n\t\t</ul>\n\t\t</div><!-- Fin sommaire du thème '+cle+'-->\n'
		#Dans le cas où il y a 3 colonnes
		for num,valeur in enumerate(dico_all[cle]['contenu']):
			# Titre du point de programme
			#Ecrire le point de programme dans le fichier d'exercices
			fichier_exo.write(dico_all[cle]['titre'][num]+'\n<ul>\n')
			#Des compléments pour certains points de programme
			if dico_all[cle]['presentation'][num] != '' :
				presentation = dico_all[cle]['presentation'][num]+'<br class="spacer">\n'
			else :
				presentation =''
			# Début du bloc formé par les colonnes (3, 2 ou 1 ?)
			begin_div_bloc = '\t\t<div id = "pt_prog_'+str(i)+str(num)+'" class="grid-x grid-margin-x small-margin-collapse"><!-- Début bloc des colonnes du id pt_prog_'+str(i)+str(num)+'-->\n'
			allhtml = allhtml +begin_div_bloc+'\t\t\t<div class="small-12 cell"><!--Début présentation du pt de prog-->\n\t\t\t\t<h4 class="program_h4">'+dico_all[cle]['titre'][num]+'</h4>\n'+presentation+'\n\t\t\t</div><!--Fin présentation du pt de prog-->\n'
			#Création du bloc de colonnes
			#Il y a les trois colonnes
			if dico_all[cle]['contenu'][num] != [''] and dico_all[cle]['capacite'][num] != [''] and dico_all[cle]['commentaire'][num]!= '':
				class_col = '"small-4 medium-4 large-4 cell program_colonne"'
				bloc_col = '\t\t\t<div class='+class_col+'><!--Début colonne 1-->\n\t\t\t\t<h4 class="titre_colonne">'+titre_col1+'</h4>\n'+\
				valeur+'\n\t\t\t</div><!-- Fin colonne 1-->\n'+'\t\t\t<div class='+class_col+'><!--Début colonne 2-->\n\t\t\t\t<h4 class="titre_colonne">'+titre_col2+'</h4>\n'+\
				dico_all[cle]['capacite'][num]+'\n\t\t\t</div><!-- Fin colonne 2-->\n'+'\t\t\t<div class='+class_col+'><!--Début colonne 3-->\n\t\t\t\t<h4 class="titre_colonne">'+titre_col3+'</h4>\n'+\
				dico_all[cle]['commentaire'][num]+'\n\t\t\t</div><!-- Fin colonne 3-->\n'
				allhtml = allhtml +bloc_col
			#Il y a une seule colonne : capacités attendues
			elif dico_all[cle]['contenu'][num] == '' and dico_all[cle]['capacite'][num] != '' and dico_all[cle]['commentaire'][num] == '':
				class_col = '"small-12 cell program_colonne"'
				bloc_col = '\t\t\t<div class='+class_col+'><!--Début colonne 1-->\n\t\t\t\t<h4 class="titre_colonne">'+titre_col2+'</h4>\n'+\
				dico_all[cle]['capacite'][num]+'\n\t\t\t</div><!-- Fin colonne 1-->\n'
				allhtml = allhtml +bloc_col
			#Pas de colonne commentaire
			elif dico_all[cle]['contenu'][num] != '' and dico_all[cle]['capacite'][num] != '' and dico_all[cle]['commentaire'][num] == '':
				class_col = '"small-6 small-6 cell program_colonne"'
				bloc_col = '\t\t\t<div class='+class_col+'><!--Début colonne 1-->\n\t\t\t\t<h4 class="titre_colonne">'+titre_col1+'</h4>\n'+\
				valeur+'\n\t\t\t</div><!-- Fin colonne 1-->\n'+'\t\t\t<div class='+class_col+'><!--Début colonne 2-->\n\t\t\t\t<h4 class="titre_colonne">'+titre_col2+'</h4>\n'+\
				dico_all[cle]['capacite'][num]+'\n\t\t\t</div><!-- Fin colonne 2-->\n'
				allhtml = allhtml +bloc_col
			# Insertion des exercices
			exercices = dico_all[cle]['wims'][num]
			liste_de_lien = []
			if len(exercices) != 0 :
				liste_de_lien = creer_liste_exo(cle,dico_all[cle]['titre'][num],exercices)
				allhtml = allhtml +'\t\t\t<div class="small-12 cell program_colonne_exo"><!-- Les exercices -->\n'
				for e in liste_de_lien :
					#Ajout du lien dans le fichier d'exercices
					fichier_exo.write(e)
				fichier_exo.write('\n</ul>\n')
				### Création de la fenêtre modale pour les exercices
				if len(liste_de_lien) != 0 :
					les_exo = ''
					fen_modal = ''
					for e in liste_de_lien :
						les_exo = les_exo+e+'\n'
					data_open = 'modal_exo_'+str(i)+str(num)
					titre_lien_exo = ' '+dico_all[cle]['titre'][num]
					fen_modal = """\t\t\t\t<span class="text_icon testexo float_left exo_modal">Exercices :  &nbsp; </span>\n\t\t\t\t<a data-open="""+data_open+""" ><span>"""+titre_lien_exo+"""</span></a>
		\t\t<div class="large reveal" id="""+data_open+""" data-reveal> 
	        		<div class="euler_actu_content_modal">
		        		<h2 class="wims_title">Exercices</h2>
		            	<div class="center euler_title_modal">
		              		<p>"""+cle+""" &#8212; """+dico_all[cle]['titre'][num]+"""</p>
		            	</div>
		            	<br class="spacer">
		            	<ul class="menu vertical">\n"""+les_exo+"""
		            	</ul>
		            	<button class="close-button" data-close aria-label="Close reveal" type="button">
		              		<span aria-hidden="true">&times;</span>
		            	</button>
	        		</div>
	    \t\t</div><!--Fin du modal-->\n\t\t\t\t<script>\n\t\t\t\t\t$$("#"""+data_open+"""").draggable();\n\t\t\t\t</script>"""
					pas_fen_modal = """<div class="accordion">
					\t<h2><span class="exo_modal">Exercices </span>: &nbsp; """+titre_lien_exo+"""</h2>
					\t\t<div>
					\t\t\t<ul class="menu vertical">\n"""+les_exo+"""
		            \t\t\t</ul>
		            \t\t</div>
					</div>"""
					#Pas de fenêtre modale du tout, accordéon pour tout thème
					#test_theme = "!if $wims_theme==Euler\n"+fen_modal+"\n!else\n"+pas_fen_modal+"\n!endif"
					#allhtml = allhtml + test_theme
					allhtml = allhtml + pas_fen_modal
				allhtml = allhtml+'\n\t\t\t</div><!-- Fin exercices -->\n'
			end_div_bloc ='\t\t</div><!--Fin bloc des colonnes du id pt_prog_'+str(i)+str(num)+'-->\n<br class="spacer">\n'
			allhtml = allhtml + end_div_bloc
		if dico_all[cle]['conclusion'][0] != '':
			allhtml = allhtml +'\t\t<div class="small-12 cell program_colonne bg_cl"><!-- Conclusion du thème '+cle+'-->\n'+dico_all[cle]['conclusion'][0]+'\n\t\t</div><!-- Fin conclusion du thème '+cle+'-->\n'
		#Fin du thème
		end_div='\t</div><!--Fin du thème '+cle+'-->\n'
		allhtml = allhtml + end_div
		i += 1
	# Fin du fichier phtml
	allhtml = allhtml+'</div><!--Fin de widget_'+base_programm.replace('.','')+'-->'
	#Création du nom du fichier à mettre dans var proc
	nom_du_prog=base_programm.replace('.','')
	print(nom_du_prog)
	allhtml = allhtml+'\n'+inserer_codejs(nom_du_prog)
	#Ecriture du contenu dans le fichier de sortie .phtml
	out_phtml.write(allhtml)
	out_phtml.close()
	fichier_exo.close()

################################################################################
work_directory = os.getcwd()
dossier_niveau = [work_directory+'/math/College/',work_directory+'/math/Lycee/']
#dossier_niveau = [work_directory+'/math/Test/']
#Lecture du fichier de base du programme pour extraire le contenu
for niveau in dossier_niveau :
	for base_programm in os.listdir(niveau):
		path_base_program = niveau+base_programm
		program_adress ='/home/wims/public_html/modules/help/teacher/program.fr/fr/'
		#Le chemin du fichier phtml qui sera créé pour chaque niveau
		prog_niveau = program_adress+base_programm+'.phtml'
		#Création d'un fchier phtml pour regrouper les exercices proposés par niveau
		fichier_exo = open('exo_'+base_programm.replace('.','_')+'.phtml','w',encoding='Windows 1252')
		texte = ' '*50+'Liste d\'exercices du niveau '+base_programm.replace('.','_')+'\n'
		fichier_exo.write(texte)
		#Création du fichier phtml pour chaque niveau
		creer_program(prog_niveau)

