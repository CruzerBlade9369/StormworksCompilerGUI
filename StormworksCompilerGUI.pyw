import subprocess
import os
import customtkinter as ctk
from tkinter import *
from tkinter import font as f
from tkinter import filedialog as fd
from tkinter import messagebox as msb

xpad = [60, 0]
apptitle = "Stormworks Compiler GUI"

class Layer1(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.input_file = ""
        self.output_folder = ""

        def AttbSwitch():
            if compilermode.get() == 1:
                self.meshprop0.configure(state="disabled")
                self.meshprop1.configure(state="disabled")
                self.meshprop2.configure(state="disabled")

                self.texprop0.configure(state="normal")
                self.texprop1.configure(state="normal")
            else:
                self.meshprop0.configure(state="normal")
                self.meshprop1.configure(state="normal")
                self.meshprop2.configure(state="normal")

                self.texprop0.configure(state="disabled")
                self.texprop1.configure(state="disabled")

            print("switch toggled, current value:", compilermode.get())

        def SelectFile():
            filetypes = [("DAE Files", "*.dae")] if compilermode.get() == 0 else [("Image Files", "*.png *.bmp")]
            file = fd.askopenfilename(filetypes = filetypes)

            if file:
                self.input_file = file
                self.fileres.configure(text=file)
        
        def SelectFolder():
            folder = fd.askdirectory()

            if folder:
                self.output_folder = folder
                self.outres.configure(text=folder)
        
        def BuildCommand():
            if not self.input_file or not self.output_folder:
                msb.showerror(apptitle, "Please select both input file and output folder.")
                return None

            if compilermode.get() == 0:
                command = f'./mesh_compiler "{self.input_file}" -o "{self.output_folder}"'
                if meshprop.get() == 1:
                    command += " -m physics_mesh"
                elif meshprop.get() == 2:
                    command += " -m physics"
            else:
                command = f'./texture_compiler "{self.input_file}" -o "{self.output_folder}"'
                if texprop.get() == 1:
                    command += " -c"
            
            return command

        def FileCompile():
            command = BuildCommand()

            if command:
                try:
                    result = subprocess.run(["powershell", "-Command", command], capture_output=True, text=True)
                    if result.returncode == 0:
                        msb.showinfo(apptitle, "Successfully compiled!")
                    else:
                        err = result.stderr if result.stderr else result.stdout

                        if "Compile error" in err:
                            err = err.split("Compile error:")[1].strip()
                            msb.showerror(apptitle, err)
                        else:
                            msb.showerror(apptitle, f"Compilation failed!")
                except Exception as e:
                    msb.showerror(apptitle, "Error compiling asset. " + {str(e)})

        compilermode = ctk.IntVar(value=0)
        meshprop = ctk.IntVar(value=0)
        texprop = ctk.IntVar(value=0)

        # config grid
        self.grid_columnconfigure(0, weight=1)

        # screen items
        self.compileselectlabel = ctk.CTkLabel(self, text="Select compiler")
        self.radiomeshselect = ctk.CTkRadioButton(self, text="Mesh", 
                                             command=AttbSwitch, variable=compilermode, value=0)
        self.radiotextureselect = ctk.CTkRadioButton(self, text="Texture", 
                                             command=AttbSwitch, variable=compilermode, value=1)
        self.openfile = ctk.CTkButton(self, text="Select file to compile", command=SelectFile)
        self.fileres = ctk.CTkLabel(self, text="")
        self.openout = ctk.CTkButton(self, text="Select folder to compile to", command=SelectFolder)
        self.outres = ctk.CTkLabel(self, text="")
        self.meshprop0 = ctk.CTkRadioButton(self, text="Compile to .mesh",
                                            variable=meshprop, value=0, state="normal")
        self.meshprop1 = ctk.CTkRadioButton(self, text="Compile to .phys mesh",
                                            variable=meshprop, value=1, state="normal")
        self.meshprop2 = ctk.CTkRadioButton(self, text="Compile to dynamic .phys",
                                            variable=meshprop, value=2, state="normal")
        self.texprop0 = ctk.CTkRadioButton(self, text="No compression",
                                            variable=texprop, value=0, state="disabled")
        self.texprop1 = ctk.CTkRadioButton(self, text="Lossy compression",
                                            variable=texprop, value=1, state="disabled")
        self.compile = ctk.CTkButton(self, text="Compile now!", command=FileCompile)
        
        # apply screen items
        self.compileselectlabel.grid(row=0, column=0, sticky="w", padx=xpad, pady=[30,0])
        self.radiomeshselect.grid(row=1, column=0, sticky="w", padx=xpad, pady=1)
        self.radiotextureselect.grid(row=2, column=0, sticky="w", padx=xpad, pady=1)
        self.openfile.grid(row=3, column=0, sticky="w", padx=xpad, pady=[20,0])
        self.fileres.grid(row=4, column=0, sticky="w", padx=xpad, pady=1)
        self.openout.grid(row=5, column=0, sticky="w", padx=xpad, pady=[20,0])
        self.outres.grid(row=6, column=0, sticky="w", padx=xpad, pady=1)
        self.meshprop0.grid(row=7, column=0, sticky="w", padx=xpad, pady=[20,0])
        self.meshprop1.grid(row=8, column=0, sticky="w", padx=xpad, pady=1)
        self.meshprop2.grid(row=9, column=0, sticky="w", padx=xpad, pady=1)
        self.texprop0.grid(row=10, column=0, sticky="w", padx=xpad, pady=[20,0])
        self.texprop1.grid(row=11, column=0, sticky="w", padx=xpad, pady=1)
        self.compile.grid(row=12, column=0, sticky="w", padx=xpad, pady=20)

        self.CheckForCompilers()

    def CheckForCompilers(self):
        mesh_compiler_exists = os.path.exists("./mesh_compiler.com")
        texture_compiler_exists = os.path.exists("./texture_compiler.com")

        if not mesh_compiler_exists or not texture_compiler_exists:
            missing_compilers = []
            if not mesh_compiler_exists:
                missing_compilers.append("mesh_compiler.com")
            if not texture_compiler_exists:
                missing_compilers.append("texture_compiler.com")

            # Disable the compile button and show error message
            self.compile.configure(state="disabled")
            msb.showerror(apptitle, f"Stormworks compiler(s) not found! Please make sure this program is placed in the same folder as these files. (Steam/steamapps/common/Stormworks/sdk)")

class Main(ctk.CTk):
    def __init__(self):
        super().__init__()

        # get system screen w and h
        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()

        # calculate window size
        w = ws/1.8
        h = hs/1.4
        self.resizable(width=False, height=False)

        # calculate window spawn position
        x = (ws/2) - (w/2)
        y = ((hs/2) - (h/2))

        # config grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=2)

        # set screen params
        ctk.set_appearance_mode("dark")
        self.title(apptitle)
        self.geometry('%dx%d+%d+%d' % (w, h, x, y))

        # declare screen items
        self.title = ctk.CTkLabel(self, text= "Stormworks Modding Assets Compiler GUI", 
                                                justify=LEFT, 
                                                font=(f.nametofont('TkTextFont'), 25))
        self.layer1 = Layer1(self)

        # apply screen items
        self.title.grid(row=0, column=0, sticky="nsew", padx=30, pady=[30, 30])
        self.layer1.grid(row=1, column=0, sticky="nsew", padx=30, pady=[0, 40])

# define app and main loop
app = Main()
app.mainloop()