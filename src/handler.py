import string
from fuzzywuzzy import process

from requester import ModelRequester


class Handler:
    def __init__(self, car_brands: tuple[str, ...], path_to_swear_words: str, requester: ModelRequester):
        self.corpus = self.load_swear_words(path=path_to_swear_words)
        self.car_brands = car_brands
        self.requester = requester

    @staticmethod
    def load_swear_words(path: str) -> list[str]:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read().split('\n')

    def check_over_brands(self, words: list[str]) -> tuple[bool, str]:
        for word in words:
            if word in self.car_brands:
                return False, "Извините, но мы предоставляем информацию только по Mercedes."
        return True, ""

    def check_profanity(self, words: list[str], threshold: int = 85) -> tuple[bool, str]:
        for word in words:
            match, similarity = process.extractOne(word, self.corpus)
            if len(word) < 3 or abs(len(word) - len(match)) > 4:
                continue
            if similarity >= threshold:
                return False, "Извините, но в вашем сообщении обнаружена ненормативная лексика."
        return True, ""

    async def handle(self, seq: str) -> str:
        seq = seq.lower().translate(str.maketrans('', '', string.punctuation))
        words = seq.split()

        is_correct, msg_over_brands = self.check_over_brands(words=words)
        if not is_correct:
            return msg_over_brands

        is_correct, msg_swear_words = self.check_profanity(words=words)
        if not is_correct:
            return msg_swear_words
        model_response = await self.requester.get_msg(msg=seq)
        return model_response


