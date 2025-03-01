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

dframe = pd.read_csv("data/reviews.csv")

print(dframe.head())

sid = SentimentIntensityAnalyzer()
dframe["sentimiento"] = dframe["mensaje"].apply(lambda x: sid.polarity_scores(x)["compound"])

# Export to csv
df.to_csv("output/salida-con-sentimiento.csv")
print(df)






