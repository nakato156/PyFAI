from app.classes import Train, Juego

juego = Juego()

train = Train(juego, 0.1, 0.9, 5000)
train.train()

print(train.q_table)
