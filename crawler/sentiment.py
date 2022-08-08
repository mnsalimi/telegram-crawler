from transformers import MT5ForConditionalGeneration, MT5Tokenizer

class Sentiment:

    def __init__(self) -> None:
        self.model_name_or_path = "persiannlp/mt5-small-parsinlu-sentiment-analysis"
        self.tokenizer = MT5Tokenizer.from_pretrained(self.model_name_or_path)
        self.model = MT5ForConditionalGeneration.from_pretrained(self.model_name_or_path)

    def predict(self, query, **generator_args):
        input_ids = self.tokenizer.encode(query, return_tensors="pt")
        res = self.model.generate(input_ids, **generator_args)
        output = self.tokenizer.batch_decode(res, skip_special_tokens=True)
        return output[0]

if __name__ == "__main__":
    from time import time
    sentiment = Sentiment()
    t1 = time()
    res = sentiment.predict(
    "من آدم خوبی هستم و شما را نیز دوست دارم"
    )
    print(time()-t1)
    print(res)