from vk_api.keyboard import VkKeyboard, VkKeyboardColor

keyboard_empty = {}

keyboard_idle = {
	'Ожидайте...' : VkKeyboardColor.SECONDARY
}

keyboard_back = {
	'Вернуться' : VkKeyboardColor.NEGATIVE
}

keyboard_main = {
	'Сменить планету' : VkKeyboardColor.POSITIVE,
	'Вылазка' : VkKeyboardColor.PRIMARY,
	1 : '',
	'Статус корабля' : VkKeyboardColor.SECONDARY,
	2 : '',
	'Выгрузка инвентаря' : VkKeyboardColor.SECONDARY,
	3 : '',
	'Покинуть планетную систему' : VkKeyboardColor.NEGATIVE
}

keyboard_sortie = {
	'Добыча' : VkKeyboardColor.POSITIVE,
	'Исследование' : VkKeyboardColor.PRIMARY,
	'Бой' : VkKeyboardColor.NEGATIVE,
	1 : '',
	'Назад' : VkKeyboardColor.SECONDARY
}

keyboard_system = {
	10 : ['Андромеда', VkKeyboardColor.PRIMARY],
	20 : ['Пиксель', VkKeyboardColor.PRIMARY]
	# 30 : ['X', VkKeyboardColor.PRIMARY],
	# 40 : ['Шалом', VkKeyboardColor.PRIMARY],
	# 50 : ['Охаё', VkKeyboardColor.PRIMARY]
}

keyboard_planets1 = {
	10 : ['Станция', VkKeyboardColor.PRIMARY],
	11 : ['AR-800', VkKeyboardColor.POSITIVE],
	12 : ['GX-25-70', VkKeyboardColor.POSITIVE],
	13 : ['SUN-1', VkKeyboardColor.POSITIVE]
}

keyboard_planets2 = {
	20 : ['Станция', VkKeyboardColor.PRIMARY],
	21 : ['Leroy', VkKeyboardColor.POSITIVE],
	22 : ['Bally-01', VkKeyboardColor.POSITIVE],
	23 : ['Keros', VkKeyboardColor.POSITIVE],
	24 : ['Simlo-2', VkKeyboardColor.POSITIVE],
	25 : ['Delo', VkKeyboardColor.POSITIVE]
}

keyboard_hotel = {
	'Привет' : VkKeyboardColor.POSITIVE,
	1 : '',
	'Инвентарь' : VkKeyboardColor.SECONDARY,
	2 : '',
	'В город' : VkKeyboardColor.NEGATIVE
}