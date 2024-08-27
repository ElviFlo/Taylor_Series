from tkinter import *
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import ttk

class Taylor:
    def __init__(self, f, a, n):
        self.f = f
        self.a = a
        self.n = n

    def taylor(self):
        x = sp.symbols('x')
        modelo = 0
        for i in range(self.n + 1):
            modelo += (self.f.diff(x, i).subs(x, self.a) * (x - self.a) ** i) / sp.factorial(i)
        return modelo

    def errores(self, equis):
        x = sp.symbols('x')
        valor_teorico = self.f.subs(x, equis).evalf()
        valor_experimental = self.taylor().subs(x, equis).evalf()
        error_absoluto = abs(valor_teorico - valor_experimental)
        error_relativo = abs((valor_teorico - valor_experimental) / valor_teorico) * 100
        return valor_teorico, valor_experimental, error_absoluto, error_relativo

        


root = Tk()
root.title("Series de Taylor")
root.geometry("1100x650")
root.resizable(False, False)
root.configure(bg='#EAF6F6')

app_ic = "icons/app_icon.png"  
aic = PhotoImage(file=app_ic)
root.iconphoto(False, aic)

home_ic = "icons/house.png"
hic = PhotoImage(file=home_ic)

lg_ic = "icons/logo.png"
gic = PhotoImage(file=lg_ic)


left_frame = Frame(root, bg='#20A2A0', width=1190, height=690)
left_frame.place(x=0, y=0)

canvas = Canvas(root, width=175, height=140, bg='#20A2A0')
canvas.place(x=-10,y=-20)

canvas.create_image(0, 0, anchor=NW, image=gic)

menu_icons = ['icons/house.png', 'icons/historial.png', 'icons/manual.png', 'icons/exit.png']
menu_items = ['   Home            ', '   Historial            ', '   Manual            ','   LogOut            ']

icon_images = []

for index, item in enumerate(menu_items):
    icon = PhotoImage(file=menu_icons[index])
    icon_images.append(icon) 
    
    Button(left_frame, text=item, fg='white', bg='#20A2A0', bd=0, anchor='w', font=('Cooper Black', 13), image=icon, compound=LEFT).place(x=20, y=165+index*50)

main_frame = Frame(root, bg='white', width=1000, height=670)
main_frame.place(x=165, y=0)


Label(main_frame, text="Taylor Series", font=('Cooper Black', 34, 'bold'), bg='white', fg='#064F5C').place(x=30, y=15)


Label(main_frame, text="- Digite a:", font=('Cooper Black', 14), bg='white', fg='black').place(x=35, y=80)
a_entry = Entry(main_frame, width=4,font=("Arial", 16), fg='black', bg='#BAEAF6',bd=2)
a_entry.place(x=145, y=82)

Label(main_frame, text="- Digite n:", font=('Cooper Black', 14), bg='white', fg='black').place(x=230, y=80)
n_entry = Entry(main_frame, width=4,font=("Arial", 16), fg='black', bg='#BAEAF6',bd=2)
n_entry.place(x=340, y=82)

Label(main_frame, text="- Digite x:", font=('Cooper Black', 14), bg='white', fg='black').place(x=425, y=80)
x_entry = Entry(main_frame, width=4,font=("Arial", 16), fg='black', bg='#BAEAF6',bd=2)
x_entry.place(x=535, y=82)

Label(main_frame, text="- Digite f(x):", font=('Cooper Black', 14), bg='white', fg='black').place(x=620, y=80)
fx_entry = Entry(main_frame, width=10,font=("Arial", 16), fg='black', bg='#BAEAF6',bd=2)
fx_entry.place(x=755, y=82)

canvas_frame = Frame(main_frame, bg='white', width=900, height=500)
canvas_frame.place(x=50, y=150)

Button(main_frame, text="1 March - 14 March", font=('Arial', 10), bg='#EAF6F6', bd=1).place(x=400, y=15)

def calcular_taylor():
    try:
        a = float(a_entry.get())
        n = int(n_entry.get())
        x = float(x_entry.get())
        f = sp.sympify(fx_entry.get())

        
        for widget in canvas_frame.winfo_children():
            widget.destroy()

        taylor = Taylor(f, a, n)
        
        # Gráfica
        x = sp.symbols('x')
        valores_x = np.linspace(-5,5,100)
        valores_fx = [f.subs(x, i) for i in valores_x]

        # Crear la figura y el eje
        fig, ax = plt.subplots()
        
        valores_x = np.linspace(-5,5,100)
        valores_fx = [taylor.f.subs(x,i) for i in valores_x]
        ax.plot(valores_x, valores_fx)
        valores_y = [taylor.taylor().subs(x,i) for i in valores_x]
        ax.plot(valores_x, valores_y)
        ax.legend(['f(x)','Taylor'])
        ax.grid()
        ax.title('Taylor')
        ax.xlabel('x')
        ax.ylabel('f(x)')
        
        ax.plot(valores_x, valores_fx)
        
        valores_y = [taylor.taylor().subs(x,i) for i in valores_x]
        ax.plot(valores_x, valores_y)

        ax.legend()
        ax.grid()
        ax.set_title('Serie de Taylor')
        ax.set_xlabel('x')
        ax.set_ylabel('f(x)')

        # Mostrar la gráfica en el frame de Tkinter
        canvas = FigureCanvasTkAgg(fig, master=canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=BOTH, expand=True)
        
        
        taylor.grafica([0, n], canvas_frame)
        vt, ve, ea, er = taylor.errores(x)
        
        resultados = f"Valor teórico: {vt}\nValor experimental: {ve}\nError absoluto: {ea}\nError relativo: {er}"
        messagebox.showinfo("Resultados", resultados)
    except Exception as e:
        messagebox.showerror("Error", f"Error en la entrada de datos: {e}")

# Botón para calcular la serie de Taylor
calc_button = Button(main_frame, text="Calcular", font=('Cooper Black', 14), bg='#20A2A0', fg='white', command=calcular_taylor)
calc_button.place(x=900, y=75)


root.mainloop()

