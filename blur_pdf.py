import tkinter as tk
from tkinter import filedialog, messagebox
import fitz
from PIL import Image, ImageTk
import os

class PDFEditorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Blur_PDF v2.1")
        self.root.geometry("1000x700")
        self.root.configure(bg="#2c3e50")

        self.estilo_botao = {
            "bg": "#3498db",
            "fg": "white",
            "activebackground": "#2980b9",
            "font": ("Segoe UI", 10, "bold"),
            "bd": 0,
            "padx": 10,
            "pady": 5
        }


        self.frame_controles = tk.Frame(root, bg="#34495e")
        self.frame_controles.pack(side=tk.TOP, fill=tk.X, pady=10)

        self.btn_carregar = tk.Button(self.frame_controles, text="Carregar PDF de Referência", command=self.carregar_pdf, **self.estilo_botao)
        self.btn_carregar.pack(side=tk.LEFT, padx=10)

        self.btn_borrar_pasta = tk.Button(self.frame_controles, text="Borrar Arquivos da Pasta", command=self.selecionar_pasta_e_borrar, **self.estilo_botao)
        self.btn_borrar_pasta.pack(side=tk.LEFT, padx=10)

        self.btn_salvar = tk.Button(self.frame_controles, text="Salvar Somente PDF de Referência", command=self.salvar_pdf, **self.estilo_botao)
        self.btn_salvar.pack(side=tk.LEFT, padx=10)
        

        self.canvas_frame = tk.Frame(root)
        self.canvas_frame.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(self.canvas_frame, bg="white")
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scroll_y = tk.Scrollbar(self.canvas_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.configure(yscrollcommand=self.scroll_y.set)

        self.retangulos = []
        self.rect_start = None
        self.rect_id = None
        self.pdf_path = None
        self.page_image = None
        self.tk_img = None

        self.canvas.bind("<Button-1>", self.iniciar_desenho)
        self.canvas.bind("<B1-Motion>", self.desenhar)
        self.canvas.bind("<ButtonRelease-1>", self.finalizar_desenho)

        self.texto_tutorial_id = self.canvas.create_text(
            500, 350,  
            text=(
                "Bem-vindo ao Blur_PDF v2.1!\n\n"
                "1. Clique em 'Carregar PDF de Referência' para selecionar um arquivo.\n"
                "- Esse arquivo vai servir com base de referência para o programa identificar os lugares corretos para borrar.\n\n"

                "2. Desenhe retângulos vermelhos nas áreas que deseja borrar.\n"
                "- Clique e segure para começar a criar o retângulo, arraste até a área que deseja e solte.\n\n"

                "3. Use 'Borrar Arquivos da Pasta' para aplicar a mesma edição em vários PDFs.\n"
                "- Selecione a pasta que contenha somente os PDF que deseja borrar. Ao final do processo ele vai criar uma subpasta 'Borrados'.\n\n"

                "Opcional: Caso opte por borrar e salvar apenas um arquivo, use 'Salvar Somente PDF de Referência'.\n\n"

                "Desenvolvido por Matheus Maia."

            ),
            fill="gray",
            font=("Segoe UI", 14),
            width=900, 
            justify=tk.CENTER
        )

    def carregar_pdf(self):
        self.pdf_path = filedialog.askopenfilename(filetypes=[("Arquivos PDF", "*.pdf")])
        if not self.pdf_path:
            return

        self.canvas.delete(self.texto_tutorial_id)

        doc = fitz.open(self.pdf_path)
        page = doc.load_page(0)
        pix = page.get_pixmap(dpi=150)
        image_path = "pagina_temp.png"
        pix.save(image_path)

        img = Image.open(image_path)
        self.page_image = img
        self.tk_img = ImageTk.PhotoImage(img)

        self.canvas.config(scrollregion=(0, 0, img.width, img.height))
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_img)
        self.retangulos.clear()
        os.remove(image_path)

    def iniciar_desenho(self, event):
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)
        self.rect_start = (x, y)
        self.rect_id = self.canvas.create_rectangle(x, y, x, y, outline="red", width=2)

    def desenhar(self, event):
        if self.rect_id:
            x = self.canvas.canvasx(event.x)
            y = self.canvas.canvasy(event.y)
            self.canvas.coords(self.rect_id, self.rect_start[0], self.rect_start[1], x, y)

    def finalizar_desenho(self, event):
        if self.rect_id:
            coords = self.canvas.coords(self.rect_id)
            self.retangulos.append(coords)
            print(f"Retângulo salvo: {coords}")
            self.rect_id = None

    def salvar_pdf(self):
        if not self.pdf_path or not self.retangulos:
            messagebox.showwarning("Aviso", "Carregue um PDF e desenhe ao menos um retângulo.")
            return

        doc = fitz.open(self.pdf_path)
        page = doc.load_page(0)

        scale_x = page.rect.width / self.page_image.width
        scale_y = page.rect.height / self.page_image.height

        for coords in self.retangulos:
            x0, y0, x1, y1 = coords
            rect_pdf = fitz.Rect(
                x0 * scale_x,
                y0 * scale_y,
                x1 * scale_x,
                y1 * scale_y
            )
            page.add_redact_annot(rect_pdf, fill=(0, 0, 0))

        page.apply_redactions()

        saida = os.path.splitext(self.pdf_path)[0] + "_borrado.pdf"
        doc.save(saida)
        doc.close()

        messagebox.showinfo("Sucesso", f"PDF salvo com redações em:\n{saida}")

    def selecionar_pasta_e_borrar(self):
        if not self.retangulos:
            messagebox.showwarning("Aviso", "Você precisa desenhar ao menos um retângulo no PDF de referência antes.")
            return

        pasta_origem = filedialog.askdirectory(title="Selecione a pasta com PDFs")
        if not pasta_origem:
            return

        pasta_saida = os.path.join(pasta_origem, "borrados")
        os.makedirs(pasta_saida, exist_ok=True)

        total = 0
        erros = 0

        for nome_arquivo in os.listdir(pasta_origem):
            if nome_arquivo.lower().endswith('.pdf'):
                caminho_entrada = os.path.join(pasta_origem, nome_arquivo)
                caminho_saida = os.path.join(pasta_saida, nome_arquivo)

                try:
                    self.borrar_pdf(caminho_entrada, caminho_saida)
                    total += 1
                except Exception as e:
                    print(f"Erro ao processar {nome_arquivo}: {e}")
                    erros += 1

        messagebox.showinfo(
            "Finalizado",
            f"{total} arquivo(s) processado(s) com sucesso.\n{erros} erro(s)."
        )

    def borrar_pdf(self, caminho_entrada, caminho_saida):
        doc = fitz.open(caminho_entrada)
        page = doc.load_page(0)

        scale_x = page.rect.width / self.page_image.width
        scale_y = page.rect.height / self.page_image.height

        for coords in self.retangulos:
            x0, y0, x1, y1 = coords
            rect_pdf = fitz.Rect(
                x0 * scale_x,
                y0 * scale_y,
                x1 * scale_x,
                y1 * scale_y
            )
            page.add_redact_annot(rect_pdf, fill=(0, 0, 0))

        page.apply_redactions()
        doc.save(caminho_saida)
        doc.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFEditorApp(root)
    root.mainloop()
