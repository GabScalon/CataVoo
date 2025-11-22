import tkinter as tk
from view import TelaGerenciamento
from persistence import (PilotoDAO, VooDAO, CompanhiaDAO, 
                         AeronaveDAO, EnderecoDAO)
from modelo import Piloto, Voo, CompanhiaAerea, Aeronave, Endereco
from datetime import datetime

def criar_dados_simulacao():
    """
    Cria dados falsos se os arquivos .pkl não existirem para testar as regras de dependência
    """
    try:
        c_dao = CompanhiaDAO()
        a_dao = AeronaveDAO()
        p_dao = PilotoDAO()
        v_dao = VooDAO()
        end_dao = EnderecoDAO()
        
        if not p_dao.get_all() and not c_dao.get_all():
            print("Simulando: Criando Piloto para teste de dependência...")
            
            end_a3 = Endereco(rua="Rua Piloto", cidade="SP", estado="SP", pais="BR")
            end_a3_salvo = end_dao.salvar(end_a3) 
            
            # Usando nova classe CompanhiaAerea e setEndereco
            comp_a3 = CompanhiaAerea(nome="Companhia com Piloto")
            comp_a3.setEndereco(end_a3_salvo)
            comp_a3_salva = c_dao.salvar(comp_a3) 
            
            assert comp_a3_salva.id is not None
            p_dao.salvar(Piloto(nome="Cmdt. Silva", companhia_id=comp_a3_salva.id)) 
            print(f"-> Companhia ID {comp_a3_salva.id} criada com 1 piloto dependente.")
        
        # --- Simulação Dependência de Voo ---
        if not v_dao.get_all():
            print("Simulando: Criando Voo para teste de dependência...")
             
            comp_b3 = c_dao.get_by_id(1)
            if not comp_b3:
                end_b3 = Endereco(rua="Rua Voo", cidade="RJ", estado="RJ", pais="BR")
                end_b3_salvo = end_dao.salvar(end_b3)
                
                comp_b3 = CompanhiaAerea(nome="Companhia com Voo")
                comp_b3.setEndereco(end_b3_salvo)
                comp_b3 = c_dao.salvar(comp_b3)

            assert comp_b3.id is not None

            aero_b3 = Aeronave(modelo="A320-VOO", companhia_id=comp_b3.id,
                                capacidadeDeCarga=1000, lotacaoMaxima=150)
            aero_b3_salva = a_dao.salvar(aero_b3)
             
            piloto_id_simulado = 1 # Assume que o Piloto ID 1 existe
            
            assert aero_b3_salva.id is not None
            v_dao.salvar(Voo(codigo="AA123", aeronave_id=aero_b3_salva.id,  
                            companhia_id=comp_b3.id, piloto_id=piloto_id_simulado, 
                            localDeSaida_id=1, destino_id=2,
                            horarioDePartidaPrevisto=datetime.now(),
                            horarioDeChegadaPrevisto=datetime.now()))
            print(f"-> Aeronave ID {aero_b3_salva.id} criada com 1 voo dependente.")

    except Exception as e:
        print(f"ERRO ao criar dados de simulação: {e}")
        print("-> Por favor, delete os arquivos .pkl se houver inconsistência.")


if __name__ == "__main__":

    # Prepara o banco de dados de simulação (se necessário)
    criar_dados_simulacao()

    # Inicia a interface gráfica (View)
    root = tk.Tk()
    app = TelaGerenciamento(root)
    app.pack(fill="both", expand=True)
    root.mainloop()