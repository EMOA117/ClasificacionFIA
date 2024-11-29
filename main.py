import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd


class DatasetAnalyzerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Loading Data ML P1")

        # Variables
        self.separator = tk.StringVar(value=",")
        self.file_path = None
        self.dataframe = None

        # Frame para cargar archivo
        self.file_frame = tk.Frame(self.root)
        self.file_frame.pack(pady=10)

        self.file_label = tk.Label(self.file_frame, text="Archivo:")
        self.file_label.grid(row=0, column=0, padx=5, pady=5)

        self.file_entry = tk.Entry(self.file_frame, width=40, state="readonly")
        self.file_entry.grid(row=0, column=1, padx=5, pady=5)

        self.browse_button = tk.Button(
            self.file_frame, text="Cargar Archivo", command=self.load_file
        )
        self.browse_button.grid(row=0, column=2, padx=5, pady=5)

        # Frame para seleccionar separador
        self.separator_frame = tk.Frame(self.root)
        self.separator_frame.pack(pady=10)

        self.separator_label = tk.Label(self.separator_frame, text="Separador:")
        self.separator_label.grid(row=0, column=0, padx=5, pady=5)

        self.separator_entry = tk.Entry(self.separator_frame, textvariable=self.separator, width=10)
        self.separator_entry.grid(row=0, column=1, padx=5, pady=5)

        self.load_button = tk.Button(
            self.separator_frame, text="Cargar Dataset", command=self.process_file
        )
        self.load_button.grid(row=0, column=2, padx=5, pady=5)

        # Frame para mostrar información
        self.info_frame = tk.Frame(self.root)
        self.info_frame.pack(pady=10, fill=tk.BOTH, expand=True)

        self.info_label = tk.Label(self.info_frame, text="Información del dataset:")
        self.info_label.pack(pady=5)

        self.info_text = tk.Text(self.info_frame, height=10, state="disabled")
        self.info_text.pack(fill=tk.BOTH, expand=True)

        # Frame para selección de atributos
        self.selection_frame = tk.Frame(self.root)
        self.selection_frame.pack(pady=10)

        self.attributes_label = tk.Label(self.selection_frame, text="Seleccionar atributos:")
        self.attributes_label.grid(row=0, column=0, padx=5, pady=5)

        self.attributes_listbox = tk.Listbox(self.selection_frame, selectmode="multiple", width=40)
        self.attributes_listbox.grid(row=0, column=1, padx=5, pady=5)

        self.generate_vector_button = tk.Button(
            self.selection_frame, text="Generar Vector", command=self.generate_vector
        )
        self.generate_vector_button.grid(row=0, column=2, padx=5, pady=5)

    def load_file(self):
        self.file_path = filedialog.askopenfilename(
            filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")]
        )
        if self.file_path:
            self.file_entry.config(state="normal")
            self.file_entry.delete(0, tk.END)
            self.file_entry.insert(0, self.file_path)
            self.file_entry.config(state="readonly")
        else:
            messagebox.showwarning("Error", "No se seleccionó ningún archivo.")

    def process_file(self):
        if not self.file_path:
            messagebox.showerror("Error", "Por favor, cargue un archivo primero.")
            return

        sep = self.separator.get()
        if not sep:
            messagebox.showerror("Error", "Por favor, ingrese un separador.")
            return

        try:
            self.dataframe = pd.read_csv(self.file_path, sep=sep)
            self.display_info()
            self.populate_attributes()
        except Exception as e:
            messagebox.showerror("Error", f"Error al procesar el archivo: {e}")

    def display_info(self):
        """Muestra información básica del dataset."""
        if self.dataframe is not None:
            info = []
            info.append(f"Número de atributos: {len(self.dataframe.columns)}")
            info.append(f"Número de patrones (filas): {len(self.dataframe)}\n")

            for col in self.dataframe.columns:
                if pd.api.types.is_numeric_dtype(self.dataframe[col]):
                    info.append(
                        f"Atributo '{col}' (Cuantitativo): Min={self.dataframe[col].min()}, "
                        f"Max={self.dataframe[col].max()}, Media={self.dataframe[col].mean():.2f}"
                    )
                else:
                    categories = self.dataframe[col].unique()
                    info.append(f"Atributo '{col}' (Cualitativo): Categorías={list(categories)}")

            # Mostrar en el widget de texto
            self.info_text.config(state="normal")
            self.info_text.delete("1.0", tk.END)
            self.info_text.insert(tk.END, "\n".join(info))
            self.info_text.config(state="disabled")

    def populate_attributes(self):
        """Llena el Listbox con los nombres de los atributos."""
        if self.dataframe is not None:
            self.attributes_listbox.delete(0, tk.END)
            for col in self.dataframe.columns:
                self.attributes_listbox.insert(tk.END, col)

    def generate_vector(self):
        """Genera un vector con los atributos seleccionados."""
        selected_indices = self.attributes_listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("Advertencia", "Seleccione al menos un atributo.")
            return

        selected_columns = [self.attributes_listbox.get(i) for i in selected_indices]
        vector = self.dataframe[selected_columns].values.tolist()

        # Muestra el vector generado en un mensaje
        messagebox.showinfo("Vector Generado", f"Vector generado con atributos seleccionados:\n{vector}")


if __name__ == "__main__":
    root = tk.Tk()
    app = DatasetAnalyzerApp(root)
    root.geometry("800x600")
    root.mainloop()
