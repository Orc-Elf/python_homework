class SensitiveWordFilter:
    def __init__(self, file_path):
        self.file_path = file_path
        self.sensitive_words = self.load_words()

    def load_words(self):
        with open(self.file_path, 'r') as file:
            return [word.strip().lower() for word in file.readlines()]

    def filter_words(self, text):
        for word in self.sensitive_words:
            if word in text.lower():
                text = text.replace(word, '*' * len(word))
        return text