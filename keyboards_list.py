from vk_api.keyboard import VkKeyboard, VkKeyboardColor

keyboard_empty = {}

keyboard_idle = {
	'Ожидайте...' : VkKeyboardColor.SECONDARY
}

keyboard_city = {
	'В отель' : VkKeyboardColor.PRIMARY,
	'В ТРЦ Ситимолл' : VkKeyboardColor.POSITIVE,
	1 : '',
	'В DNS' : VkKeyboardColor.PRIMARY,
	'К развлечениям' : VkKeyboardColor.POSITIVE,
}

keyboard_hotel = {
	'Привет' : VkKeyboardColor.POSITIVE,
	1 : '',
	'Инвентарь' : VkKeyboardColor.SECONDARY,
	2 : '',
	'В город' : VkKeyboardColor.NEGATIVE
}