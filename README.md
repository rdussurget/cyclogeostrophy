Ceci est le dépôt interne CLS des outils de correction des effets de cyclo-géostrophie.

Pour accéder au dépôt github: https://github.com/rdussurget/cyclogeostrophy.

NOTE: Il est nécessaire de synchroniser ces deux dépôts afin de bénéficier d'éventuelles MaJ par des développeurs externes.

-------------------

Ce module contient notamment différents outils pour la lecture et l'écriture de fichiers NetCDF et la gestion des points de grilles.

Il s'agit d'une remise en forme principalement cosmétique du code plus un certain nombre de 

1. INSTALLATION:

	python setup.py install
	Installe la distrib sur le système (nécessite les droits adéquats). Idéalement, mettre en place un environnement virtualenv (eg. http://docs.python-guide.org/en/latest/dev/virtualenvs/)

	
	Pour modifier les répertoires d'installation, utiliser les options  --prefix, --install-lib et ou --install-scripts
	(eg. --prefix /mon/chemin/)
	
2. EXECUTION:

	compute_ug.py fichier_UV.nc  fichier_CUV.nc
	ou fichier_UV.nc est un fichier AVISO contenant les vitesses géostrophiques.
	Il s'agit du programme original modifié pour prendre un entrée directement les vitesses et non plus les hauteurs.
	
	La structure du fichier_CUV.nc est définie, par défaut, dans le fichier cyclogeo/utils.nc.yaml. Il est possible de définir un format alternatif et de le faire passer à la fonction LoadYaml() 
	
3. TODO:

	Compléter la librairie avec d'autres fonctions/programmes.


Pour plus d'info, ne pas hésiter à me contacter. 

R.Dussurget
rdussurget@cls.fr