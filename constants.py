"""
Este módulo contiene las constantes utilizadas a lo largo del sistema.
"""

user_types = {
	"normal": "normal",
	"vendor": "vendor",
	"admin": "admin"
}
order_states = {
	"pending": "pending",
	"done": "done"
}

admitted_users = (user_types['normal'], user_types['vendor'])
rating_values = (1, 2, 3, 4, 5)
admitted_order_states = (order_states['done'],)
