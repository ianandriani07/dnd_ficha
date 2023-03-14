class LinkedText:

    def __init__(self, header: str):
        self.header: str = header
        self.description: str = ''
        self.subcategories: dict[str, str] = {}

    def prettify_subcategories(self, amount_of_spaces: int) -> str:
        text = ''
        for key in self.subcategories.keys():
            text += ' '*amount_of_spaces + '<->' + key + '\n' + ' ' * \
                amount_of_spaces + '    ' + self.subcategories[key]
        return text

    def __repr__(self) -> str:
        return f"""{self.header}

{self.description}

{self.prettify_subcategories(5)}"""
