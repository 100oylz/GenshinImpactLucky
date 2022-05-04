import json
import random

import pandas as pd
import requests

headers = {
	'useragent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36'}


class Pond:
	def __init__(self, url, name):
		self.name = name
		self.response = requests.get(url=url, headers=headers)
		self.raw = json.loads(self.response.text)
		self.r3_prob_list = self.raw['r3_prob_list']
		self.r4_prob_list = self.raw['r4_prob_list']
		self.r5_prob_list = self.raw['r5_prob_list']
		self.content = self.raw['content']
		self.title = self.raw['title']
		self.dictionary = []
		self.r4_prob_figure = []
		self.r4_prob_weapon = []
		self.r5_prob_figure = []
		self.r5_prob_weapon = []
		self.r4_up = []
		self.r5_up = []
		self.r5_common = []
		self.r4_common = []
	
	def Text(self):
		print(self.content)
	
	def Items(self):
		for item in self.r3_prob_list:
			print('3:', end='')
			print(item)
		for item in self.r4_prob_list:
			print('4:', end='')
			print(item)
		for item in self.r5_prob_list:
			print('5:', end='')
			print(item)
	
	def Easy(self):
		for obj in self.r3_prob_list:
			del obj['item_id'], obj['order_value']
			self.dictionary.append(obj)
		for obj in self.r4_prob_list:
			del obj['item_id'], obj['order_value']
			self.dictionary.append(obj)
		for obj in self.r5_prob_list:
			del obj['item_id'], obj['order_value']
			self.dictionary.append(obj)
	
	def ToExcel(self):
		database = pd.DataFrame(self.dictionary)
		database.to_excel(f'{self.name}.xlsx')
	
	def Select(self):
		for obj in self.r5_prob_list:
			if obj['is_up'] == 1:
				self.r5_up.append(obj)
			else:
				self.r5_common.append(obj)
			if obj['item_type'] == '武器':
				self.r5_prob_weapon.append(obj)
			else:
				self.r5_prob_figure.append(obj)
		for obj in self.r4_prob_list:
			if obj['is_up'] == 1:
				self.r4_up.append(obj)
			else:
				self.r4_common.append(obj)
			if obj['item_type'] == '武器':
				self.r4_prob_weapon.append(obj)
			else:
				self.r4_prob_figure.append(obj)


