import tkinter as tk
from tkinter import messagebox

# Importa a tela do UC03 que está na subpasta
from gerenciar_aeronaves_e_companhias.view import TelaGerenciamento

# Importa os DAOs e Entidades para criar dados de teste
from persistent import CompanhiaAereaDAO, AeronaveDAO, PilotoDAO, EnderecoDAO
from entities import CompanhiaAerea, Endereco, Piloto, Aeronave

def criar_dados_iniciais():
    """Cria dados básicos caso o banco esteja vazio, para facilitar o teste."""
    try:
        c_dao = CompanhiaAereaDAO()
        
        # Só cria se não existir nenhuma companhia
        if not c_dao.get_all():
            print("--- Criando dados de teste para UC03 ---")
            end_dao = EnderecoDAO()
            
            end = Endereco(rua="Av. Paulista", numero=1000, cidade="São Paulo", 
                           estado="SP", pais="Brasil", bairro="Bela Vista")
            end_salvo = end_dao.salvar(end)
            
            comp = CompanhiaAerea(nome="Latam Teste", email="contato@latam.com", 
                                  numeroContato="1199999999")
            comp.setEndereco(end_salvo)
            comp_salva = c_dao.salvar(comp)
            
            print(f"Companhia '{comp_salva.nome}' criada com ID {comp_salva.id}.")

    except Exception as e:
        print(f"Aviso: Não foi possível criar dados de teste: {e}")

if __name__ == "__main__":
    # Prepara dados iniciais
    criar_dados_iniciais()

    # Configura a Janela Principal
    root = tk.Tk()
    root.title("Sistema CataVoo - Teste UC03")
    root.geometry("400x300")
    
    # Carrega a View do UC03
    app = TelaGerenciamento(root)
    app.pack(fill="both", expand=True)
    
    root.mainloop()