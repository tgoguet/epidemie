# Thomas GOGUET

import tkinter as tk
import time

from enum import Enum
from random import randint

from tkinter import *

tailleFenetre = "1050x720"
tailleCellule = 12
nombreDeLignes = 50
nombreDeColonnes = nombreDeLignes
tailleCanvas = tailleCellule * nombreDeColonnes

increment = 5

txtTitre = "Simulation d'épidémie"
txtTauxTransmission = "Taux de transmission : "
txtTauxVaccination = "Taux de vaccination : "
txtInProgress = "Simulation en cours"
		
class Etat(Enum):
	vaccine = 1
	sain = 2
	malade = 3
	immunise = 4

class App(tk.Frame):

	def __init__( self, parent):
		tk.Frame.__init__(self, parent)
		self._createVariables(parent)
		self._createCanvas()

	def _createVariables(self, parent):
		self.parent = parent
		self.rectx0 = 0
		self.recty0 = 0
		self.rectx1 = 0
		self.recty1 = 0
		self.rectid = None
		self.risqueDeContamination = 20
		self.tauxDeVaccination = 20
		self.contaminationEnCours = False

		
	def _createCanvas(self):
		self.canvas = tk.Canvas(self.parent, width = 10, height = 10, bg = "white" )
		self.canvas.place(x = 50, y = 80, width=tailleCanvas, height=tailleCanvas)
		
		# Titre
		self.labelTitre = tk.Label(root, text=txtTitre)
		self.labelTitre.place(x = 200, y = 20, width=300, height=50)
		self.labelTitre.config(font=("Arial", 20))
		
		# Bloc vaccination
		bouton_augmenteVaccination = tk.Button(root, text="▲", command=self.augmenteVaccination)
		bouton_augmenteVaccination.place(x = 700, y = 100, width=30, height=25)
		
		bouton_diminueVaccination= tk.Button(root, text="▼", command=self.diminueVaccination)
		bouton_diminueVaccination.place(x = 700, y = 130, width=30, height=25)
		
		self.labelTauxVaccination = tk.Label(root, text="...")
		self.labelTauxVaccination.config(text= txtTauxVaccination + str(self.tauxDeVaccination) + " %")
		self.labelTauxVaccination.place(x = 750, y = 120, width=150, height=25)
		
		# Bloc transmission
		bouton_augmenteContagion = tk.Button(root, text="▲", command=self.augmenteContagion)
		bouton_augmenteContagion.place(x = 700, y = 170, width=30, height=25)
		
		bouton_diminueContagion = tk.Button(root, text="▼", command=self.diminueContagion)
		bouton_diminueContagion.place(x = 700, y = 200, width=30, height=25)
		
		self.labelTauxContagion = tk.Label(root, text="...")
		self.labelTauxContagion.config(text= txtTauxTransmission + str(self.risqueDeContamination) + " %")
		self.labelTauxContagion.place(x = 750, y = 190, width=150, height=25)
		
		# Bouton action
		bouton_action = tk.Button(root, text="Démarrer la simulation", command=self.action)
		bouton_action.place(x = 700, y = 250, width=150, height=25)
		
		# Bouton quitter
		#bouton_quitter = tk.Button(root, text="Quitter", command=quit)
		#bouton_quitter.place(x = 880, y = 250, width=150, height=25)		

		# LabelInProgress
		self.labelInfo = tk.Label(root, text="")
		self.labelInfo.place(x = 700, y = 300, width=150, height=25)
				
		# Legende
		#frameLegende = Frame ( root, relief="ridge" ) #, option, ... )
		frameLegende.place(x = 680, y = 400, width=330, height=280)
		self.afficheLegende("Individu sans contact avec la maladie", Etat.sain, 450)
		self.afficheLegende("Individu vacciné", Etat.vaccine, 500)
		self.afficheLegende("Individu malade", Etat.malade, 550)
		self.afficheLegende("Individu en contact avec la maladie, non malade", Etat.immunise, 600)
		
		
	def afficheLegende(self, texteLegende, etatLegende, yLegende):
		frameLegende.canvasLegende1 = tk.Canvas(self.parent, width = tailleCellule, height = tailleCellule, bg = "white" )
		frameLegende.canvasLegende1.place(x = 700, y = yLegende+5, width=tailleCellule, height=tailleCellule)
		self.afficheRectDansCanvas(1, 1, etatLegende , frameLegende.canvasLegende1)
		frameLegende.legendeSain = tk.Label(root, text=texteLegende, anchor="w")
		frameLegende.legendeSain.place(x = 720, y = yLegende, width=280, height=25)


	def augmenteVaccination(self):
		self.changeVaccination(increment)
		
	def diminueVaccination(self):
		self.changeVaccination(-increment)
	
	def changeVaccination(self, increment):
		if self.tauxDeVaccination + increment > 0 and self.tauxDeVaccination + increment < 100 :
			self.tauxDeVaccination += increment
			self.labelTauxVaccination.config(text= txtTauxVaccination + str(self.tauxDeVaccination) + " %")
	
	def augmenteContagion(self):
		self.changeContagion(increment)
		
	def diminueContagion(self):
		self.changeContagion(-increment)
	
	def changeContagion(self, increment):
		if self.risqueDeContamination + increment > 0 and self.risqueDeContamination + increment < 100 :
			self.risqueDeContamination += increment
			self.labelTauxContagion.config(text= txtTauxTransmission + str(self.risqueDeContamination) + " %")
		
	def createArray(self):
		self.tableau={}
		self.nextTableau={}
		i=1
		j=1
		while i <= nombreDeColonnes:
			j=1
			while j <= nombreDeLignes:
				self.tableau[i,j]=Etat.sain
				self.nextTableau[i,j]=Etat.sain
				j += 1
			i += 1
	
	def ajouteAleatoirementUnMalade(self):
		i=randint(1, nombreDeColonnes)
		j=randint(1, nombreDeLignes)
		self.tableau[i,j]=Etat.malade
		self.nextTableau[i,j]=Etat.malade
		
	def afficheRect(self, i,j,valeur):
		if valeur==Etat.vaccine: 	couleur = '#1df215'
		elif valeur==Etat.sain:		couleur = '#fffb9e'
		elif valeur==Etat.malade:	couleur = '#ed1010'
		elif valeur==Etat.immunise:	couleur = '#045e00'
		self.rect = self.canvas.create_rectangle(	(i-1)*tailleCellule,
													(j-1)*tailleCellule,
													i*tailleCellule,
													j*tailleCellule,
													fill=couleur )

	def afficheRectDansCanvas(self, i,j,valeur, theCanvas):
		if valeur==Etat.vaccine: 	couleur = '#1df215'
		elif valeur==Etat.sain:		couleur = '#fffb9e'
		elif valeur==Etat.malade:	couleur = '#ed1010'
		elif valeur==Etat.immunise:	couleur = '#045e00'
		self.rect = theCanvas.create_rectangle(	(i-1)*tailleCellule,
													(j-1)*tailleCellule,
													i*tailleCellule,
													j*tailleCellule,
													fill=couleur )
													
	def afficheArray(self):
		i=1
		j=1
		while i <= nombreDeColonnes:
			j=1
			while j <= nombreDeLignes:
				self.afficheRect(i,j,self.tableau[i,j])
				j += 1
			i += 1
		root.update()
	
	def uneEtapeDeContagion(self):
		i=1
		j=1
		while i <= nombreDeColonnes:
			j=1
			while j <= nombreDeLignes:
				if self.tableau[i,j] == Etat.malade:
					self.contamine(i-1,j-1)
					self.contamine(i-1,j)
					self.contamine(i-1,j+1)
					self.contamine(i,j-1)
					self.contamine(i,j)
					self.contamine(i,j+1)
					self.contamine(i+1,j-1)
					self.contamine(i+1,j)
					self.contamine(i+1,j+1)
				j += 1
			i += 1
		self.recupereNouvelEtat()

	def recupereNouvelEtat(self):
		i=1
		j=1
		while i <= nombreDeColonnes:
			j=1
			while j<= nombreDeLignes:
				self.tableau[i,j]=self.nextTableau[i,j]
				j += 1
			i += 1
			
	def contamine(self, i, j):
		if i>=1 and i<=nombreDeColonnes and j>=1 and j<=nombreDeLignes :
			if self.nextTableau[i,j]==Etat.sain :
				self.contaminationEnCours=True
				chance=randint(1, 100)
				if chance > self.risqueDeContamination :
					self.nextTableau[i,j]=Etat.immunise
				else :
					self.nextTableau[i,j]=Etat.malade

	def action(self):
		self.labelInfo.config(text= txtInProgress )
		self.createArray()
		self.vaccine()
		self.ajouteAleatoirementUnMalade()
		self.ajouteAleatoirementUnMalade()
		self.ajouteAleatoirementUnMalade()
		self.afficheArray()
		t=1
		self.contaminationEnCours=True
		while self.contaminationEnCours and t<50:
			#time.sleep(1)
			self.contaminationEnCours=False
			self.canvas.delete(ALL)
			self.uneEtapeDeContagion()
			self.afficheArray()
			t +=1
		self.labelInfo.config(text= "" )

	def vaccine(self):
		i=1
		j=1
		while i <= nombreDeColonnes:
			j=1
			while j <= nombreDeLignes:
				probaVaccin = randint(1, 100)
				if probaVaccin <= self.tauxDeVaccination :
					self.tableau[i,j]=Etat.vaccine
					self.nextTableau[i,j]=Etat.vaccine
				j += 1
			i += 1

if __name__ == "__main__":
	root = tk.Tk()
	root.geometry( tailleFenetre )
	root.title('Simulation d\'épidémie')
	frameLegende = LabelFrame( root, text="Légende" )
	app = App(root)
	root.mainloop()

