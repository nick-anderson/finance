from Tkinter import *
import numpy as np
import pickle
import os
import csv
import time
import pandas as pd
from datetime import datetime
import sys

class  MainApp():
	def begin(self):
		self.dumpdf = True
		self.vals = []
		self.beginning = True
		self.load = Tk()
		self.load.title('Gui Loader (N/A)')
		self.dayvar = StringVar()
		self.rpt = StringVar()
		self.instr = StringVar()
		self.instruments = StringVar()
		self.evts = StringVar()
		self.font_size = StringVar()
		self.lookback = IntVar()
		self.rpt.set('2718400')
		self.lookback.set(10000)
		self.evts.set('500')
		self.dayvar.set('20170404')
		self.instr.set('YMM7')
		self.instruments.set('YMM7')
		self.volumes = {}
		for i in (self.instruments.get().split(',')):
			self.volumes[i] = ''
		Label(self.load, text = "Day of data (YYYYMMDD): ").grid(row=0,column=0)
		Entry(self.load, textvariable=self.dayvar).grid(row=0,column=1)
		Label(self.load, text = "Rpt_seq Lookup: ").grid(row=1,column=0)
		Entry(self.load, textvariable=self.rpt).grid(row=1,column=1)
		Label(self.load, text = "Instrument Lookup: ").grid(row=2,column=0)
		Entry(self.load, textvariable=self.instr).grid(row=2,column=1)
		Label(self.load, text = "Instruments to View: ").grid(row=3,column=0)
		Entry(self.load, textvariable=self.instruments).grid(row=3,column=1)
		Label(self.load, text = "How many events to generate: ").grid(row=4,column=0)
		Entry(self.load, textvariable=self.evts).grid(row=4,column=1)
		Label(self.load, text = "How frames to lookback for initial generation: ").grid(row=5,column=0)
		Entry(self.load, textvariable=self.lookback).grid(row=5,column=1)
		Button(self.load, text="Generate Frames",command = self.process).grid(row=6,column=0)
		self.load.mainloop()
	def exit(self):
		print 'okv'
		os._exit(0)
		sys.exit()

	def process(self):
		self.load.destroy()
		# self.exit = Tk()
		# Button(self.exit, text="Stop",command = self.exit).grid(row=0,column=0)
		# self.exit.mainloop()


		data_dict = {
		'34':'sequence',
		'83': 'RptSeq' ,
		'60': 'event time',
		'52':'send time',
		'268':'MDU number' ,
		'279':'MDupdateAction' ,
		'269':'MD entry type',
		'55':'instrument name',
		'270':'price',
		'271':'quantity',
		'346':'NumberOfOrders'}


		md_entry_dict = {
		'0' : 'Bid',
		'1' : 'Offer',
		'2' : 'Trade',
		'e' : 'Electronic Volume',
		'N' : 'Session High Bid',
		'O' : 'Session Low Offer',
		'E' : 'Implied Bid',
		'F' : 'Implied Offer'
		}

		mdu_update_dict = {
		'0' : 'New',
		'1' : 'Change',
		'2' : 'Delete'
		}
		def look():
			_ = 0
			daylookup = self.dayvar.get()
			rpt = self.rpt.get()
			file_name = 'cleaned_data{}{}.txt'.format(self.slash,daylookup)
			input = csv.reader(open(file_name), delimiter = '\x01')
			with open(file_name, 'rU') as input:
				for sequence in csv.reader((line.replace('\0','') for line in input), delimiter="\x01"):
					try:
						update_locs = []
						inner_ = -1
						try:
							sequence.remove('')
						except:
							pass
						for event in sequence:
							inner_ +=1
							rec = event.split('=')
							key,value = rec[0],rec[1]
							if key == '279':
								update_locs.append(inner_)
						for i in range(len(update_locs)):
							if len(update_locs) - 1 != i:
								ix,iy = update_locs[i],update_locs[i+1]
								for j in sequence[ix:iy]:
									rec = j.split('=')
									key,value = rec[0],rec[1]
									if key == '55': instrument = value
									if key == '83': rpt_seq = value
							elif len(update_locs) -1 == i:
								ix = update_locs[i]
								for j in sequence[ix:]:
									rec = j.split('=')
									key,value = rec[0],rec[1]

									if key == '55': instrument = value
									if key == '83': rpt_seq = (value)
							_ +=1
							if rpt_seq == self.rpt.get() and instrument == self.instr.get():
								print 'Lookup sequence found at packet: %s'%_
								return _

					except:
						print 'caught bad packet'
						pass
			print 'Something broke, maybe the cleaned_data/date is corrupt, re-run sort script for this day'
			return output

		def generate(vook):
			file_name = 'cleaned_data{}{}.txt'.format(self.slash,self.dayvar.get())
			beg = time.time()
			file_10 = open('key_pair.txt','w')
			df_count = 0
			capture_data = False
			_v = 0
			output = []
			input = csv.reader(open(file_name),delimiter = '\x01')
			with open(file_name, 'rU') as input:
				for sequence in csv.reader((line.replace('\0','') for line in input), delimiter="\x01"):
					try:
						update_locs = []
						inner_ = -1
						try:
							sequence.remove('')
						except:
							pass
						for event in sequence:
							inner_ +=1
							rec = event.split('=')
							key,value = rec[0],rec[1]
							if key == '34': seq = int(value)
							if key == '52': send_time = str(value)
							if key == '60':
								file_10.write("%s\n"%value)
								year = int(value[:4])
								month = int(value[4:6])
								day = int(value[6:8])
								event_time = str(value[:])
							if key == '279':
								update_locs.append(inner_)
						for i in range(len(update_locs)):
							if len(update_locs) - 1 != i:
								ix,iy = update_locs[i],update_locs[i+1]
								for j in sequence[ix:iy]:
									rec = j.split('=')
									key,value = rec[0],rec[1]

									if key == '269':
										if value in md_entry_dict.keys():
											md_entry = md_entry_dict[value]
										# if value in ['N','O','E','F']:
											# print value, 'WHOAH'
											# break
										# else:
											# break
									if key == '55': instrument = value
									if key == '270': price = float(value)
									if key == '271': quantity = int(value)
									if key == '346': orders = int(value)
									if key == '83': rpt_seq = value
									if key == '279':
										# if value
										if value in mdu_update_dict.keys():
											mdu_update = mdu_update_dict[value]
										if str(value) == '2':
											quantity = 0
											orders = 0
										else: md_update = ''
							elif len(update_locs) -1 == i:
								ix = update_locs[i]
								for j in sequence[ix:]:
									rec = j.split('=')
									key,value = rec[0],rec[1]
									if key == '269':
										if value in md_entry_dict.keys(): 
											md_entry = md_entry_dict[value]
										# if value in ['N','O','E','F']:
											# print value, 'WHOAH'
											# break


									if key == '55': instrument = value
									if key == '270': price = float(value)
									if key == '271': quantity = int(value)
									if key == '346': orders = int(value)
									if key == '83': rpt_seq = (value)
									if key == '279':
										if value in mdu_update_dict.keys():
											mdu_update = mdu_update_dict[value]
										if str(value) == '2':
											quantity = 0
											orders = 0
										else: md_update = ''
							# if rpt_seq == self.rpt.get() and instrument == self.instr.get():
							# 	print _v, 'oh'

							_v +=1
							# capture_data = True
							if _v == vook-int(self.lookback.get()):
								# print 'ah'
								capture_data = True
							# print instrument,'b4'
							if capture_data == True and df_count < int(self.lookback.get()) + int(self.evts.get()) + 10000 and md_entry not in ['Session High Bid','Session Low Offer'] and instrument in self.instruments.get().split(','):
								output.append([seq,year,month,day,event_time,send_time,rpt_seq,mdu_update,md_entry,instrument,price,quantity,orders])
								print instrument ,'success'
								df_count +=1
								# if instrument in self.instruments.get().split(','):
									# print instrument, self.instruments.get(),'ok'
								# print instrument

							if df_count >= int(self.lookback.get()) + int(self.evts.get()) + 10000:
								return output

					except:
						print 'oi'
						pass
			print 'bad run'
			return output

		inttime = time.time()
		lookback = int(self.lookback.get())-10
		_v = look()
		table = generate(_v)
		df = pd.DataFrame(table)


		print "Dataframe size of %s with %s lookback frames and %s future frames + 10000 (padding)"%( df.shape[0],int(lookback)+10, self.evts.get())
		df.columns = ['sequence','year','month','day','event_time','send_time','rpt_seq','mdu_update','md_entry','instrument','price','quantity','orders']
		df.ix[df.mdu_update == 'Delete', 'quantity'] = 0
		df.ix[df.mdu_update == 'Delete', 'orders'] = 0
		df = df.sort_values(['event_time','sequence','rpt_seq'])
		df = df.reset_index(drop=True)
		if self.dumpdf == True:
			pickle.dump(df,open('tempt.df','wb'))
		print 'All the instruments in lookback and forward are: ',list(df.instrument.unique())

		print 'Took %s minutes to load and transform the data'%(round( (float(time.time())-float(inttime))/60,2))
		file = open('output{}dict.txt'.format(self.slash),'w')
		file_2 = open('output{}events.txt'.format(self.slash),'w')
		file_3 = open('output{}times.txt'.format(self.slash),'w')
		file_4 = open('output{}instruments.txt'.format(self.slash),'w')
		file_5 = open('output{}volumes_test.txt'.format(self.slash),'w')
		file_trades = open('output{}trades.txt'.format(self.slash),'w')
		xx = int(self.evts.get())
		frame_loc = 'output{}objects'.format(self.slash)
		init_rpt = self.rpt.get()
		init_instr = self.instr.get()
		hard_instruments = self.instruments.get().strip(' ').split(',')

		for i in hard_instruments:
			file_4.write("%s\n"%i)

		def get_events_by_event_time(event_time,df):
			return df[df.event_time== event_time]


		def get_event_time_by_rpt_inst(rpt_seq,instrument,df):
			return df[(df.rpt_seq == rpt_seq)&(df.instrument == instrument)]['event_time'].max()

		def get_event_time_by_seq(sequence,df):
			event_time = df[(df.sequence == sequence)]['event_time'].max()
			return event_time

		def get_prev_event_time_by_event_time(event_time,df):
			prev_event_time = df[(df.event_time < event_time)]['event_time'].max()
			return prev_event_time

		def get_next_event_time_by_event_time(event_time,df):
			next_event_time = df[(df.event_time > event_time)]['event_time'].min()
			return next_event_time



		def get_next_x_event_times_by_event_time(event_time,x,df):
			x -=1
			event_list = [event_time]
			for i in range(x):
				event_time = get_next_event_time_by_event_time(event_time[i],df)
				event_list.append(event_time)



		def get_most_recent_order_by_type_for_instr_price_event_time(instrument,md_entry,price,event_time,df):
			last_q = df[(df.instrument == instrument)& (df.price == price) & (df.md_entry == md_entry) &
			   (df.event_time <= event_time)].tail(1)['orders'].max()
			return last_q

		def get_most_recent_quantity_by_type_for_instr_price_event_time(instrument,md_entry,price,event_time,df):
			last_q = df[(df.instrument == instrument)& (df.price == price) & (df.md_entry == md_entry) &
			   (df.event_time <= event_time)].tail(1)['quantity'].max()
			return last_q


		def get_all_prices_for_instr_before_event_time(instrument,event_time,df):

			all_prices = df[(df.instrument==instrument) & (df.event_time <= event_time)].price.unique()

			return all_prices



		def create_instr_price_dict(t1,df,hard_instruments,lookback):
			file_5 = open('output{}volumes.txt'.format(self.slash),'w')
			df_loc = get_events_by_event_time(t1,df).index[0]
			try:
				start_point = df_loc - lookback
			except:
				print 'Start point is before beginning of first event time, using 1000 value instead'
				start_point = df_loc - 1000
			print start_point, 'start'
			df_n = df.iloc[start_point-1:df_loc]
			df_n = df.iloc[:df_loc]

			order_offer_dict = {}
			order_bid_dict = {}
			order_trade_dict = {}


			quantity_offer_dict = {}
			quantity_bid_dict = {}
			quantity_trade_dict = {}

			volume_dict = {}
			instruments = list(df_n.instrument.unique())
			# print 'All the instruments in lookback are: ',instruments

			# hard_instruments = ['ESM7','ESU7']

			for instrument in hard_instruments:
				offer_price_dict = {}
				bid_price_dict = {}
				volume_price_dict = {}

				order_offer_price_dict = {}
				order_bid_price_dict = {}
				volume_q = instrument,df_n[(df_n.instrument == instrument) & (df_n.md_entry == 'Electronic Volume')].tail(1)['quantity'].max()
				# print volume_q
				file_5.write(str(volume_q[0]))
				file_5.write('|')
				file_5.write(str(volume_q[1]))
				file_5.write('\n')


				order_trade_dict[instrument] = {}
				quantity_trade_dict[instrument] = {}
				all_prices = get_all_prices_for_instr_before_event_time(instrument,t1,df_n)
				print all_prices, 'all prices'
				for price in all_prices:
					offer_quantity = get_most_recent_quantity_by_type_for_instr_price_event_time(instrument,'Offer',price,t1,df_n)
					bid_quantity = get_most_recent_quantity_by_type_for_instr_price_event_time(instrument,'Bid',price,t1,df_n)
					trade_quantity = get_most_recent_quantity_by_type_for_instr_price_event_time(instrument,'Trade',price,t1,df_n)
					order_bid_quantity = get_most_recent_order_by_type_for_instr_price_event_time(instrument,'Bid',price,t1,df_n)
					order_offer_quantity = get_most_recent_order_by_type_for_instr_price_event_time(instrument,'Offer',price,t1,df_n)
					volume_quantity = get_most_recent_order_by_type_for_instr_price_event_time(instrument,'Electronic Volume',price,t1,df_n)

					if str(volume_quantity) != 'nan' and str(volume_quantity) != '0':
						volume_price_dict[price] = volume_quantity
						volume_dict[instrument] = volume_price_dict
					if str(offer_quantity) != 'nan' and str(offer_quantity) != '0':
						offer_price_dict[price] = offer_quantity
						quantity_offer_dict[instrument] = offer_price_dict
					if str(bid_quantity) != 'nan' and str(bid_quantity) != '0':
						bid_price_dict[price] = bid_quantity
						quantity_bid_dict[instrument] = bid_price_dict

					if str(order_bid_quantity) != 'nan' and str(order_bid_quantity) != '0':
						order_bid_price_dict[price] = order_bid_quantity
						order_bid_dict[instrument] = order_bid_price_dict

					if str(order_offer_quantity) != 'nan' and str(order_offer_quantity) != '0':
						order_offer_price_dict[price] = order_offer_quantity
						order_offer_dict[instrument] = order_offer_price_dict

			file_5.close()
			return quantity_offer_dict,quantity_bid_dict,quantity_trade_dict,order_bid_dict,order_offer_dict,order_trade_dict,volume_dict

		def populate_first_frame(rpt_seq,instrument,df,file,file_2,hard_instruments,lookback):
			v1 = time.time()
			t1 = get_event_time_by_rpt_inst(rpt_seq,instrument,df)
			self.t1 = t1
			print t1, 'this event time'
			evts = get_events_by_event_time(t1,df)
			print evts, 'these events'
			instruments = evts.instrument.unique()
			print instruments, 'these instruments'
			quantity_offer_dict,quantity_bid_dict,quantity_trade_dict,order_bid_dict,order_offer_dict,order_trade_dict,volume_dict = create_instr_price_dict(t1,df,hard_instruments,lookback)
			print df.shape, 'df shape'
			print df.head() ,'df head'
			return t1,evts,quantity_offer_dict,quantity_bid_dict,quantity_trade_dict,order_bid_dict,order_offer_dict,order_trade_dict,volume_dict


		def generate_frame_for_seq(t1,df,seq,quantity_offer_dict,quantity_bid_dict,quantity_trade_dict,order_bid_dict,order_offer_dict,order_trade_dict,file,file_2,hard_instruments):
			v1 = time.time()
			seq = seq


			# lmv
			evts = get_events_by_event_time(t1,df)
			# hard_instruments = ['ESM7','ESU7']

			quantity_offer_dict,quantity_bid_dict,quantity_trade_dict,order_bid_dict,order_offer_dict,order_trade_dict = quantity_offer_dict,quantity_bid_dict,quantity_trade_dict,order_bid_dict,order_offer_dict,order_trade_dict
			for instrument in hard_instruments:
				unique_offer_prices = evts[(evts.md_entry=='Offer')& (evts.instrument==instrument) & (evts.rpt_seq==seq)]['price'].unique().tolist()
				unique_bid_prices = evts[(evts.md_entry=='Bid') & (evts.instrument == instrument)& (evts.rpt_seq==seq)]['price'].unique().tolist()
				unique_trade_prices = evts[(evts.md_entry=='Trade') & (evts.instrument == instrument)& (evts.rpt_seq==seq)]['price'].unique().tolist()


				if instrument in quantity_offer_dict.keys() and instrument in quantity_bid_dict.keys():
					offer_price_dict = quantity_offer_dict[instrument]
					bid_price_dict = quantity_bid_dict[instrument]
					order_offer_price_dict = order_offer_dict[instrument]
					order_bid_price_dict = order_bid_dict[instrument]


					for price in unique_offer_prices:
						offer_price_dict[price] = evts[(evts.price==price) & (evts.md_entry=='Offer')& (evts.rpt_seq==seq)]['quantity'].astype(float).sum()
						quantity_offer_dict[instrument] = offer_price_dict

						order_offer_price_dict[price] = evts[(evts.price==price) & (evts.md_entry=='Offer')& (evts.rpt_seq==seq)]['orders'].astype(float).sum()
						order_offer_dict[instrument] = order_offer_price_dict

					for price in unique_bid_prices:
						bid_price_dict[price] = evts[(evts.price==price) & (evts.md_entry == 'Bid')& (evts.rpt_seq==seq)]['quantity'].astype(float).sum()
						quantity_bid_dict[instrument] = bid_price_dict

						order_bid_price_dict[price] = evts[(evts.price==price) & (evts.md_entry == 'Bid')& (evts.rpt_seq==seq)]['orders'].astype(float).sum()
						order_bid_dict[instrument] = order_bid_price_dict

				if instrument in quantity_trade_dict.keys():
					trade_price_dict = quantity_trade_dict[instrument]
					for price in unique_trade_prices:
						trade_price_dict[price] = evts[(evts.price==price) & (evts.md_entry=='Trade')& (evts.rpt_seq==seq)]['quantity'].astype(float).sum()
						quantity_trade_dict[instrument] = trade_price_dict
			evts = evts[evts.rpt_seq==seq]
			return t1,evts,quantity_offer_dict,quantity_bid_dict,quantity_trade_dict,order_bid_dict,order_offer_dict,order_trade_dict

		def generate_next_x_frames(tx,df,quantity_offer_dict,quantity_bid_dict,quantity_trade_dict,order_bid_dict,order_offer_dict,order_trade_dict,x,file,file_2,file_3,file_trades,frame_loc,hard_instruments):
			pkl_c = 0
			time_x = 0
			iter_x = 0
			# recent_volume_dict = {}
			first_volume_file = open('output/volumes.txt')
			volume_details = {}
			for i in first_volume_file:
					# print i, 'hahahaha'
				try:
					volume_details[i.split('|')[0]] = int(i.split('|')[1].strip('\n'))
				except:
					print 'no lookup volume past for instrument' ,i.split('|')[0]
					volume_details[i.split('|')[0]] = 0
				# print volume_details, 'ohh'
			while iter_x < x:
				v1 = time.time()
				tx = get_next_event_time_by_event_time(tx,df)
				evts = get_events_by_event_time(tx,df)
				unique_instrs = list(evts['instrument'].unique())
				# hard_instruments = ['ESM7','ESU7']
				# print hard_instruments, 'hard', unique_instrs
				count_instruments = 0

				for instr in hard_instruments:
					if instr in unique_instrs:
						# recent_volume_dict[instr:1337]
						count_instruments +=1

				if count_instruments == 0:
					continue

				unique_sequences = list(evts['rpt_seq'].unique())
				unique_sequences.sort()
				# print unique_sequences
				file_2.write('-----------------------------------------------------------------------------------------\n')
				file_2.write('%s seconds takes: \n'%(time.time()-v1))

				sorted_evts = evts.sort_values(['sequence','rpt_seq'])

				for _,iv in sorted_evts[['instrument','rpt_seq','mdu_update','md_entry','price','quantity','sequence']].iterrows():

					file_2.write(str(iv['instrument']))
					file_2.write(' ')

					file_2.write(str(iv['rpt_seq']))
					file_2.write(' ')

					file_2.write(str(iv['sequence']))
					file_2.write('  ')

					file_2.write(str(iv['mdu_update']))
					file_2.write(' ')

					file_2.write(str(iv['md_entry']))
					file_2.write(' ')

					file_2.write(str(iv['price']))
					file_2.write(' ')

					file_2.write(str(iv['quantity']))
					file_2.write('\n')
				file_2.write('-----------------------------------------------------------------------------------------\n')



				for seq in unique_sequences:

					iter_x +=1
					t1 = time.time()

					file_3.write(str(tx)+'-'+str(time_x)+'\n')
					time_x +=1

					pkl_c +=1
					for instrument in evts.instrument.unique():
						quantity_trade_dict[instrument] = {}

					tx,evts,quantity_offer_dict,quantity_bid_dict,quantity_trade_dict,order_bid_dict,order_offer_dict,order_trade_dict = generate_frame_for_seq(tx,df,seq,quantity_offer_dict,quantity_bid_dict,quantity_trade_dict,order_bid_dict,order_offer_dict,order_trade_dict,file,file_2,hard_instruments)
					# volume_details = {}
					unique_instr = evts['instrument'].unique()
					# print unique_instr[0], hard_instruments
					# if unique_instr[0] not in hard_instruments:
					# 	print unique_instr[0], 'FGO!'
					# 	continue
					# print unique_instrs, hard_instruments, '~~'
					# count_instruments = 0
					# for instr in hard_instruments:
					# 	if instr in unique_instrs:
					# 		# recent_volume_dict[instr:1337]
					# 		count_instruments +=1

					# if count_instruments == 0:
					# 	continue
					# print evts
					if pkl_c % 100 == 0:
						diff = str(long(evts.event_time.unique()[0])- long(self.t1))
						v = ""
						final_diff = ""
						for _,i in enumerate(reversed(diff)):
							if _ % 3 == 0:
								 v += " | "
							v += i
						for i in reversed(v):
							final_diff += i
						print "Frame: ",pkl_c, ". Difference in event_times: ",final_diff, self.t1, evts.event_time.unique()[0]
					# most_recent_volume = 1337
					# for instrument in hard_instruments:
					# 	volume_details[instrument] = ''
					for instrument in hard_instruments:
						q = ''
						q = evts[(evts.md_entry=='Electronic Volume') & (evts.instrument == instrument)][['instrument','quantity']]
						# print pkl_c, q['quantity'].max()
						# print str(q['quantity'].max())
						dis =  str(q['quantity'].max())
						# print dis, dis == 'nan', dis[0] == 'n'
						if str(q['quantity'].max()) != 'nan':
							# print 
							volume_details[instrument] = int(q['quantity'].max())
							# volume_details[instrument] = 10
							# print q['quantity'].max()
						# if q['quantity'].max() == 'nan':
						# 	volume_details[instrument] = 20


					# print volume_details
						# volume_details[instrument] = most_recent_volume
		#                     str(q['instrument'].max()) + '-' + str(q['quantity'].max())

		#                 event_details[instrument] = {volume:q}

		#             if q['quantity'].max() != 'nan':
		#                 event_details['Electronic Volume'] = str(q['instrument'].max()) + '-' + str(q['quantity'].max())

					if evts.md_entry.unique()[0] == 'Trade':
						# print str(pkl_c)
						file_trades.write(str(pkl_c))
						file_trades.write('\n')
					event_details['Event Time'] = evts.event_time.unique()[0]
					event_details['Send Time'] = evts.send_time.unique()[0]
					event_details['Rpt Sequence'] = evts.rpt_seq.unique()[0]
					event_details['Sequence'] = evts.sequence.unique()[0]
					event_details['Instrument'] = evts.instrument.unique()[0]


					pickle.dump(quantity_offer_dict, open('{}{}offer_quantity_{}.pkl'.format(frame_loc,self.slash,pkl_c), 'wb'))
					pickle.dump(quantity_bid_dict, open('{}{}bid_quantity_{}.pkl'.format(frame_loc,self.slash,pkl_c), 'wb'))
					pickle.dump(quantity_trade_dict, open('{}{}trade_quantity_{}.pkl'.format(frame_loc,self.slash,pkl_c), 'wb'))

					pickle.dump(order_offer_dict, open('{}{}offer_order_{}.pkl'.format(frame_loc,self.slash,pkl_c), 'wb'))
					pickle.dump(order_bid_dict, open('{}{}bid_order_{}.pkl'.format(frame_loc,self.slash,pkl_c), 'wb'))
					pickle.dump(order_trade_dict, open('{}{}trade_order_{}.pkl'.format(frame_loc,self.slash,pkl_c), 'wb'))

					pickle.dump(event_details, open('{}{}details_{}.pkl'.format(frame_loc,self.slash,pkl_c), 'wb'))
					for instrument in hard_instruments:
						pickle.dump(volume_details[instrument], open('{}{}{}_volume_{}.pkl'.format(frame_loc,self.slash,instrument,pkl_c), 'wb'))

					for instr in hard_instruments:
						offer_vals = {}
						bid_vals = {}
						trade_vals = {}
						vals = []
						if instr in quantity_offer_dict.keys():
							for price in quantity_offer_dict[instr]:
								offer_vals[price] = quantity_offer_dict[instr][price]
								vals.append(price)
						if instr in quantity_bid_dict.keys():
							for price in quantity_bid_dict[instr]:
								bid_vals[price] = quantity_bid_dict[instr][price]
								vals.append(price)
						if instr in quantity_trade_dict.keys():
							for price in quantity_trade_dict[instr]:
								trade_vals[price] = quantity_trade_dict[instr][price]
								vals.append(price)
						vals = list(set(vals))
						vals.sort()
						vals.reverse()
						file.write('------------------------\n')
						file.write('Rpt Sequence: %s for event time %s for instrument %s'%(seq,tx,instr))
						file.write('\n')
						file.write('Instr Price    Type  Quant')
						file.write('\n')
						for val in vals:
							if val in offer_vals.keys() and float(offer_vals[val]) != 0.0:
								file.write("%s  %s  'offer'  %s"%(instr,val,offer_vals[val]))
								file.write('\n')
							if val in trade_vals.keys() and float(trade_vals[val]) != 0.0:
								file.write("%s  %s  'trade'  %s"%(instr,val,trade_vals[val]))
								file.write('\n')
							if val in bid_vals.keys() and float(bid_vals[val]) != 0.0:
								file.write("%s  %s  'bid'  %s"%(instr,val,bid_vals[val]))
								file.write('\n')

					file.write('------------------------\n')
					file.write('\nNEW EVENT\n')
					# print tx,time_x,time.time()-t1

		v1 = time.time()
		print hard_instruments,'hard_ins'
		t1,evts,quantity_offer_dict,quantity_bid_dict,quantity_trade_dict,order_bid_dict,order_offer_dict,order_trade_dict,volume_dict = populate_first_frame(init_rpt,init_instr,df,file,file_2,hard_instruments,lookback)
		print quantity_offer_dict, 'q_offer'
		print quantity_bid_dict, 'q_bid'

		event_details = {}
		event_details['Event Time'] = evts.event_time.unique()[0]
		event_details['Rpt Sequence'] = evts.rpt_seq.unique()[0]
		event_details['Sequence'] = evts.sequence.unique()[0]
		event_details['Instrument'] = evts.instrument.unique()[0]
		pickle.dump(quantity_offer_dict, open('{}{}offer_quantity_0.pkl'.format(frame_loc,self.slash), 'w'))
		pickle.dump(quantity_bid_dict, open('{}{}bid_quantity_0.pkl'.format(frame_loc,self.slash), 'w'))
		pickle.dump(quantity_trade_dict, open('{}{}trade_quantity_0.pkl'.format(frame_loc,self.slash), 'w'))
		pickle.dump(order_offer_dict, open('{}{}offer_order_0.pkl'.format(frame_loc,self.slash), 'w'))
		pickle.dump(order_bid_dict, open('{}{}bid_order_0.pkl'.format(frame_loc,self.slash), 'w'))
		pickle.dump(order_trade_dict, open('{}{}trade_order_0.pkl'.format(frame_loc,self.slash), 'w'))
		pickle.dump(event_details, open('{}{}details_0.pkl'.format(frame_loc,self.slash), 'w'))

		for instr in hard_instruments:
			if instr in quantity_offer_dict.keys() and instr in quantity_bid_dict.keys():
				offer_vals = {}
				bid_vals = {}
				vals = []
				for price in quantity_offer_dict[instr]:
					offer_vals[price] = quantity_offer_dict[instr][price]
					vals.append(price)
				for price in quantity_bid_dict[instr]:
					bid_vals[price] = quantity_bid_dict[instr][price]
					vals.append(price)
				vals = list(set(vals))
				vals.sort()
				vals.reverse()
				file.write('------------------------\n')
				file.write('Event Time: %s for instrument %s'%(t1,instr))
				file.write('\n')
				file.write('Instr Price  Type Quant')
				file.write('\n')
				for val in vals:
					if val in offer_vals.keys() and float(offer_vals[val]) != 0.0:
						file.write("%s  %s  'offer'  %s"%(instr,val,offer_vals[val]))
						file.write('\n')
					if val in bid_vals.keys() and float(bid_vals[val]) != 0.0:
						file.write("%s  %s  'bid'  %s"%(instr,val,bid_vals[val]))
						file.write('\n')
		t2 = str(get_prev_event_time_by_event_time(t1,df))




		generate_next_x_frames(t2,df,quantity_offer_dict,quantity_bid_dict,quantity_trade_dict,order_bid_dict,order_offer_dict,order_trade_dict,xx,file,file_2,file_3,file_trades,frame_loc,hard_instruments)
		# file.close()
		# file_2.close()

		print 'Finished, taking an entire time of %s minutes for %s frames' %(((float(time.time()) - float(inttime))/60),xx)

		print str(datetime.now()), 'Last line of Script'

	def __init__(self):
		if sys.platform.startswith('darwin'):
			self.slash = '/'
		if sys.platform.startswith('win32'):
			self.slash = '\\'
		self.begin()


MainApp()
