from module.basenotebookclass import BaseLibrary, BaseNotebook, BasePage, BaseLine
from module.mymongodb.basedbclass import BaseMongoDB


class LibraryMongoDB(BaseLibrary, BaseMongoDB):
    def __init__(self):
        BaseLibrary.__init__(self)
        BaseMongoDB.__init__(self)

    def load_all_notebooks(self):
        filter_document = {}
        notebooks_found = self.database['notebook'].find(filter_document)

        self.notebooks = []
        if notebooks_found:
            for notebook in notebooks_found:
                try:
                    new_notebook = NotebookMongoDB(_id=notebook['_id'],
                                                   title=notebook['title'],
                                                   modified_date=notebook['modified_date'])
                    self.notebooks.append(new_notebook)

                except KeyError as e:
                    print("Key error:", e.args[0])

    def add_new_notebook(self, title):
        if not str(title) == '':
            new_notebook = NotebookMongoDB(title=title)
            new_notebook.save()

            self.load_all_notebooks()

        else:
            print("[-] Can't add new notebook with empty title.")

    def search_lines(self, search_text):
        search_document = {"$regex": search_text}
        lines_found = self.database['line'].find({"content": search_document})

        result = '\n'
        for l in lines_found:
            collection = self.database['page']
            pages = collection.find({'_id': l['page_id']})
            for p in pages:
                collection = self.database['notebook']
                notebooks = collection.find({'_id': p['notebook_id']})
                for n in notebooks:
                    result += str(n['title']) + ">"
                result += str(p['name']) + ">"
            result += l['content'] + "\n"

        print("[SearchResult]: {}".format(result.split('\n')))

        return result


class NotebookMongoDB(BaseNotebook, BaseMongoDB):
    def __init__(self, _id=None, title=None, modified_date=None):
        self.collection_name = 'notebook'

        BaseNotebook.__init__(self, title)
        BaseMongoDB.__init__(self, self.collection_name, _id, modified_date)

    def save(self):
        document = {'title': self.title}
        self.insert(document)

    def edit(self, new_title):
        self.title = new_title
        document = {'title': self.title}
        self.update(document)

    def load_all_pages(self):
        filter_document = {'notebook_id': self.id}
        pages_found = self.database['page'].find(filter_document)

        self.pages = []
        if pages_found:
            for page in pages_found:
                try:
                    new_page = PageMongoDB(self,
                                           _id=page['_id'],
                                           name=page['name'],
                                           modified_date=page['modified_date'])
                    self.pages.append(new_page)

                except KeyError as e:
                    print('[Error]: Key error ', e.args[0])

    def add_new_page(self, name):
        if not name == '':
            new_page = PageMongoDB(self, name=name)
            new_page.save()

            self.load_all_pages()

        else:
            print("[-] Can't add new page with empty name.")


class PageMongoDB(BasePage, BaseMongoDB):
    def __init__(self, notebook_object, _id=None, name=None, modified_date=None):
        self.collection_name = 'page'

        BasePage.__init__(self, notebook_object, name)
        BaseMongoDB.__init__(self, self.collection_name, _id, modified_date)

    def save(self):
        document = {'notebook_id': self.notebook_object.id, 'name': self.name}
        self.insert(document)

    def edit(self, new_name):
        self.name = new_name
        document = {'name': self.name}
        self.update(document)

    def load_all_lines(self):
        filter_document = {'page_id': self.id}
        lines_found = self.database["line"].find(filter_document)

        self.lines = []
        if lines_found:
            for line in lines_found:
                try:
                    new_line = LineMongoDB(self,
                                           _id=line['_id'],
                                           content=line['content'],
                                           modified_date=line['modified_date'])
                    self.lines.append(new_line)

                except KeyError as e:
                    print('Key error:', e.args[0])

    def add_new_line(self, content):
        new_line = LineMongoDB(self, content=content)
        new_line.save()

        self.load_all_lines()


class LineMongoDB(BaseLine, BaseMongoDB):
    def __init__(self, page_object, _id=None, content=None, modified_date=None):
        self.collection_name = 'line'

        BaseLine.__init__(self, page_object, content)
        BaseMongoDB.__init__(self, self.collection_name, _id, modified_date)

    def save(self):
        document = {'page_id': self.page_object.id, 'content': self.content}
        self.insert(document)

    def edit(self, new_content):
        self.content = new_content
        document = {'content': self.content}
        self.update(document)

    def __str__(self):
        return "[{}]: {}".format(self.created_date, self.content)
