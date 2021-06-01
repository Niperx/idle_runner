from vk_api.keyboard import VkKeyboard, VkKeyboardColor

keyboard_empty = {}

keyboard_idle = {
	'Ожидайте...' : VkKeyboardColor.SECONDARY
}

keyboard_main = {
	'Сменить планету' : VkKeyboardColor.POSITIVE,
	'Вылазка' : VkKeyboardColor.PRIMARY,
	1 : '',
	'Статус корабля' : VkKeyboardColor.SECONDARY,
	2 : '',
	'Покинуть планетную систему' : VkKeyboardColor.NEGATIVE
}

keyboard_sortie = {
	'Добыча' : VkKeyboardColor.POSITIVE,
	'Исследование' : VkKeyboardColor.PRIMARY,
	'Бой' : VkKeyboardColor.NEGATIVE,
	1 : '',
	'Назад' : VkKeyboardColor.SECONDARY
}

keyboard_planets = {
	'AR-800' : VkKeyboardColor.POSITIVE,
	'GX-25-70' : VkKeyboardColor.POSITIVE,
	'SUN-1' : VkKeyboardColor.NEGATIVE,
	1 : '',
	'Назад' : VkKeyboardColor.SECONDARY
}

keyboard_sys_escape = {
	'AR-800' : VkKeyboardColor.POSITIVE,
	'GX-25-70' : VkKeyboardColor.POSITIVE,
	'SUN-1' : VkKeyboardColor.NEGATIVE,
	1 : '',
	'Назад' : VkKeyboardColor.SECONDARY
}



keyboard_test = {
	'Сменить планету' : VkKeyboardColor.PRIMARY,
	'Вылазка' : VkKeyboardColor.POSITIVE,
	1 : '',
	'Статус корабля' : VkKeyboardColor.PRIMARY,
	'К развлечениям' : VkKeyboardColor.POSITIVE,
}

keyboard_hotel = {
	'Привет' : VkKeyboardColor.POSITIVE,
	1 : '',
	'Инвентарь' : VkKeyboardColor.SECONDARY,
	2 : '',
	'В город' : VkKeyboardColor.NEGATIVE
}