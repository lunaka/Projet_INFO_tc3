# -*- coding: utf-8 -*-
"""
Created on Tue Jun 12 09:38:45 2018

@author: User
"""

import http.server
import socketserver
from urllib.parse import urlparse, parse_qs
import json
import sqlite3
from time import sleep
from Chercher_Base_Donnees import *
import shutil
import codecs
import os
# Port d'écoute du serveur web. Notez qu'il faut être root pour avoir accès aux ports 80 et 443. 
PORT = 8080
print('Running on port {}'.format(PORT))


# définition du handler
class RequestHandler(http.server.SimpleHTTPRequestHandler):

	# nous permettra une redirection
    static_dir = 'client'

	# version du serveur
    server_version = '0.0'

    
    code = codecs.open('client/Interface1.html', encoding = 'utf-8', mode = 'r') 
    code_html = code.read()
    code.close()
    
    scene_courante = [] #liste des objets en mémoire
	
    def do_GET(self):
        self.init_params()
        
        if self.path == '/':
            shutil.copyfile('scene_vide.png', 'client/image/scene_courante.png')
            self.send_html(self.code_html)
        else:
            # on modifie le chemin d'accès en insérant le répertoire préfixe
            self.path = self.static_dir + self.path
        
            http.server.SimpleHTTPRequestHandler.do_GET(self)
        
	# méthode pour traiter les requêtes POST - non utilisée dans l'exemple
    def do_POST(self):
        self.init_params()
        n = len(self.path_info)
        
        if n>0 and self.path_info[0] == "service":
            if self.params['forme'][0] == 'Ajouter Forme':
                self.scene_courante.append(self.params['formeSelection'] + self.params['posX'] + self.params['posY'] + self.params['posZ'] + self.params['taille'])
            else:
                for i in range (len(self.scene_courante)):
                    self.scene_courante.pop()
                
            #on va chercher dans la base de données ou creer l'image demandée
            im=Cherche_Base_Donnees(self.scene_courante)       			

            # image = '/images/nom.png'
            image=im+'.png' # On indique le chemin menant à l'image.
            shutil.copyfile(image, 'client/image/scene_courante.png')
            self.send_html(self.code_html)

        # méthode non autorisée
        else:
            self.send_error(400)
		
	# on envoie un document html dynamique
    def send_html(self,content):
        headers = [('Content-Type','text/html;charset=utf-8')]
        html = '<!DOCTYPE html><title>{}</title><meta charset="utf-8">{}' \
            .format(self.path_info[0],content)
        self.send(html,headers)

	# on envoie un contenu encodé en json
    def send_json(self,data,headers=[]):
        body = bytes(json.dumps(data),'utf-8') # encodage en json et UTF-8
        self.send_response(200)
        self.send_header('Content-Type','application/json')
        self.send_header('Content-Length',int(len(body)))
        [self.send_header(*t) for t in headers]
        self.end_headers()
        self.wfile.write(body) 

	# on envoie la réponse
    def send(self,body,headers=[]):
        encoded = bytes(body, 'UTF-8')

        self.send_response(200)

        [self.send_header(*t) for t in headers]
        self.send_header('Content-Length',int(len(encoded)))
        self.end_headers()

        self.wfile.write(encoded)


	# on analyse la requête pour initialiser nos paramètres
    def init_params(self):
		# analyse de l'adresse
        info = urlparse(self.path)
        self.path_info = info.path.split('/')[1:]
        self.query_string = info.query
        self.params = parse_qs(info.query)

		# récupération du corps
        length = self.headers.get('Content-Length')
        ctype = self.headers.get('Content-Type')
        if length:
            self.body = str(self.rfile.read(int(length)),'utf-8')
            self.params = parse_qs(self.body)
        if ctype == 'application/x-www-form-urlencoded' : 
            self.params = parse_qs(self.body)
        else:
            self.body = ''
		#print(length,ctype,self.body, self.params)

    def send_static(self):

    # on modifie le chemin d'accès en insérant le répertoire préfixe
        self.path = self.static_dir + self.path

    # on calcule le nom de la méthode (do_GET ou do_HEAD) à appeler
    # via la classe mère, à partir du verbe HTTP (GET ou HEAD)
        method = 'do_{}'.format(self.command)

    # on traite la requête via la classe mère
        getattr(http.server.SimpleHTTPRequestHandler,method)(self)


########### insérer le nom de la base de donnée
# connexion à la base de données.
conn = sqlite3.connect('raytracing.sqlite')
cur = conn.cursor()


# instanciation et lancement du serveur
httpd = socketserver.TCPServer(("", PORT), RequestHandler)
httpd.serve_forever()