from tkinter import *
from module import mythread
from module.bnotebookapp import BNotebookApp
import time

my_app = BNotebookApp()


class MainForm:
    def __init__(self):
        self.root = Tk()
        self.root.wm_title("BNotebook")

        # Column 0
        self.frame1_col0 = Frame(self.root)
        self.frame1_col0.grid(row=0, column=0, sticky=(N,))
        Label(self.frame1_col0, text="Notebook List:").grid(row=0)
        self.listbox_notebook = Listbox(self.frame1_col0)
        self.listbox_notebook.grid(row=1)
        self.listbox_notebook.bind('<<ListboxSelect>>', self.listbox_notebook_select_event)

        self.entry_add_new_notebook = Entry(self.frame1_col0)
        self.entry_add_new_notebook.grid(row=2, column=0)
        self.add_notebook_btn = Button(self.frame1_col0, text='Add notebook', command=self.add_notebook_btn_clicked)
        self.add_notebook_btn.grid(row=3, column=0)
        self.edit_notebook_btn = Button(self.frame1_col0, text='Edit notebook', command=self.edit_notebook_btn_clicked)
        self.edit_notebook_btn.grid(row=4, column=0)

        # Column 1
        self.frame1_col1 = Frame(self.root)
        self.frame1_col1.grid(row=0, column=1, sticky=(N,))
        Label(self.frame1_col1, text="Note List:").grid(row=0)
        self.listbox_page = Listbox(self.frame1_col1)
        self.listbox_page.grid(row=1)
        self.listbox_page.bind('<<ListboxSelect>>', self.listbox_page_select_event)

        self.entry_add_new_page = Entry(self.frame1_col1)
        self.entry_add_new_page.grid(row=2, column=0)
        self.add_page_btn = Button(self.frame1_col1, text='Add page', command=self.add_page_btn_clicked)
        self.add_page_btn.grid(row=3, column=0)
        self.edit_page_btn = Button(self.frame1_col1, text='Edit page', command=self.edit_page_btn_clicked)
        self.edit_page_btn.grid(row=4, column=0)

        # Column 2
        self.frame1_col2 = Frame(self.root)
        self.frame1_col2.grid(row=0, column=2, sticky=(W, N))

        self.label_notebook = Label(self.frame1_col2, text="Notebook:")
        self.label_notebook.grid(row=0, column=0, columnspan=3, sticky=(W,))
        self.label_page = Label(self.frame1_col2, text="Note:")
        self.label_page.grid(row=1, column=0, columnspan=3, sticky=(W,))

        # ==== Frame2 label: textbox button
        self.frame2_col2 = Frame(self.frame1_col2)
        self.frame2_col2.grid(row=2, column=0, sticky=(W,))
        Label(self.frame2_col2, text="New Line:").grid(row=0, column=0)
        self.entry_line = Entry(self.frame2_col2, width=100)
        self.entry_line.grid(row=0, column=1)
        self.entry_line.bind('<Return>', self.entry_line_enter_pressed)
        self.write_btn = Button(self.frame2_col2, text='Write', command=self.write_btn_clicked)
        self.write_btn.grid(row=0, column=2)
        self.CheckVarRefresh = IntVar()
        self.refresh_real_time_checkbox = Checkbutton(self.frame2_col2, text="Refresh",
                                                      variable=self.CheckVarRefresh,
                                                      onvalue=1, offvalue=0)
        self.refresh_real_time_checkbox.grid(row=0, column=3)

        self.labelframe = LabelFrame(self.frame1_col2, text="Content")
        self.labelframe.grid(row=3, column=0, columnspan=3, sticky=(N, S, E, W))
        # Label(labelframe, text='').grid(row=0, column=0, sticky=(N, W))

        # create a Text widget
        self.text_lines = Text(self.labelframe, borderwidth=2, relief="sunken")
        self.text_lines.config(font=("consolas", 12), undo=True, wrap='word')
        self.text_lines.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)

        # create a Scrollbar and associate it with txt
        self.scrollbar = Scrollbar(self.labelframe, command=self.text_lines.yview)
        self.scrollbar.grid(row=0, column=1, sticky='nsew')
        self.text_lines['yscrollcommand'] = self.scrollbar.set

        # Search box
        self.frame2_col0 = Frame(self.root, borderwidth=2, relief='sunken')
        self.frame2_col0.grid(row=0, column=3, columnspan=2, sticky=(N, S, W, E))
        Label(self.frame2_col0, text='Search:').grid(row=0, column=0)
        self.entry_search = Entry(self.frame2_col0)
        self.entry_search.grid(row=0, column=1)
        self.entry_search.bind('<Return>', self.entry_search_pressed_enter)
        self.label_search_result = Label(self.frame2_col0, text='Result:', justify=LEFT)
        self.label_search_result.grid(row=1, column=0, columnspan=2)

        self.root.protocol('WM_DELETE_WINDOW', self.window_closed)

        # Threading

        self.refresh_text_line_thread = mythread.MyThread("RefreshTextLineThread", self.thread_loop_refresh_text_line)

        if not self.refresh_text_line_thread.isAlive():
            self.refresh_text_line_thread.start()

        # refresh notebook listbox
        self.listbox_notebook_refresh()

        # Tkinter loop
        self.root.mainloop()

    def window_closed(self):
        """ (Event) when window is closed """
        self.refresh_text_line_thread.exitThreadFlag = 1
        time.sleep(0.7)
        self.root.destroy()

    def thread_loop_refresh_text_line(self):
        """ (Function) loop text_lines_refresh() when checkbox refresh is ticked """
        value = self.CheckVarRefresh
        if value.get() == 1:
            self.text_lines_refresh()

    def listbox_notebook_refresh(self):
        """ (Function) Reload all notebooks, clear listbox_notebook, and reinsert"""
        self.listbox_notebook.delete(0, END)

        my_app.library.load_all_notebooks()

        index = 0
        if my_app.library.notebooks:
            for notebook in my_app.library.notebooks:
                self.listbox_notebook.insert(index, str(notebook))
                index += 1

    def listbox_notebook_select_event(self, event):
        """ (Event) listbox_notebook is selected """
        print("[GUI]: listbox_notebook_select_event")
        if self.listbox_notebook.curselection():
            index = self.listbox_notebook.curselection()[0]
            my_app.select_notebook(index)
            self.label_notebook.config(text="Notebook: {}".format(my_app.notebook_selected.title))
            self.label_page.config(text="Note: {}".format(''))
            self.listbox_page_refresh()

            self.text_lines_refresh()

    def add_notebook_btn_clicked(self, event=None):
        """ (Event) add_page_btn is clicked """
        if self.entry_add_new_notebook != '':
            my_app.library.add_new_notebook(self.entry_add_new_notebook.get())

            self.entry_add_new_notebook.delete(0, END)
            self.listbox_notebook_refresh()

    def edit_notebook_btn_clicked(self, event=None):
        """ (Event) edit_notebook_btn is clicked """
        if my_app.notebook_selected:
            ew = EditNotebookWindow(self.root, w_title="Edit Notebook", title=my_app.notebook_selected.title,
                                    func=self.listbox_notebook_refresh)

    def listbox_page_refresh(self):
        """ (Function) Refresh listbox_pages """
        self.listbox_page.delete(0, END)

        my_app.notebook_selected.load_all_pages()

        index = 0
        for page in my_app.notebook_selected.pages:
            self.listbox_page.insert(index, str(page))
            index += 1

    def listbox_page_select_event(self, event):
        """ (Event) listbox_page is selected """
        print("[GUI]: listbox_page_select_event")
        if self.listbox_page.curselection():
            index = self.listbox_page.curselection()[0]
            my_app.select_page(index)
            self.label_page.config(text="Note: {}".format(my_app.page_selected.name))
            self.text_lines_refresh()

    def add_page_btn_clicked(self, event=None):
        """ (Event) add_page_btn is clicked """
        if my_app.notebook_selected and self.entry_add_new_page.get() != '':
            my_app.notebook_selected.add_new_page(self.entry_add_new_page.get())

            self.entry_add_new_page.delete(0, END)
            self.listbox_page_refresh()

    def edit_page_btn_clicked(self, event=None):
        """ (Event) edit_page_btn is clicked """
        if my_app.page_selected:
            ew = EditPageWindow(self.root, w_title="Edit Page", name=my_app.page_selected.name,
                                func=self.listbox_page_refresh)

    def write_btn_clicked(self, event=None):
        """ (Event) Add new line when write button click """
        if my_app.page_selected:
            my_app.page_selected.add_new_line(self.entry_line.get())
            self.text_lines_refresh()

        else:
            print('select page first')

        self.entry_line.delete(0, END)

    def entry_line_enter_pressed(self, event):
        """ (Event) Add new line when press enter """
        if my_app.page_selected:
            my_app.page_selected.add_new_line(self.entry_line.get())
            self.text_lines_refresh()

        else:
            print('select page first')

        self.entry_line.delete(0, END)

    def text_lines_refresh(self):
        """ Refresh text_lines """
        self.text_lines.delete('1.0', END)

        if my_app.page_selected:
            my_app.page_selected.load_all_lines()

            index = 0
            for line in my_app.page_selected.lines[::-1]:
                self.text_lines.insert(END, "{}\n".format(str(line)))
                index += 1

    def entry_search_pressed_enter(self, event):
        """ (Event) when search button click """
        self.label_search_result.config(text="Result: {}".format(my_app.library.search_lines(self.entry_search.get())))


class EditNotebookWindow:
    """
    This class is create new edit notebook window
    """
    def __init__(self, main_root, w_title=None, title=None, func=None):
        self.func = func
        self.window = Toplevel(main_root)
        self.window.wm_title(w_title)
        self.entry_title = Entry(self.window)
        self.entry_title.insert(0, title)
        self.entry_title.pack()
        self.edit_btn = Button(self.window, text='Edit', command=self.edit)
        self.edit_btn.pack()
        self.delete_btn = Button(self.window, text="Delete", command=self.delete)
        self.delete_btn.pack()

    def edit(self, event=None):
        my_app.notebook_selected.edit(self.entry_title.get())
        self.func()
        self.window.destroy()

    def delete(self, event=None):
        my_app.notebook_selected.delete()
        self.func()
        self.window.destroy()


class EditPageWindow(EditNotebookWindow):
    """
        This class is create new edit notebook window
    """
    def __init__(self, main_root, w_title=None, name=None, func=None):
        super().__init__(main_root, w_title, name, func)

    def edit(self, event=None):
        my_app.page_selected.edit(self.entry_title.get())
        self.func()
        self.window.destroy()

    def delete(self, event=None):
        my_app.page_selected.delete()
        self.func()
        self.window.destroy()
