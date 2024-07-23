class Character:
	# Thuộc tính (attributes)
	def __init__(self, hair_color, age):
		self.hair_color = hair_color
		self.age = age
		self.genger = "Male"

	# Phương thức (methods)
	def punch(self):
		return "Mất 50 máu"

	def kick(self):
		print("Mất 30 máu")

songoku = Character("black", 30)
vegeta = Character("black", 27)

songoku.punch()
print(songoku.punch())