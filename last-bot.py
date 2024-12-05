import customtkinter as ctk
import pandas as pd

class Chatbot:
    def __init__(self, master, data):
        self.master = master
        self.data = data
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
        self.text_area.insert(ctk.END, "Olá! Me informe o protocolo ou a data e hora que você deseja consultar.\n")
        self.text_area.configure(state="disabled")

        # Campo de entrada
        self.entry = ctk.CTkEntry(master, width=500, placeholder_text="Digite o protocolo ou a data e hora...")
        self.entry.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        self.entry.bind("<Return>", self.process_input)

        # Botão de envio
        self.send_button = ctk.CTkButton(master, text="Enviar", fg_color="blue", command=self.process_input)
        self.send_button.grid(row=2, column=0, padx=20, pady=10)

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

                # Filtrar a planilha
                result = self.data[
                    (self.data['solicitacao_data'].str.startswith(data)) & 
                    (self.data['solicitacao_hora'] == hora)
                ]

                if not result.empty:
                    return self.format_response(result.iloc[0])
            
            # Caso o input seja apenas protocolo
            result = self.data[self.data['processo_numero'] == user_input.strip()]
            if not result.empty:
                return self.format_response(result.iloc[0])

            return "Dados não encontrados para o protocolo, data ou hora especificados."
        except Exception as e:
            return f"Erro ao processar os dados: {e}"

    def format_response(self, row):
        return "\n".join([
            f"Protocolo: {row['processo_numero']}",
            f"Data: {row['solicitacao_data']}",
            f"Hora: {row['solicitacao_hora']}",
            f"Descrição: {row['solicitacao_descricao']}",
            f"Situação: {row['processo_situacao']}",
            f"Bairro: {row['solicitacao_bairro']}",
            f"Endereço: {row['solicitacao_endereco']}",
        ])

if __name__ == "__main__":
    # Carregar a planilha
    file_path = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vQxv0s8YI31UYgsD0C0llc8XY0haohAEveQmYw40ua7WYRDTqtgX4PFBHcvxdV9ftzmUT0RLtO9aXLq/pub?output=csv'
    data = pd.read_csv(file_path)

    # Inicializar o chatbot
    root = ctk.CTk()
    chatbot = Chatbot(root, data)
    root.mainloop()
