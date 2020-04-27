import time
import socket

#Constantes d'application
IP = "127.0.0.1"
Port = 1234

#On défini les paramêtres du socket 
Serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
Serveur.bind((IP, Port))

#On configure le serveur en mode non-bloquant : Au lieu d'attendre une réponse et de bloquer le programme, l'instruction retourne 
#une exeception si jamais aucune données n'est envoyée
Serveur.setblocking(0)

#Démarrage du serveur
Serveur.listen()
print("Serveur démarré à", time.strftime("%H:%M:%S"))

#On initialise la liste qui contient les coordonnées des clients connectés
listeClient = []

while True:
	#Si il y'a une nouvelle connnexion, on traite la connexion
	try:
		infosClients, IPClient = Serveur.accept()
		listeClient.append(infosClients) #On stocke les infos du client dans la liste dédiées
		print("Nouveau client connecté ! IP =>", str(IPClient))
	except IOError:
	#Si personne n'essaie de se connecter, on ralenti le programme pour préserver les ressources de la machine
		time.sleep(0.1)
	
	for client in listeClient:
	#On récupere chaque clients dans la variable
		
		#Si un message est envoyé, on le récupere, sinon l'instruction génére une exception
		try:
			message = client.recv(2048)
			message = message.decode("utf-8")

			if message == "":
				pass

			else:
				print(message)

				for destinataire in listeClient:
				#On désigne les destinaires du message, à savoir tout les clients connectés
					if destinataire != client:
					#Si le destinaire n'est pas l'expéditeur
						destinataire.send(bytes(message, "utf-8"))
					else:
						pass
		except:
			#Si aucun message n'a été envoyé
			time.sleep(0.1)