#!/usr/bin/env python

from Tkinter import *
from PIL import Image, ImageTk
import Pmw
import time

knightMoves=[(2,1),(2,-1),(1,2),(1,-2),(-2,1),(-2,-1),(-1,2),(-1,-2)]

class KnightsTour:
	def __init__(self,initRow,initColumn):
		self.board={(i,j):0 for i in range(8) for j in range(8)}
		move=(initRow,initColumn)
		for p in range(1,65):
			self.board[move]=p
			d=self.degreeDict(move)
			move=sorted(d,key=d.get)[0]
		return
	def validMove(self,move):
		if move in self.board and self.board[move]==0: return True
		else: return False
	def degree(self,move):
		r,c=move; deg=0
		for (p,q) in knightMoves:
			if self.validMove((r+p,c+q)): deg+=1
		return deg
	def degreeDict(self,move):
		r,c=move; degDict={}
		for (p,q) in knightMoves:
			tryMove=(r+p,c+q)
			if self.validMove(tryMove): 
				deg=self.degree(tryMove)
				degDict[tryMove]=deg
		if degDict=={}: degDict[move]=0
		return degDict 

class ShowTour:
	def __init__(self,parent,bw,bh):
		self.parent=parent
		frame=Frame(parent); frame.pack()
		Label(frame,text="Click any square",font=("Helvetica","12","bold")).pack()
		self.canvas=Canvas(frame,width=bw,height=bh); self.canvas.pack()
		colors=("green","yellow")
		self.step=bw/8; x,col=0,0
		self.ids=dict();col=0
		for i in range(8):
			y=0
			for j in range(8):
				tid=self.canvas.create_rectangle(x,y,x+self.step,y+self.step,fill=colors[col])
				self.ids[tid]=(j,i)
				self.canvas.tag_bind(tid,"<1>",self.callBack)
				y+=self.step
				col=1-col
			x+=self.step
			col=1-col
		imfile=Image.open("50px-Chess_ndt45.svg.png")
		self.knight=ImageTk.PhotoImage(imfile)
		self.tags=[]
		return
	def callBack(self,event):
		tid=event.widget.find_withtag(CURRENT)[0]
		r,c=self.ids[tid]
		tour=KnightsTour(r,c)
		board=sorted(tour.board,key=tour.board.get)
		offset=self.step/2
		k=0
		for m in board:
			k=k+1
			c,r=m
			ktag=self.canvas.create_image(offset+r*self.step,offset+c*self.step,image=self.knight)
			self.canvas.update_idletasks()
			time.sleep(1)
			self.canvas.delete(ktag)
			self.canvas.update_idletasks()
			t=self.canvas.create_text(offset+r*self.step,offset+c*self.step,text=str(k),font=("Helvetica","24","bold"))
			self.tags.append(t)
		top=Toplevel()
		self.top=top
		buttonBox=Pmw.ButtonBox(top, labelpos='nw',label_text='What next?',frame_borderwidth=2,frame_relief='groove')
		buttonBox.pack(fill='both',expand=1,padx=10,pady=10)
		buttonBox.add('Continue', command=self.Continue)
		buttonBox.add('Terminate',command=self.Terminate)
		buttonBox.add('Cancel',command=self.Cancel)
		buttonBox.setdefault('Cancel')
		buttonBox.alignbuttons()
		buttonBox.invoke()
		return
	def Continue(self):
		for t in self.tags:
			self.canvas.delete(t)
		self.top.destroy()
		return
	def Terminate(self):
		self.parent.destroy()
		return
	def Cancel(self):
		pass

if __name__=="__main__":
	root=Tk()
	Pmw.initialise(root)
	root.wm_title("Knight's tour")
	sw=root.winfo_screenwidth(); sh=root.winfo_screenheight()
	ar=float(sw)/float(sh)
	bw=int(sw*0.4); bw=(bw/8)*8
	bh=int(sh*ar*0.4); bh=(bh/8)*8
	x=(sw-bw)/2; y=(sh-bh)/2
	root.geometry("+%d+%d"%(x,y))
	tmp=ShowTour(root,bw,bh)
	root.mainloop()
