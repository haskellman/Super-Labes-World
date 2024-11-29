def check_answer(self):
    if self.option == self.answer:
        self.test.append(1)
        self.error_mode = False
        self.sounds['correct_answer'].play()
        self.counter_text_speak = 0
        self.done_text_speak = False
        self.current_text = choice(CORRECTS_SPEAKS)

    else:
        self.test.append(0)
        self.error_mode = True
        self.sounds['wrong_answer'].play()
        self.counter_text_speak = 0
        self.done_text_speak = False
        self.current_text = choice(WRONGS_SPEAKS)