class Lucky(Pond):
	luckybreak = 0
	luckyone = 1
	luckyten = 2
	little = 0
	big = 1
	
	def __init__(self, url, name):
		super().__init__(url=url, name=name)
		self.choice = ''
		self.is_up_5 = 0
		self.is_4 = 0
		self.up_history = 0
		self.weapon_history = 0
		self.common_history = 0
		self.dinggui = {}
		self.Select()
	
	def InitWindows(self):
		print('* ' * 20)
		print(' *' * 20)
		print(
			'* ' * round((20 - len(self.name) / 2) / 2) + f"{self.name}" + ' *' * round((20 - len(self.name) / 2) / 2))
		print('* ' * 20)
		print(' *' * 20)
	
	def ExitWindows(self):
		print('* ' * 20)
		print(' *' * 20)
		print(f'* ' * 9 + "Exit" + ' *' * 9)
		print('* ' * 20)
		print(' *' * 20)
	
	def lucky(self):
		self.InitWindows()
		print('')
		print('')
		print('0代表退出，1代表单抽，2代表十连')
		while (1):
			commend = int(input('please enter a commond'))
			if commend == self.luckybreak:
				self.ExitWindows()
				break
			elif commend == self.luckyone:
				if 'up' in self.name:
					self.up_history += 1  # up池抽奖次数
					print(self.up_history)
					i = random.randint(0, 90 - self.up_history % 90)  # 随次数增加而概率增加
					if (i == 0):  # 抽到五星
						self.up_history = 0  # 重置五星计数器
						if self.is_up_5 == self.big:
							self.is_up_5 = self.little  # 下一次是小保底
							self.choice = random.choice(self.r5_up)
							print('' + self.choice['item_name'] + '')
						j = random.randint(0, 2)  # 五星up概率抽奖
						if (j == 0):
							self.is_up_5 = self.little  # 下一次是小保底
							self.choice = random.choice(self.r5_up)
							print('' + self.choice['item_name'] + '')
						elif (j == 1):
							self.is_up_5 = self.big  # 下一次是大保底
							self.choice = random.choice(self.r5_common)
							print('' + self.choice['item_name'] + '')
					elif i % 10 == 0:
						self.choice = random.choice(self.r4_prob_list)
						print('' + self.choice['item_name'] + '')
					else:
						i = random.randint(0, 1000)
						if i in range(0, 6):
							self.up_history = 0
							self.choice = random.choice(self.r5_common)
							print('' + self.choice['item_name'] + '')
						elif i in range(6, 32):
							self.choice = random.choice(self.r4_prob_figure)
							print('' + self.choice['item_name'] + '')
						elif i in range(32, 57):
							self.choice = random.choice(self.r4_prob_weapon)
							print('' + self.choice['item_name'] + '')
						elif i in range(57, 1000):
							self.choice = random.choice(self.r3_prob_list)
							print('' + self.choice['item_name'] + '')
				elif 'weapon' in self.name:
					self.weapon_history += 1  # 武器池抽奖次数
					print(self.weapon_history)
					i = random.randint(0, 90 - self.weapon % 90)  # 随次数增加而概率增加
					if (i == 0):  # 抽到五星
						self.weapon_history = 0  # 重置五星计数器
						if self.is_up_5 == self.big:
							self.is_up_5 = self.little  # 下一次是小保底
							self.choice = random.choice(self.r5_up)
							print('' + self.choice['item_name'] + '')
						j = random.randint(0, 2)  # 五星up概率抽奖
						if (j == 0):
							self.is_up_5 = self.little  # 下一次是小保底
							self.choice = random.choice(self.r5_up)
							print('' + self.choice['item_name'] + '')
						elif (j == 1):
							self.is_up_5 = self.big  # 下一次是大保底
							self.choice = random.choice(self.r5_common)
							print('' + self.choice['item_name'] + '')
					elif i % 10 == 0:
						self.choice = random.choice(self.r4_prob_list)
						print('' + self.choice['item_name'] + '')
					else:
						i = random.randint(0, 1000)
						if i in range(0, 6):
							self.weapon_history = 0
							self.choice = random.choice(self.r5_common)
							print('' + self.choice['item_name'] + '')
						elif i in range(6, 57):
							self.choice = random.choice(self.r4_prob_weapon)
							print('' + self.choice['item_name'] + '')
						elif i in range(57, 1000):
							self.choice = random.choice(self.r3_prob_list)
							print('' + self.choice['item_name'] + '')
				elif 'common' in self.name:
					self.common_history += 1  # 武器池抽奖次数
					print(self.common_history)
					i = random.randint(0, 90 - self.common_history % 90)  # 随次数增加而概率增加
					if (i == 0):  # 抽到五星
						self.common_history = 0  # 重置五星计数器
						self.choice = random.choice(self.r5_prob_list)
						print('' + self.choice['item_name'] + '')
					i = random.randint(0, 1000)
					if i in range(0, 6):
						self.common_history = 0
						self.choice = random.choice(self.r5_common)
						print('' + self.choice['item_name'] + '')
					elif i in range(6, 32):
						self.choice = random.choice(self.r4_prob_figure)
						print('' + self.choice['item_name'] + '')
					elif i in range(32, 57):
						self.choice = random.choice(self.r4_prob_weapon)
						print('' + self.choice['item_name'] + '')
					elif i in range(57, 1000):
						self.choice = random.choice(self.r3_prob_list)
						print('' + self.choice['item_name'] + '')
			elif commend == self.luckyten:
				if 'up' in self.name:
					for k in range(10):
						self.up_history += 1  # up池抽奖次数
						print(self.up_history)
						i = random.randint(0, 90 - self.up_history % 90)  # 随次数增加而概率增加
						if (i == 0):  # 抽到五星
							self.up_history = 0  # 重置五星计数器
							if self.is_up_5 == self.big:
								self.is_up_5 = self.little  # 下一次是小保底
								self.choice = random.choice(self.r5_up)
								print('' + self.choice['item_name'] + '')
							j = random.randint(0, 2)  # 五星up概率抽奖
							if (j == 0):
								self.is_up_5 = self.little  # 下一次是小保底
								self.choice = random.choice(self.r5_up)
								print('' + self.choice['item_name'] + '')
							elif (j == 1):
								self.is_up_5 = self.big  # 下一次是大保底
								self.choice = random.choice(self.r5_common)
								print('' + self.choice['item_name'] + '')
						elif i % 10 == 0:
							self.choice = random.choice(self.r4_prob_list)
							print('' + self.choice['item_name'] + '')
						else:
							i = random.randint(0, 1000)
							if i in range(0, 6):
								self.up_history = 0
								self.choice = random.choice(self.r5_common)
								print('' + self.choice['item_name'] + '')
							elif i in range(6, 32):
								self.choice = random.choice(self.r4_prob_figure)
								print('' + self.choice['item_name'] + '')
							elif i in range(32, 57):
								self.choice = random.choice(self.r4_prob_weapon)
								print('' + self.choice['item_name'] + '')
							elif i in range(57, 1000):
								self.choice = random.choice(self.r3_prob_list)
								print('' + self.choice['item_name'] + '')
				elif 'weapon' in self.name:
					for k in range(10):
						self.weapon_history += 1  # 武器池抽奖次数
						print(self.weapon_history)
						i = random.randint(0, 90 - self.weapon_history % 90)  # 随次数增加而概率增加
						if (i == 0):  # 抽到五星
							self.weapon_history = 0  # 重置五星计数器
							if self.is_up_5 == self.big:
								self.is_up_5 = self.little  # 下一次是小保底
								self.choice = random.choice(self.r5_up)
								print(self.choice['item_name'])
							j = random.randint(0, 2)  # 五星up概率抽奖
							if (j == 0):
								self.is_up_5 = self.little  # 下一次是小保底
								self.choice = random.choice(self.r5_up)
								print(self.choice['item_name'])
							elif (j == 1):
								self.is_up_5 = self.big  # 下一次是大保底
								self.choice = random.choice(self.r5_common)
								print(self.choice['item_name'])
						elif i % 10 == 0:
							self.choice = random.choice(self.r4_prob_list)
							print(self.choice['item_name'])
						else:
							i = random.randint(0, 1000)
							if i in range(0, 6):
								self.weapon_history = 0
								self.choice = random.choice(self.r5_common)
								print(self.choice['item_name'])
							elif i in range(6, 57):
								self.choice = random.choice(self.r4_prob_weapon)
								print(self.choice['item_name'])
							elif i in range(57, 1000):
								self.choice = random.choice(self.r3_prob_list)
								print(self.choice['item_name'])
				elif 'common' in self.name:
					for k in range(10):
						self.common_history += 1  # 武器池抽奖次数
						print(self.common_history)
						i = random.randint(0, 90 - self.common_history % 90)  # 随次数增加而概率增加
						if (i == 0):  # 抽到五星
							self.common_history = 0  # 重置五星计数器
							self.choice = random.choice(self.r5_prob_list)
							print(self.choice['item_name'])
						i = random.randint(0, 1000)
						if i in range(0, 6):
							self.common_history = 0
							self.choice = random.choice(self.r5_common)
							print(self.choice['item_name'])
						elif i in range(6, 32):
							self.choice = random.choice(self.r4_prob_figure)
							print(self.choice['item_name'])
						elif i in range(32, 57):
							self.choice = random.choice(self.r4_prob_weapon)
							print(self.choice['item_name'])
						elif i in range(57, 1000):
							self.choice = random.choice(self.r3_prob_list)
							print(self.choice['item_name'])
			else:
				print('Commend Error')
				print('Please try again')


