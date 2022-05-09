import LuckyFunction

exit = 0
up = 1
weapon = 2
common = 3
url_common = 'https://webstatic.mihoyo.com/hk4e/gacha_info/cn_gf01/cbca8b58edaea048a628aa2ecfe20204f69696/zh-cn.json?2'
url_weapon = 'https://webstatic.mihoyo.com/hk4e/gacha_info/cn_gf01/db9eddc6811aa7170b49f251fa5c488e030bd7/zh-cn.json?'
url_up = 'https://webstatic.mihoyo.com/hk4e/gacha_info/cn_gf01/eaa07ae07196ca35c36b48213560ab6df7617e/zh-cn.json?'

LuckyFunction.InitWindows()
while 1:
	print('请输入所需要进行的操作：0代表退出，1代表up池，2代表武器池，3代表常驻池')
	commend = int(input('please enter a commend:'))
	if commend == exit:
		LuckyFunction.ExitWindows()
		break
	elif commend == up:
		LuckyUp = LuckyFunction.Lucky(url=url_up)
		LuckyUp.lucky()
	elif commend == weapon:
		LuckyWeapon = LuckyFunction.Lucky(url=url_weapon)
		LuckyWeapon.lucky()
	elif commend == common:
		LuckyCommon = LuckyFunction.Lucky(url=url_common)
		LuckyCommon.lucky()
	else:
		print('Commend Error')
		print('Please try again')
