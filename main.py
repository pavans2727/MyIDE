from tkinter import *
from tkinter.filedialog import asksaveasfilename, askopenfilename
import subprocess

# creates the ui
compiler = Tk()
compiler.title("Brahma's IDE") # gives the title
file_path = ""
already_saved = False

# used to set the file path
def set_file_path(path):
    global file_path
    file_path = path

# run the code
def run():
    if file_path == "":
        # to alert whenn the save is not done
        save_prompt = Toplevel()
        text = Label(save_prompt, text="Please save your code to run")
        text.pack()
        return

    # command to run python file
    command = f'python {file_path}'
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

    # to print the results in code_output text area
    output, error = process.communicate()
    code_output.delete('1.0', END)
    code_output.insert('1.0', error)
    code_output.insert('1.0', output)

# open button
def open_file():
    # only python files have to be opened
    path = askopenfilename(filetypes=[("Python Files", '*.py')])

    with open(path, 'r') as file:
        # taken from file delete current contents of text area and put to text area
        code = file.read()  
        editor.delete('1.0', END)
        editor.insert('1.0', code)
        set_file_path(path)

# save and save as
def save_as():
    global file_path

    # if not saved initially
    if file_path == "":
        path = asksaveasfilename(filetypes=[("Python Files", '*.py')])
    
    # else if saved initially
    else:
        path = file_path

    with open(path, 'w') as file:
        code = editor.get('1.0', END)
        file.write(code) 
        set_file_path(path)

# menu bar -> ( run, file)
menu_bar = Menu(compiler)

# File related options
file_menu = Menu(menu_bar, tearoff=0)
file_menu.add_command(label='Open', command=open_file) # performs certain function
file_menu.add_command(label='Save', command=save_as) 
file_menu.add_command(label='Save As', command=save_as) 
menu_bar.add_cascade(label='File', menu=file_menu)  # run must be on top to menu

# Run related options
run_bar = Menu(menu_bar, tearoff=0)
run_bar.add_command(label='Run', command=run) 
menu_bar.add_cascade(label='Run', menu=run_bar)

exit_bar = Menu(menu_bar, tearoff=0)
exit_bar.add_command(label='Exit', command=exit) 
menu_bar.add_cascade(label='Exit', menu=exit_bar)

compiler.config(menu=menu_bar)

editor = Text()  # creates text area to write
editor.pack()

code_output = Text(height=10)  # used to display the output
code_output.pack()

compiler.mainloop()