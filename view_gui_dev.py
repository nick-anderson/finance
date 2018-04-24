from Tkinter import *
import numpy as np
import pickle
import os
import sys


class  MainApp():

	def gui(self):
		self.vals = []
		self.frame_clicks = 0
		self.beginning = True
		f = open(os.getcwd() +'{}output{}instruments.txt'.format(self.slash,self.slash))
		self.instruments = ""
		for i in f:
			self.instruments += i[:-1]
			self.instruments += ','
		self.instruments = self.instruments[:-1]
		self.volumes = {}
		for i in (self.instruments.split(',')):
			self.volumes[i] = ''
		self.root = Tk()
		self.root.title("Replay App")
		self.roots = []
		for i in range(len(self.instruments.split(','))):
			self.roots.append(Tk())
		self.iv = IntVar()

		self.framevar = IntVar()
		self.font_size = IntVar()
		self.font_size.set(8)
		self.refresh_rate = IntVar()
		self.refresh_rate.set(10)
		self.timevar = IntVar()
		self.timevar.set(100)
		self.framevar.set(0)
		Entry(self.root, textvariable=self.framevar).grid(row=5,column=2)
		Label(self.root, text = "Frame").grid(row=5,column=0)
		Button(self.root, text="Next Frame",command = self.generate_next_frame).grid(row=5,column=4,rowspan=3)
		Button(self.root, text="Previous Frame",command = self.generate_previous_frame).grid(row=5,column=3)
		Button(self.root, text="Refresh",command = self.refresh).grid(row=7,column=3)
		Button(self.root, text="Next Trade",command = self.nexttrade).grid(row=7,column=4)
		Entry(self.root, textvariable=self.timevar).grid(row=6,column=2)
		Label(self.root, text = "Nanoseconds").grid(row=6,column=0)
		Label(self.root, text = "Refresh Rate").grid(row=7,column=0)
		Entry(self.root, textvariable=self.refresh_rate).grid(row=7,column=2)
		Label(self.root, text = "Font Size").grid(row=8,column=0)
		Entry(self.root, textvariable=self.font_size).grid(row=8,column=2)

		Button(self.root, text="Go forward seconds",command = self.forward_time).grid(row=6,column=3)
		self.root.mainloop()
	def __init__(self):
		if sys.platform.startswith('darwin'):
			self.slash = '/'
		if sys.platform.startswith('win32'):
			self.slash = '\\'

		self.gui()
	def nexttrade(self):
		trades = open(os.getcwd() +'{}output{}trades.txt'.format(self.slash,self.slash))
		curr =  int(self.framevar.get())
		for i in trades:
			val = int(i.strip('\n'))
			if val > curr:
				self.framevar.set(int(val))
				# self.display()
				self.generate_previous_frame()
				# self.generate_previous_frame()
				self.generate_next_frame()
				break
		# break
	def nothing(self):
		True
	def previous_time(self):
		True
	def forward_time(self):
		aList = []
		f = open(os.getcwd() +'{}output{}times.txt'.format(self.slash,self.slash))
		amount = int(self.timevar.get())
		current_frame = str(self.framevar.get())
		for i in f:
			val = i.strip('\n').split('-')
			time, frame = val[0],val[1]
			aList.append([time,frame])
			if str(frame) == str(current_frame):
				current_time = time
				# print time

		future_time = int(current_time) + int(amount)
		for i in aList:
			time, frame = i[0],i[1]
			if int(time) > future_time:
				# print 'ha'
				wanted_event_frame = frame
				self.framevar.set(int(wanted_event_frame))
				# self.display()
				self.generate_previous_frame()
				# self.generate_previous_frame()
				self.generate_next_frame()
				self.generate_next_frame()
				# print '_DDD'
				f.close()
				break



	def generate_next_frame(self):
		self.frame_clicks += 1
		if int(self.frame_clicks) == int(self.refresh_rate.get()):
			self.frame_clicks = 0

			self.refresh()
		# self.frame = int(self.framevar.get()) + 1
		self.framevar.set(int(self.framevar.get())+1)
		self.display()
	def refresh(self):
		for val in self.roots:
			for child in val.winfo_children():
				child.pack_forget()
				child.destroy()
				del child

	def display(self):
		#self.framechange
		a = pickle.load(open(os.getcwd() +'{}output{}objects{}bid_quantity_{}.pkl'.format(self.slash,self.slash,self.slash,str(self.framevar.get()))))
		b = pickle.load(open(os.getcwd() +'{}output{}objects{}offer_quantity_{}.pkl'.format(self.slash,self.slash,self.slash,str(self.framevar.get()))))
		c = pickle.load(open(os.getcwd() +'{}output{}objects{}trade_quantity_{}.pkl'.format(self.slash,self.slash,self.slash,str(self.framevar.get()))))
		a1 = pickle.load(open(os.getcwd() +'{}output{}objects{}bid_order_{}.pkl'.format(self.slash,self.slash,self.slash,str(self.framevar.get()))))
		b1 = pickle.load(open(os.getcwd() +'{}output{}objects{}offer_order_{}.pkl'.format(self.slash,self.slash,self.slash,str(self.framevar.get()))))
		c1 = pickle.load(open(os.getcwd() +'{}output{}objects{}trade_order_{}.pkl'.format(self.slash,self.slash,self.slash,str(self.framevar.get()))))
		d = pickle.load(open(os.getcwd() +'{}output{}objects{}details_{}.pkl'.format(self.slash,self.slash,self.slash,str(self.framevar.get()))))
		dictionary_instruments = self.instruments.split(',')
		new_price = False
		volume_dict = {}
		for r,instr in enumerate(dictionary_instruments):
			try:
			# if True:
				new_price = False
				# new_price_loc
				for label in self.roots[r].grid_slaves():
					label.grid_remove()
				self.roots[r].title(instr)

				try:
					price_set = list(set(a[instr].keys()+b[instr].keys()))
					price_set.sort()
					price_set.reverse()
					old_box = np.load(os.getcwd() +'{}output{}objects{}{}_{}.npy'.format(self.slash,self.slash,self.slash,instr,str(int(self.framevar.get())-1)))
				except:
					# print 'here1', instr
					pass
				box = np.zeros((len(price_set),6)).astype(float)
				if int(self.framevar.get())> 0:
					e = pickle.load(open(os.getcwd() + '{}output{}objects{}{}_volume_{}.pkl'.format(self.slash,self.slash,self.slash,instr,str(self.framevar.get()))))
					if int(self.framevar.get()) == 1:
						e_old = e
					else :
						e_old = pickle.load(open(os.getcwd() + '{}output{}objects{}{}_volume_{}.pkl'.format(self.slash,self.slash,self.slash,instr,str(int(self.framevar.get())-1))))
					# if e == 'nan':
					# 	Label(self.roots[r], text=str(self.volumes[instr]),font = ('Times',self.font_size.get())).grid(row=1,column=3)
					# if e != 'nan' and self.frame != 0:
					# 	Label(self.roots[r], text=str(e), bg='yellow',font = ('Times',self.font_size.get())).grid(row=1,column=3)
					# 	self.volumes[instr] = str(e)
					if e != e_old:
						Label(self.roots[r], text=str(e),bg = "yellow",font = ('Times',self.font_size.get())).grid(row=1,column=3)
					else:
						Label(self.roots[r], text=str(e),font = ('Times',self.font_size.get())).grid(row=1,column=3)

					# self.volumes[instr] = e
					# print self.volumes
					# print e, 'eeee'
				# if self.frame == 1:
					# e = pickle.load(open(os.getcwd() + '{}output{}objects{}{}_volume_{}.pkl'.format(self.slash,self.slash,self.slash,instr,self.frame)))

				if int(self.framevar.get()) == 0:
					f_volumes = open('output{}volumes.txt'.format(self.slash))
					for i in f_volumes:
						vol_instr,vol = i.split('|')
						# print vol_instr, vol
						if instr == vol_instr:
							e = vol
					Label(self.roots[r], text=str(e),font = ('Times',self.font_size.get())).grid(row=1,column=3)
					self.volumes[instr] = str(e)
					# volume_dict = {}
				# print instr, price_set
				# try:
				for i,price in enumerate(price_set):
						box[i,2] = price
						# print instr, price, '1'
						if price in b[instr].keys():
							box[i,3] = float(b[instr][price])
							try:
								box[i,4] = float(b1[instr][price])
							except:
								#patch in late march, unsure of why couldn't find order
								box[i,4] = 0
						# print instr, price, '2'

						if price in a[instr].keys():
							box[i,1] = a[instr][price]
							try:
								box[i,0] = a1[instr][price]
							except:
								#patch in late march, unsure of why couldn't find order

								box[i,0] = 0
						# print instr, price, '3'

						if price in c[instr].keys():
							box[i,5] = c[instr][price]
						# print instr, price, '4'

							# box[i,6] = c1[instr][price]
				# except:

					# print instr, 'bad'
				try:
					n_i, n_j = np.where((box - old_box) !=0)
				except:
					# print 'here2'
					try:
						# print box.shape, old_box.shape
						old_values = []
						for i in old_box:
							# print i
							old_values.append(i[2])
						for _,i in enumerate(box):
							if i[2] not in old_values:
								# print _,i,'lol'
								new_price = True
								new_price_loc = _
					except:
						# print 'what'
						pass
					# print box.shape, old_box.shape
					# old_values = []
					# for i in old_box:
					# 	print i
						# old_values.append(i[2])
					# for _,i in enumerate(box):
					# 	if i[2] not in old_values:
					# 		print _,i,'lol'
					# 		new_price = True
					# 		new_price_loc = _

					pass

				np.save(os.getcwd() +'{}output{}objects{}{}_{}'.format(self.slash,self.slash,self.slash,instr,str(self.framevar.get())),box)
				Label(self.roots[r], text='bid orders',font = ('Times',self.font_size.get())).grid(row=4,column=0)
				Label(self.roots[r], text='bid quantity',font = ('Times',self.font_size.get())).grid(row=4,column=1)
				Label(self.roots[r], text='price',font = ('Times',self.font_size.get())).grid(row=4,column=2)
				Label(self.roots[r], text='offer quantity',font = ('Times',self.font_size.get())).grid(row=4,column=3)
				Label(self.roots[r], text='offer orders',font = ('Times',self.font_size.get())).grid(row=4,column=4)
				Label(self.roots[r], text='trade quantity',font = ('Times',self.font_size.get())).grid(row=4,column=5)
				# print self.box
				for i in range(box.shape[0]):
					for j in range(box.shape[1]):
						if j == 5:
							if box[i,j] != 0:
								w = Label(self.roots[r], text=box[i,j], bg = 'yellow',font = ('Times',self.font_size.get()))
								#NEW EVENTS
								try:
									if i == n_i[0] and j == n_j[0]:
										w = Label(self.roots[r], text=box[i,j], bg = 'yellow',font = ('Times',self.font_size.get()))
								except:
									# print 'here3', instr
									pass
								###########
								w.grid(row=i+1+5,column=j)


							if box[i,j] == 0:
								w = Label(self.roots[r], text="",font = ('Times',self.font_size.get()))
								w.grid(row=i+1+5,column=j)
						if j != 5:
							w = Label(self.roots[r], text=box[i,j],font = ('Times',self.font_size.get()))
							# if new_price:
							# print new_price
							if new_price and i == new_price_loc and int(self.framevar.get()) > 1:
								# print box[i,j]
								# print 'ohhdj'
								# w = Label(self.roots[r], text=box[i,j], bg = "yellow",font = ('Times',self.font_size.get()))

								w = Label(self.roots[r], bg = 'yellow',text=box[i,j],font = ('Times',self.font_size.get()))
							#NEW EVENTS
							try:
							# if True:

								for k in range(len(n_i)):
									if i == n_i[k] and j == n_j[k]:

										# changed_price = old_box[n_i]
										# temp_a = pickle.load(open(os.getcwd() +'{}output{}objects{}bid_quantity_{}.pkl'.format(self.slash,self.slash,self.slash,self.frame-1)))
										# print temp_a[instr][changed_price]
										# if j == 0:
										# updated_text = 20
										new_text = box[i,j]
										# print new_text
										# print old_box[n_i], 'lol'
										changed_price = old_box[n_i][0][j]
										# print 
										# print new_text
										# print changed_price
										updated_text = str(new_text) + ' (' + str(changed_price) + ')'
										# print changed_price
										# print updated_text
										w = Label(self.roots[r], text=updated_text, bg = 'yellow',font = ('Times',self.font_size.get()))

										 # n_j
										# print self.frame, i, j
							except:
								# print 'wah'

								pass
							###########

							w.grid(row=i+1+5,column=j)
							self.vals.append(w)
				Label(self.roots[r], text='Rpt Sequence',font = ('Times',self.font_size.get())).grid(row=0,column=0)
				Label(self.roots[r], text='Sequence',font = ('Times',self.font_size.get())).grid(row=0,column=1)
				Label(self.roots[r], text='Event Time',font = ('Times',self.font_size.get())).grid(row=2,column=0)
				Label(self.roots[r], text='Send Time',font = ('Times',self.font_size.get())).grid(row=3,column=0)
				Label(self.roots[r], text='Diff Time',font = ('Times',self.font_size.get())).grid(row=0,column=4)

				if int(self.framevar.get()) > 0:
					snd_time = d['Send Time']
					final_snd_time = ""
					for _,i in enumerate(snd_time):
						final_snd_time += i
						if _ == 3 or _ ==5 or _ == 7:
							 final_snd_time += '-'
						if _ == 9 or _ == 11:
							final_snd_time += ': '
						if _ == 13 or _ == 16 or _ == 19:
							final_snd_time += " | "

					# diff_time = str(int(d['Send Time']) - int(d['Event Time']))
					# final_diff_time = ""
					# lv = len(diff_time)
					# for i in diff

					#dzdo
					final_diff_time = str(int(d['Send Time']) - int(d['Event Time']))
					# for _,i in enumerate(str(int(d['Send Time']) - int(d['Event Time']))):
					# 	final_diff_time += i
					# 	if _ == 9 or _ == 11:
					# 		final_diff_time += ': '
					# 	if _ == 13 or _ == 16 or _ == 19:
					# 		final_diff_time += " | "


					Label(self.roots[r], text=(final_diff_time),font = ('Times',self.font_size.get())).grid(row=1,column=4)
					Label(self.roots[r], text=final_snd_time,font = ('Times',self.font_size.get())).grid(row=3,column=1,columnspan=5)

				Label(self.roots[r], text='Volume Update',font = ('Times',self.font_size.get())).grid(row=0,column=3)
				Label(self.roots[r], text='Instrument',font = ('Times',self.font_size.get())).grid(row=0,column=2)

				Label(self.roots[r], text=d['Rpt Sequence'],font = ('Times',self.font_size.get())).grid(row=1,column=0)
				Label(self.roots[r], text=d['Sequence'],font=('Times',self.font_size.get())).grid(row=1,column=1)
				evt_time = d['Event Time']
				final_evt_time = ""
				for _,i in enumerate(evt_time):
					final_evt_time += i
					if _ == 3 or _ ==5 or _ == 7:
						 final_evt_time += '-'
					if _ == 9 or _ == 11:
						final_evt_time += ': '
					if _ == 13 or _ == 16 or _ == 19:
						final_evt_time += " | "
				Label(self.roots[r], text=final_evt_time,font = ('Times',self.font_size.get())).grid(row=2,column=1,columnspan=5)
				Label(self.roots[r], text=instr,font = ('Times',self.font_size.get())).grid(row=1,column=2)

			except:
				print "here5", instr
				pass
		del a
		del b
		del c
		del a1
		del b1
		del c1
		del d



	def generate_previous_frame(self):
		# self.frame = int(self.framevar.get()) - 2
		self.framevar.set(int(self.framevar.get())-3)
		# self.display()
		# self.generate_next_frame()
		self.generate_next_frame()
		self.generate_next_frame()
		# self.display()

MainApp()
