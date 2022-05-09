from os import mkdir
from os.path import exists
from json import loads
from random import randint, choice
from re import compile

from openpyxl import Workbook
from requests import get

headers = {
	'useragent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36'}


class Pond:
	def __init__(self, url):
		self.response = get(url=url, headers=headers)
		self.raw = loads(self.response.text)
		self.r3_prob_list = self.raw['r3_prob_list']
		self.r4_prob_list = self.raw['r4_prob_list']
		self.r5_prob_list = self.raw['r5_prob_list']
		self.content = self.raw['content']
		self.title = self.raw['title']
		select = compile(r'.*?(<.*?>).*?')
		result = select.findall(self.title)
		for res in result:
			self.title = self.title.replace(res, '')
		self.dictionary = []
		self.r4_prob_figure = []
		self.r4_prob_weapon = []
		self.r5_prob_figure = []
		self.r5_prob_weapon = []
		self.r4_up = []
		self.r5_up = []
		self.r5_common = []
		self.r4_common = []
		self.type = ''

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

	# def ToExcel(self):
	# 	if not (exists('祈愿详情')):
	# 		mkdir('祈愿详情')
	# 	Sheet = Workbook()
	# 	sheet = Sheet.active
	# 	header = []
	# 	data = []
	# 	for key in self.dictionary[0].keys():
	# 		print(key)
	# 		header.append(key)
	# 	for dict in self.dictionary:
	# 		List = []
	# 		for value in dict.values():
	# 			List.append(value)
	# 		data.append(List)
	# 		del List
	# 	data.insert(0, header)
	# 	rows = len(data)
	# 	columns = len(data[0])
	# 	for i in range(rows):
	# 		for j in range(columns):
	# 			sheet.cell(row=i + 1, column=j + 1).value = data[i][j]
	# 	Sheet.save(f'祈愿详情\{self.title}.xlsx')

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
		print(self.r5_up)
		if self.r5_up == []:
			self.type = 'common'
		elif self.r5_up[0]['item_type'] == '武器':
			self.type = 'weapon'
		elif self.r5_up[0]['item_type'] == '角色':
			self.type = 'up'
		else:
			self.type = ''


