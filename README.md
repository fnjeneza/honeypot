Honey Pot

Pour que l'application puisse marcher, il faut veiller à ce que les fichiers
dans la config  existent et vérifier la lecture et l'écriture dans les
dossiers concernés

docs/
	contient la documentation sur les modules du projet

src/
	-config.yaml	:	fichier de configuration du service
	-tags.yaml		:	contient les tags des balises html
	-db.py			:	contient les actions sur la base de données
	-ldap.py		:	contient les actions sur le ldap
	-inspector.py	:	contient les actions sur la supervision de logs du
						serveur 
	-hphttp.py		:	contient les actions d'intéractions avec la page de
						phishing
	-scheduler		:	contient les actions de plannification des actions
	-honeypotd.py	:	gére le service honeypot. main de l'application
	-config.example/
		-*.ldif		:	structure de l'annuaire LDAP
		-regex.filter:	exemple d'expression régulière python
		-dump.sql	:	sauvegarde sql. Contient les tables necessaires au
						fonctionnement du projet

www/
	manage.py		:	gère le projet django
	www/			:	contient la structur du projet django
	honeypot_web/
		-views.py	:	gère les routes http
		-models.py	:	définit les classes de la base de données
		-templates/
			index.html:	templates de la page web du projet
