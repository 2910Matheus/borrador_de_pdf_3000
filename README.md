# Blur_PDF v2.1 🕵️‍♂️🔒

**Interface gráfica para redigir (borrar) automaticamente áreas de múltiplos PDFs com base em um PDF de referência.**

> Desenvolvido por Matheus Maia

---

## ✨ Funcionalidades

- 📂 **Carregue um PDF de referência**
- 📐 **Desenhe áreas a serem borradas diretamente com o mouse**
- 🔁 **Aplique os mesmos redactions em múltiplos PDFs de uma pasta**
- 💾 **Opcionalmente, salve apenas o PDF de referência com as áreas redigidas**
- 🎨 Interface intuitiva e responsiva feita com Tkinter

---

## 🖼️ Demonstração Visual

```
1. Clique em "Carregar PDF de Referência"
2. Desenhe os retângulos vermelhos nas áreas que deseja borrar
3. Clique em "Borrar Arquivos da Pasta" para aplicar nos demais PDFs
```

---

## 🛠️ Requisitos

Instale os pacotes necessários com:

```bash
pip install PyMuPDF Pillow
```

---

## 🚀 Como Usar

1. **Execute o programa**:
    ```bash
    python blur_pdf.py
    ```

2. **Passo a passo**:
   - Clique em **"Carregar PDF de Referência"** e escolha um arquivo PDF.
   - Desenhe **retângulos vermelhos** nas áreas que devem ser borradas (clique e arraste).
   - Para aplicar o mesmo redaction em múltiplos arquivos, clique em **"Borrar Arquivos da Pasta"** e escolha uma pasta com PDFs. Os arquivos editados serão salvos em uma subpasta `borrados/`.
   - Ou clique em **"Salvar Somente PDF de Referência"** se quiser exportar só o PDF editado.

---

## 📁 Estrutura de Saída

Ao borrar arquivos em massa, os PDFs editados são salvos em:
```
/sua-pasta/
└── borrados/
    ├── arquivo1.pdf
    ├── arquivo2.pdf
    └── ...
```

---

## 📌 Observações

- O programa considera **apenas a primeira página** dos PDFs.
- O redaction (borrão) é feito de forma **permanente** e **irreversível**.
- O arquivo de referência deve ter a **mesma estrutura visual** dos arquivos a serem processados.

---

## 🧠 Tecnologias Utilizadas

- [Python 3](https://www.python.org/)
- [Tkinter](https://docs.python.org/3/library/tkinter.html) – GUI nativa do Python
- [PyMuPDF (fitz)](https://pymupdf.readthedocs.io/en/latest/) – Manipulação de PDF
- [Pillow](https://python-pillow.org/) – Processamento de imagens

---

## 🧑‍💻 Autor

**Matheus Maia**  
Este projeto foi criado com o intuito de facilitar a edição em massa de documentos PDF com redactions visuais consistentes e seguros.

---

## 📃 Licença

Este projeto está disponível sob a licença MIT.  
Sinta-se livre para usar, modificar e distribuir com os devidos créditos.
