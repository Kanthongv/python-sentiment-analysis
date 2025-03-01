from classifier import SentimentClassifier

cls = SentimentClassifier()

x = "Es un producto encantador y hermoso"
y = "Es una experiencia horrible"
z = "No tengo nada que decir. Normal hasta ahora."

#cls.train()

print(cls.predict(x))
print(cls.predict(y))
print(cls.predict(z))



