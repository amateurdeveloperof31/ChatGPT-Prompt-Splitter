# --------------------------------------------------- Imports ----------------------------------------------------------
from tkinter import Tk, Text, StringVar
from tkinter import ttk, messagebox
import pyperclip
import math
# ---------------------------------------------- Utility Functions -----------------------------------------------------
def split_prompt(prompt: str, limit: int = 4000):
    words = prompt.split()
    if not words:
        return {}

    total_parts = math.ceil(len(words) / limit)
    prompt_dict = {}

    for i in range(total_parts):
        chunk = ' '.join(words[i * limit: (i + 1) * limit])
        if i + 1 == total_parts:
            chunk += f"End of Part {i + 1} of {total_parts}. You now have the full input."
        else:
            f"Part {i + 1} of {total_parts}. Please acknowledge and wait for the next part. Do not summarize or respond yet."
        prompt_dict[f"Part {i + 1}"] = chunk

    return prompt_dict
# -------------------------------------------------- Main Class --------------------------------------------------------
class CgptPromptSplitter:
    def __init__(self):

        # Window
        self.root = Tk()
        self.root.title("ChatGPT Prompt Splitter")
        self.root.geometry("600x600")
        self.root.resizable(False, False)

        self.prompt_dict = {}
        self.default_splitter_limit = 4000

        self.style_settings()
        self.program_ui()
# ------------------------------------------------ Style Settings ------------------------------------------------------
    def style_settings(self):
        # Style
        style = ttk.Style()
        style.theme_use('clam')

        # Frame
        style.configure('shinyblack.TFrame', background='#212121', highlightbackground='#FF3737',
                        highlightthickness=2)
        # style.map('shinyblack.TFrame', background=[('selected', '#212121')])

        # Button Style
        style.configure('shinyBlack.TButton', foreground='#FFF', background='#212121', bordercolor='#444444',
                        focusthickness=3, focuscolor='none', font=('arial', 10, 'normal'), relief='raised')
        # style.map('shinyBlack.TButton', background=[('active', '#333333'), ('pressed', '#444444')])

        # Options Menu Style
        style.configure('TMenubutton', font=('Arial', 10, 'bold'), foreground='#fff', background='#008000')
        # style.map('TMenubutton', foreground=[('active', '#444444')], background=[('active', '#fff')])
# -------------------------------------------------- Program UI --------------------------------------------------------
    def program_ui(self):

        self.head_frame = ttk.Frame(master=self.root, borderwidth=2, relief='ridge', padding='10 10 10 10',
                                    style='shinyblack.TFrame')
        self.head_frame.place(relx=0.5, rely=0, anchor='n', relwidth=1, relheight=0.1)

        self.heading_label = ttk.Label(self.head_frame, text="ChatGPT Prompt Splitter", font=('arial', 20, 'bold'),
                                       foreground='white', background='#212121')
        self.heading_label.place(relx=0.5, rely=0.5, anchor='center')

        self.body_frame = ttk.Frame(master=self.root, borderwidth=2, relief='ridge', padding='10 10 10 10',
                                    style='shinyblack.TFrame')
        self.body_frame.place(relx=0.5, rely=0.1, anchor='n', relwidth=1, relheight=0.6)

        self.prompt_text = Text(self.body_frame, font=('arial', 20, 'bold'))
        self.prompt_text.place(relx=0.5, rely=0.5, anchor='center', relwidth=1, relheight=1)

        self.tail_frame = ttk.Frame(master=self.root, borderwidth=2, relief='ridge', padding='10 10 10 10',
                                    style='shinyblack.TFrame')
        self.tail_frame.place(relx=0.5, rely=1, anchor='s', relwidth=1, relheight=0.3)

        self.split_parts_label = ttk.Label(self.tail_frame, text=f'Enter Parts (default:{self.default_splitter_limit}): ',
                                           font=('arial', 10, 'normal'), foreground='#FFF', background='#212121')
        self.split_parts_label.place(relx=0, rely=0.2, anchor='w')

        self.split_parts_entry = ttk.Entry(self.tail_frame, font=('arial', 10, 'normal'))
        self.split_parts_entry.place(relx=0.4, rely=0.2, anchor='center')

        self.split_parts_button = ttk.Button(self.tail_frame, text="Generate", style='shinyBlack.TButton',
                                             command=self.split_parts)
        self.split_parts_button.place(relx=0.65, rely=0.2, anchor='center')
# -------------------------------------------------- Split Parts -------------------------------------------------------
    def split_parts(self):
        prompt = self.prompt_text.get('1.0', 'end-1c').strip()

        if not prompt.strip():
            messagebox.showwarning("Empty Prompt", "Please enter a prompt to split.")
            return

        try:
            splitter_limit = int(self.split_parts_entry.get())
        except ValueError:
            splitter_limit = self.default_splitter_limit

        self.prompt_dict = split_prompt(prompt, splitter_limit)

        if not self.prompt_dict:
            messagebox.showinfo("Split Result", "Prompt was too short to split.")
            return

        selected_option = StringVar()

        self.prompt_part_options = ttk.OptionMenu(self.tail_frame, selected_option, list(self.prompt_dict.keys())[0],
                                                  *self.prompt_dict.keys())
        self.prompt_part_options.place(relx=0.2, rely=0.9, anchor='w')

        self.prompt_part_button = ttk.Button(self.tail_frame, text="Copy", style='shinyBlack.TButton',
                                             command=lambda: self.copy_to_clipboard(selected_option))
        self.prompt_part_button.place(relx=0.4, rely=0.9, anchor='w')
# ----------------------------------------------- Copy to Clipboard ---------------------------------------------------
    def copy_to_clipboard(self, selected_option):
        selected_key = selected_option.get()
        pyperclip.copy(self.prompt_dict[selected_key])
        messagebox.showinfo("Copied", f"{selected_key} copied to clipboard!")
# ------------------------------------------------------ Run -----------------------------------------------------------
    def run(self):
        self.root.mainloop()
# ----------------------------------------------------- Debug ----------------------------------------------------------
if __name__ == '__main__':
    app = CgptPromptSplitter()
    app.run()