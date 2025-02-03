class TextManager:
    def __init__(self, font):
        self.font = font
        self.text_groups = {}

    def create_text(self, text_id, text, x, y):
        text_group = self.font.write_text(text, x, y)
        self.text_groups[text_id] = {
            'group': text_group,
            'x': x,
            'y': y,
            'text': text
        }
        return text_group

    def update_text(self, text_id, new_text):
        if text_id in self.text_groups:
            info = self.text_groups[text_id]
            new_group = self.font.write_text(new_text, info['x'], info['y'])
            self.text_groups[text_id]['text'] = new_text
            self.text_groups[text_id]['group'] = new_group
            return new_group
        return None

    def get_current_group(self, text_id):
        if text_id in self.text_groups:
            return self.text_groups[text_id]['group']
        return None