def InitWindows():
	print('* ' * 20)
	print(' *' * 20)
	print('* ' * 20)
	print('* ' * 6 + '欢迎使用原神抽卡模拟器' + ' *' * 6)
	print(' *' * 20)
	print('* ' * 20)
	print(' *' * 20)
	print('* ' * 20)
	print(' *' * 20)


def ExitWindows():
	print('* ' * 20)
	print(' *' * 20)
	print('* ' * 20)
	print('* ' * 6 + '感谢使用原神抽卡模拟器' + ' *' * 6)
	print(' *' * 20)
	print('* ' * 20)
	print(' *' * 20)
	print('* ' * 20)
	print(' *' * 20)


exit = 0
up = 1
weapon = 2
common = 3
url_common = 'https://webstatic.mihoyo.com/hk4e/gacha_info/cn_gf01/cbca8b58edaea048a628aa2ecfe20204f69696/zh-cn.json?ts=1648597697'
url_weapon = 'https://webstatic.mihoyo.com/hk4e/gacha_info/cn_gf01/db9eddc6811aa7170b49f251fa5c488e030bd7/zh-cn.json?ts=1648598032'
url_up = 'https://webstatic.mihoyo.com/hk4e/gacha_info/cn_gf01/eaa07ae07196ca35c36b48213560ab6df7617e/zh-cn.json?ts=1648597985'

InitWindows()
while 1:
	print('请输入所需要进行的操作：0代表退出，1代表up池，2代表武器池，3代表常驻池')
	commend = int(input('please enter a commend:'))
	if commend == exit:
		ExitWindows()
		break
	elif commend == up:
		LuckyUp = Lucky(url=url_up, name='2.6up')
		LuckyUp.lucky()
	elif commend == weapon:
		LuckyWeapon = Lucky(url=url_weapon, name='2.6weapon')
		LuckyWeapon.lucky()
	elif commend == common:
		LuckyCommon = Lucky(url=url_common, name='2.6common')
		LuckyCommon.lucky()
	else:
		print('Commend Error')
		print('Please try again')
