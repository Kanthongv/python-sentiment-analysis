# Solo sirve para inglés

from nltk.sentiment.vader import SentimentIntensityAnalyzer

x = "It is a charming and beautifull product"
y = "It was an horrible experience"
z = "I have nothing to say. Normal so far."

#analyzer = SentimentIntensityAnalyzer()

# print(analyzer.polarity_scores(x))
# print(analyzer.polarity_scores(y))
# print(analyzer.polarity_scores(z))

# File sentiment analysis
import pandas as pd

df = pd.read_csv("data/reviews.csv")

print(df.head())

sid = SentimentIntensityAnalyzer()
df["sentimiento"] = df["mensaje"].apply(lambda x: sid.polarity_scores(x)["compound"])

# Export to csv
df.to_csv("salida-con-sentimiento.csv")
print(df)