class Lucky(Pond):
	luckybreak = 0
	luckyone = 1
	luckyten = 2
	little = 0
	big = 1

	def __init__(self, url):
		super().__init__(url=url)
		self.Easy()
		self.Select()
		# self.ToExcel()
		self.choice = ''
		self.is_up_5 = 0
		self.is_4 = 0
		self.up_history = 0
		self.weapon_history = 0
		self.common_history = 0
		self.dinggui = {}

	def InitWindows(self):
		print('* ' * 20)
		print(' *' * 20)
		print(
			'* ' * round((20 - len(self.title) / 2) / 2) + f"{self.title}" + ' *' * round(
				(20 - len(self.title) / 2) / 2))
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
				if 'up' == self.tyoe:
					self.LuckyUpMethod()
				elif 'weapon' == self.type:
					self.LuckyWeaponMethod()
				elif 'common' == self.type:
					self.LuckyCommonMethod()
			elif commend == self.luckyten:
				if 'up' == self.type:
					for k in range(10):
						self.LuckyUpMethod()
						self.Log()
				elif 'weapon' == self.type:
					for k in range(10):
						self.LuckyWeaponMethod()
						self.Log()
				elif 'common' == self.type:
					for k in range(10):
						self.LuckyCommonMethod()
						self.Log()
				else:
					print('error')
			else:
				print('Commend Error')
				print('Please try again')

	def LuckyUpMethod(self):
		self.up_history += 1  # up池抽奖次数
		print(self.up_history)
		i = randint(0, 90 - self.up_history % 90)  # 随次数增加而概率增加
		if (i == 0):  # 抽到五星
			self.up_history = 0  # 重置五星计数器
			if self.is_up_5 == self.big:
				self.is_up_5 = self.little  # 下一次是小保底
				self.choice = choice(self.r5_up)
				print('' + self.choice['item_name'] + '')
			j = randint(0, 2)  # 五星up概率抽奖
			if (j == 0):
				self.is_up_5 = self.little  # 下一次是小保底
				self.choice = choice(self.r5_up)
				print('' + self.choice['item_name'] + '')
			elif (j == 1):
				self.is_up_5 = self.big  # 下一次是大保底
				self.choice = choice(self.r5_common)
				print('' + self.choice['item_name'] + '')
		elif i % 10 == 0:
			self.choice = choice(self.r4_prob_list)
			print('' + self.choice['item_name'] + '')
		else:
			i = randint(0, 1000)
			if i in range(0, 6):
				self.up_history = 0
				self.choice = choice(self.r5_common)
				print('' + self.choice['item_name'] + '')
			elif i in range(6, 32):
				self.choice = choice(self.r4_prob_figure)
				print('' + self.choice['item_name'] + '')
			elif i in range(32, 57):
				self.choice = choice(self.r4_prob_weapon)
				print('' + self.choice['item_name'] + '')
			elif i in range(57, 1000):
				self.choice = choice(self.r3_prob_list)
				print('' + self.choice['item_name'] + '')

	def LuckyWeaponMethod(self):
		self.weapon_history += 1  # 武器池抽奖次数
		print(self.weapon_history)
		i = randint(0, 90 - self.weapon_history % 90)  # 随次数增加而概率增加
		if (i == 0):  # 抽到五星
			self.weapon_history = 0  # 重置五星计数器
			if self.is_up_5 == self.big:
				self.is_up_5 = self.little  # 下一次是小保底
				self.choice = choice(self.r5_up)
				print(self.choice['item_name'])
			j = randint(0, 2)  # 五星up概率抽奖
			if (j == 0):
				self.is_up_5 = self.little  # 下一次是小保底
				self.choice = choice(self.r5_up)
				print(self.choice['item_name'])
			elif (j == 1):
				self.is_up_5 = self.big  # 下一次是大保底
				self.choice = choice(self.r5_common)
				print(self.choice['item_name'])
		elif i % 10 == 0:
			self.choice = choice(self.r4_prob_list)
			print(self.choice['item_name'])
		else:
			i = randint(0, 1000)
			if i in range(0, 6):
				self.weapon_history = 0
				self.choice = choice(self.r5_common)
				print(self.choice['item_name'])
			elif i in range(6, 57):
				self.choice = choice(self.r4_prob_weapon)
				print(self.choice['item_name'])
			elif i in range(57, 1000):
				self.choice = choice(self.r3_prob_list)
				print(self.choice['item_name'])

	def LuckyCommonMethod(self):
		self.common_history += 1  # 武器池抽奖次数
		print(self.common_history)
		i = randint(0, 90 - self.common_history % 90)  # 随次数增加而概率增加
		if (i == 0):  # 抽到五星
			self.common_history = 0  # 重置五星计数器
			self.choice = choice(self.r5_prob_list)
			print(self.choice['item_name'])
		i = randint(0, 1000)
		if i in range(0, 6):
			self.common_history = 0
			self.choice = choice(self.r5_common)
			print(self.choice['item_name'])
		elif i in range(6, 32):
			self.choice = choice(self.r4_prob_figure)
			print(self.choice['item_name'])
		elif i in range(32, 57):
			self.choice = choice(self.r4_prob_weapon)
			print(self.choice['item_name'])
		elif i in range(57, 1000):
			self.choice = choice(self.r3_prob_list)
			print(self.choice['item_name'])

	def Log(self):
		if not exists('History'):
			mkdir('History')
		if self.type == 'up':
			with open(f'History/{self.title}.txt', 'a')as fp:
				fp.write(f'{self.choice["rank"]}星   {self.choice["item_name"]}   {self.up_history}次\n')
		elif self.type == 'weapon':
			with open(f'History/{self.title}.txt', 'a')as fp:
				fp.write(f'{self.choice["rank"]}星   {self.choice["item_name"]}   {self.weapon_history}次\n')
		elif self.type == 'common':
			with open(f'History/{self.title}.txt', 'a', encoding='utf-8')as fp:
				fp.write(f'{self.choice["rank"]}星   {self.choice["item_name"]}   {self.common_history}次\n')


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
