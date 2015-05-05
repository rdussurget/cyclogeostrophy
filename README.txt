Ce dossier est une distribution du module Cyclogeostrophy

Ce module contient notamment différents outils pour la lecture et l'écriture
de fichiers NetCDF et la gestion des points de grilles.
Il s'agit d'une remise en forme principalement cosmétique du code plus un certain nombre de modifications.


INSTALLATION:

	python setup.py install
	Installe la distrib sur le système (nécessite les droits adéquats).
	
	Pour modifier les répertoires d'installation, utiliser les options  --prefix, --install-lib et ou --install-scripts
	(eg. --prefix /mon/chemin/)
	
EXECUTION:

	compute_ug.py fichier_UV.nc  fichier_CUV.nc
	ou fichier_UV.nc est un fichier AVISO contenant les vitesses géostrophiques.
	Il s'agit du programme original modifié pour prendre un entrée directement les vitesses et non plus les hauteurs.
	
	Le programme fichier_CUV.nc est défini, par défaut, dans le fichier cyclogeo/utils.nc.yaml. Il est possible de définir un format alternatif et de le faire passer à la fonction LoadYaml() 
	
TODO:

	Compléter la librairie avec d'autres fonctions/programmes.


Pour plus d'info, ne pas hésiter à me contacter (je dispose d'un dépot Mercurial que je peux mettre à disposition de qui veux pour faire évoluer ce code!). 

R.Dussurget
rdussurget@cls.fr
