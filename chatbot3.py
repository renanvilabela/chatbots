import customtkinter as ctk
import pandas as pd

class Chatbot:
    def __init__(self, master):
        self.master = master
        master.title("Artemis")
        master.geometry("800x600")

        # Configuração da janela
        master.grid_columnconfigure(0, weight=1)
        master.grid_rowconfigure(0, weight=1)
        master.grid_rowconfigure(1, weight=0)
        master.grid_rowconfigure(2, weight=0)

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        # Área de texto
        self.text_area = ctk.CTkTextbox(master, width=700, height=400, wrap="word")
        self.text_area.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.text_area.insert(ctk.END, "Olá! Me informe o número do processo ou a data, hora que você deseja consultar.\n")
        self.text_area.configure(state="disabled")

        # Campo de entrada
        self.entry = ctk.CTkEntry(master, width=500, placeholder_text="Digite o número do processo ou a data, hora...")
        self.entry.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        self.entry.bind("<Return>", self.process_input)

        # Botão de envio
        self.send_button = ctk.CTkButton(master, text="Enviar", fg_color="blue", command=self.process_input)
        self.send_button.grid(row=2, column=0, padx=20, pady=10)

        # Carregando os dados do CSV
        self.data = pd.read_csv("sedec_chamados.csv")

    def process_input(self, event=None):
        user_input = self.entry.get()
        if not user_input:
            return

        self.text_area.configure(state="normal")
        self.text_area.insert(ctk.END, "Você: " + user_input + "\n")
        self.text_area.configure(state="disabled")

        response = self.get_response(user_input)

        self.text_area.configure(state="normal")
        self.text_area.insert(ctk.END, "Artemis: " + response + "\n")
        self.text_area.configure(state="disabled")

        self.entry.delete(0, ctk.END)

    def get_response(self, user_input):
        try:
            # Verificar se o input contém uma data e hora no formato 'data, hora'
            if ',' in user_input:
                data, hora = user_input.split(',')
                data = data.strip()
                hora = hora.strip()

                resultado = self.data[
                    (self.data['solicitacao_data'].str.contains(data)) & 
                    (self.data['solicitacao_hora'].str.contains(hora))
                ]
            else:
                resultado = self.data[self.data['processo_numero'].astype(str) == user_input.strip()]

            if not resultado.empty:
                return resultado.iloc[0].to_string(index=False)
            else:
                return "Dados não encontrados para o número do processo ou data/hora especificados."
        except Exception as e:
            return f"Erro ao buscar os dados: {e}"

if __name__ == "__main__":
    root = ctk.CTk()
    chatbot = Chatbot(root)
    root.mainloop()
