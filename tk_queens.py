#!/usr/bin/env python

import itertools
from Tkinter import *
from PIL import Image, ImageTk


class Board():
	def __init__(self,parent,w,h):
		self.solns=list(); self.solnum=0; self.qtags=list()
		frame=Frame(parent); frame.pack()

		self.label=Label(frame); self.label.pack()
		
		self.board=Canvas(frame, width=w, height=h); self.board.pack()
		colors=['green','yellow']
		self.s=w/8; x=0; k=0
		for i in range(8):
			y=0
			for j in range(8):
				self.board.create_rectangle(x,y,x+self.s,y+self.s,fill=colors[k])
				y=y+self.s
				k=1-k
			x=x+self.s
			k=1-k
		imfile=Image.open("50px-Chess_qdt45.svg.png")
		self.queen=ImageTk.PhotoImage(imfile)
		self.qw=self.queen.width(); self.qh=self.queen.height()
		xscale=1.0; yscale=1.0
		imfile=imfile.resize((int(xscale*self.qw), int(yscale*self.qh)), Image.ANTIALIAS)
		self.queen=ImageTk.PhotoImage(imfile)
		self.qw=self.queen.width(); self.qh=self.queen.height()
		self.xoffset=(self.s-self.qw); self.yoffset=(self.s-self.qh)
		
		self.button=Button(frame, text="Click here for next solution")
		self.button.bind("<1>",self.showSolution)
		self.button.pack()
		return

	def solutions(self):
		for p in itertools.permutations(range(8)):
			b=[(i,p[i]) for i in range(8)]
			for r,c in b:
				i,j=r,c
				z=False
				while not z:
					i=i-1
					if i<0: break
					j=j-1
					if j<0: break
					if (i,j) in b: z=True
				if z: break
				i,j=r,c
				while not z:
					i=i+1
					if i>7: break
					j=j+1
					if j>7: break
					if (i,j) in b: z=True
				if z: break
				i,j=r,c
				while not z:
					i=i-1
					if i<0: break
					j=j+1
					if j>7: break
					if (i,j) in b: z=True
				if z: break
				i,j=r,c
				while not z:
					i=i+1
					if i>7: break
					j=j-1
					if j<0: break
					if (i,j) in b: z=True
				if z: break
			if z: continue
			yield p

	def showSolution(self,data=None):
		if self.solnum==0:
			for p in self.solutions(): self.solns.append(p)
		self.solnum+=1
		if self.solnum>len(self.solns): self.solnum=1
		text="Solution no: %d"%self.solnum
		self.label.config(text=text)
		p=self.solns[self.solnum-1]
		if not self.qtags:
			for i in range(8):
				j=p[i]
				x=i*self.s+self.xoffset; y=j*self.s+self.yoffset
				t=self.board.create_image(x,y,image=self.queen)
				self.qtags.append(t)
		else:
			for i in range(8):
				j=p[i]
				x=i*self.s+self.xoffset; y=j*self.s+self.yoffset
				self.board.coords(self.qtags[i],(x,y))
		return

root=Tk()
root.wm_title("Eight queens problem")
sw=root.winfo_screenwidth(); sh=root.winfo_screenheight()
ar=float(sw)/float(sh)
w=int(sw*0.4); w=(w/8)*8
h=int(sh*ar*0.4); h=(h/8)*8
x=(sw-w)/2; y=(sh-h)/2
root.geometry("+%d+%d"%(x,y))
b=Board(root,w,h)
root.mainloop()
