class Return(Exception):
    def __init__(self, value: object):
        super().__init__(value)
        self.value = value
