class BaseLibrary:
    def __init__(self):
        self.notebooks = []


class BaseNotebook:
    def __init__(self, title=None):
        self.title = title
        self.pages = []

    def __str__(self):
        return "{}".format(self.title)


class BasePage:
    def __init__(self, notebook_object, name=None):
        self.notebook_object = notebook_object
        self.name = name
        self.lines = []

    def __str__(self):
        return "{}".format(self.name)


class BaseLine:
    def __init__(self, page_object, content=None):
        self.page_object = page_object
        self.content = content

    def __str__(self):
        return "{}".format(self.content)

