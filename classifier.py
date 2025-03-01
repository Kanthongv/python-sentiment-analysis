class SentimentClassifier:
    def __init__(self):
        # Spanish sentiment words
        self.positive_words = [
            "bueno", "excelente", "fantástico", "increíble", "maravilloso",
            "genial", "encantador", "hermoso", "agradable", "feliz",
            "positivo", "satisfecho", "contento", "alegre", "perfecto"
        ]
        
        self.negative_words = [
            "malo", "terrible", "horrible", "pésimo", "desagradable",
            "defectuoso", "decepcionante", "triste", "negativo", "enfadado",
            "enojado", "frustrado", "inútil", "peor", "fatal"
        ]
    
    def predict(self, text):
        text = text.lower()
        
        # Count positive and negative words
        positive_count = sum(1 for word in self.positive_words if word in text)
        negative_count = sum(1 for word in self.negative_words if word in text)
        
        # Calculate sentiment score
        if positive_count > negative_count:
            label = "POSITIVE"
            score = positive_count / (positive_count + negative_count + 0.1)
        elif negative_count > positive_count:
            label = "NEGATIVE"
            score = negative_count / (positive_count + negative_count + 0.1)
        else:
            label = "NEUTRAL"
            score = 0.5
            
        return {"label": label, "score": score}
    
    def train(self):
        print("This is a rule-based classifier, no training needed.") 