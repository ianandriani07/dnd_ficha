class Text:

    def __init__(self, main_text: str):
        self.main_text: str = main_text
        self.sub_text: list[str] = []

    def prettify_subtext(self, amount_of_spaces: int) -> str:
        text = ''
        for t in self.sub_text:
            text += ' '*amount_of_spaces + '-> ' + t
        return text

    def __repr__(self) -> str:
        if self.sub_text:
            return f"{self.main_text}\n{self.prettify_subtext(10)}"
        return f"{self.main_text}"


class LinkedText:

    def __init__(self, header: str):
        self.header: str = header
        self.description: str = ''
        self.subcategories: dict[str, Text] = {}

    def prettify_subcategories(self, amount_of_spaces: int) -> str:
        text = ''
        for key in self.subcategories.keys():
            text += ' '*amount_of_spaces + '<->' + key + '\n' + ' ' * \
                amount_of_spaces + '    ' + str(self.subcategories[key]) + '\n'
        return text

    def __repr__(self) -> str:
        return f"""{self.header}

{self.description}

{self.prettify_subcategories(5)}"""
