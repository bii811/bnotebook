from module.notebookmongodb import LibraryMongoDB


class BNotebookApp:
    def __init__(self):
        self.app_title = "BNotebook"

        self.library = LibraryMongoDB()

        # Selected
        self.notebook_selected = None
        self.page_selected = None
        self.line_selected = None

    def __str__(self):
        return "{}".format(self.app_title)

    def select_notebook(self, index):
        if self.library.notebooks:
            self.notebook_selected = self.library.notebooks[index]
            self.line_selected = None
            self.page_selected = None

            print("[+] Notebook <{}> selected.".format(self.notebook_selected))

        else:
            print("[-] This Library hasn't any notebook to select.")

    def select_page(self, index):
        if self.notebook_selected:
            if self.notebook_selected.pages:
                self.page_selected = self.notebook_selected.pages[index]
                self.line_selected = None
                print("[+] Page <{}> selected.".format(self.page_selected))

            else:
                print("[-] This notebook hasn't any page to select.")
        else:
            print("[-] You aren't select any notebook yet.")

    def select_line(self, index):
        if self.notebook_selected:
            if self.page_selected:
                if self.page_selected.lines:
                    self.line_selected = self.page_selected.lines[index]
                    print("[+] Line <{}> selected.".format(self.line_selected))

                else:
                    print("[-] This page hasn't any line to select.")

            else:
                print("[-] You aren't select any page yet.")
        else:
            print("[-] You aren't select any notebook yet.")
