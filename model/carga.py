import sqlite3
import os

def insert_data_into_tarefa_tipo(database_path):
    # Conecta ao banco de dados SQLite
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    
    # Comandos SQL para inserir dados
    insert_commands = [
        "delete from tarefa_padrao;",
        "delete from bloco_padrao;",
        "delete from tarefa_tipo;",        
        "INSERT INTO tarefa_tipo (id_tarefa_tipo, descricao, tempo) VALUES (1, 'Dormir', 300);",
        "INSERT INTO tarefa_tipo (id_tarefa_tipo, descricao, tempo) VALUES (2, 'Preparar e tomar café da manhã com a família', 60);",
        "INSERT INTO tarefa_tipo (id_tarefa_tipo, descricao, tempo) VALUES (3, 'Preparar as crianças para a escola', 30);",
        "INSERT INTO tarefa_tipo (id_tarefa_tipo, descricao, tempo) VALUES (4, 'Deslocamento para o trabalho', 30);",
        "INSERT INTO tarefa_tipo (id_tarefa_tipo, descricao, tempo) VALUES (5, 'Trabalho - Desenvolvimento de software', 180);",
        "INSERT INTO tarefa_tipo (id_tarefa_tipo, descricao, tempo) VALUES (6, 'Reunião de equipe', 60);",
        "INSERT INTO tarefa_tipo (id_tarefa_tipo, descricao, tempo) VALUES (7, 'Trabalho - Revisão de código', 120);",
        "INSERT INTO tarefa_tipo (id_tarefa_tipo, descricao, tempo) VALUES (8, 'Almoço', 60);",
        "INSERT INTO tarefa_tipo (id_tarefa_tipo, descricao, tempo) VALUES (9, 'Trabalho - Planejamento de projetos', 120);",
        "INSERT INTO tarefa_tipo (id_tarefa_tipo, descricao, tempo) VALUES (10, 'Estudar para a pós-graduação - Teoria', 90);",
        "INSERT INTO tarefa_tipo (id_tarefa_tipo, descricao, tempo) VALUES (11, 'Deslocamento para casa', 30);",
        "INSERT INTO tarefa_tipo (id_tarefa_tipo, descricao, tempo) VALUES (12, 'Jogar com as crianças', 60);",
        "INSERT INTO tarefa_tipo (id_tarefa_tipo, descricao, tempo) VALUES (13, 'Jantar com a família', 60);",
        "INSERT INTO tarefa_tipo (id_tarefa_tipo, descricao, tempo) VALUES (14, 'Leitura noturna com as crianças', 30);",
        "INSERT INTO tarefa_tipo (id_tarefa_tipo, descricao, tempo) VALUES (15, 'Tempo livre com a esposa', 90);",
        "INSERT INTO tarefa_tipo (id_tarefa_tipo, descricao, tempo) VALUES (16, 'Estudar para a pós-graduação - Prática', 60);",
        "INSERT INTO tarefa_tipo (id_tarefa_tipo, descricao, tempo) VALUES (17, 'Preparação para dormir', 60);",
        "INSERT INTO tarefa_tipo (id_tarefa_tipo, descricao, tempo) VALUES (18, 'Passeio no parque com a família', 180);",
        "INSERT INTO tarefa_tipo (id_tarefa_tipo, descricao, tempo) VALUES (19, 'Compras no supermercado', 90);",
        "INSERT INTO tarefa_tipo (id_tarefa_tipo, descricao, tempo) VALUES (20, 'Almoço especial de sábado', 90);",
        "INSERT INTO tarefa_tipo (id_tarefa_tipo, descricao, tempo) VALUES (21, 'Sessão de cinema em casa', 120);",
        "INSERT INTO tarefa_tipo (id_tarefa_tipo, descricao, tempo) VALUES (22, 'Manutenção da casa', 60);",
        "INSERT INTO tarefa_tipo (id_tarefa_tipo, descricao, tempo) VALUES (23, 'Jantar fora', 90);",
        "INSERT INTO tarefa_tipo (id_tarefa_tipo, descricao, tempo) VALUES (24, 'Café da manhã tardio', 60);",
        "INSERT INTO tarefa_tipo (id_tarefa_tipo, descricao, tempo) VALUES (25, 'Visita à família ou amigos', 180);",
        "INSERT INTO tarefa_tipo (id_tarefa_tipo, descricao, tempo) VALUES (26, 'Churrasco em família', 180);",
        "INSERT INTO tarefa_tipo (id_tarefa_tipo, descricao, tempo) VALUES (27, 'Preparativos para a semana', 60);",
        "INSERT INTO tarefa_tipo (id_tarefa_tipo, descricao, tempo) VALUES (28, 'Hora do conto', 30);",
        "INSERT INTO bloco_padrao (id_bloco_padrao, descricao, tempo, dias_semana) VALUES (1, 'Dia de Semana', 1440, '0111110');",
        "INSERT INTO bloco_padrao (id_bloco_padrao, descricao, tempo, dias_semana) VALUES (2, 'Sábado', 1440, '0000001');",
        "INSERT INTO bloco_padrao (id_bloco_padrao, descricao, tempo, dias_semana) VALUES (3, 'Domingo', 1440, '1000000');",
        "INSERT INTO tarefa_padrao (id_bloco_padrao, id_tarefa_tipo, detalhes, tempo) VALUES (1, 1, 'Dormir', 480);",  
        "INSERT INTO tarefa_padrao (id_bloco_padrao, id_tarefa_tipo, detalhes, tempo) VALUES (1, 2, 'Preparar e tomar café da manhã com a família', 60);",          
        "INSERT INTO tarefa_padrao (id_bloco_padrao, id_tarefa_tipo, detalhes, tempo) VALUES (1, 4, 'Deslocamento para o trabalho', 60);",  
        "INSERT INTO tarefa_padrao (id_bloco_padrao, id_tarefa_tipo, detalhes, tempo) VALUES (1, 5, 'Trabalho - Desenvolvimento de software', 240);",          
        "INSERT INTO tarefa_padrao (id_bloco_padrao, id_tarefa_tipo, detalhes, tempo) VALUES (1, 8, 'Almoço', 60);",  
        "INSERT INTO tarefa_padrao (id_bloco_padrao, id_tarefa_tipo, detalhes, tempo) VALUES (1, 9, 'Trabalho - Planejamento de projetos', 180);",  
        "INSERT INTO tarefa_padrao (id_bloco_padrao, id_tarefa_tipo, detalhes, tempo) VALUES (1, 10, 'Estudar para a pós-graduação - Teoria', 120);",  
        "INSERT INTO tarefa_padrao (id_bloco_padrao, id_tarefa_tipo, detalhes, tempo) VALUES (1, 11, 'Deslocamento para casa', 60);",                  
        "INSERT INTO tarefa_padrao (id_bloco_padrao, id_tarefa_tipo, detalhes, tempo) VALUES (1, 13, 'Jantar com a família', 60);",          
        "INSERT INTO tarefa_padrao (id_bloco_padrao, id_tarefa_tipo, detalhes, tempo) VALUES (1, 15, 'Tempo livre com a esposa', 90);",          
        "INSERT INTO tarefa_padrao (id_bloco_padrao, id_tarefa_tipo, detalhes, tempo) VALUES (1, 17, 'Preparação para dormir', 60);",
        "INSERT INTO tarefa_padrao (id_bloco_padrao, id_tarefa_tipo, detalhes, tempo) VALUES (2, 1, 'Dormir', 540);",
        "INSERT INTO tarefa_padrao (id_bloco_padrao, id_tarefa_tipo, detalhes, tempo) VALUES (2, 2, 'Preparar e tomar café da manhã com a família', 60);",
        "INSERT INTO tarefa_padrao (id_bloco_padrao, id_tarefa_tipo, detalhes, tempo) VALUES (2, 19, 'Compras no supermercado', 120);",
        "INSERT INTO tarefa_padrao (id_bloco_padrao, id_tarefa_tipo, detalhes, tempo) VALUES (2, 18, 'Passeio no parque com a família', 180);",
        "INSERT INTO tarefa_padrao (id_bloco_padrao, id_tarefa_tipo, detalhes, tempo) VALUES (2, 20, 'Almoço especial de sábado', 90);",
        "INSERT INTO tarefa_padrao (id_bloco_padrao, id_tarefa_tipo, detalhes, tempo) VALUES (2, 22, 'Manutenção da casa', 120);",
        "INSERT INTO tarefa_padrao (id_bloco_padrao, id_tarefa_tipo, detalhes, tempo) VALUES (2, 21, 'Sessão de cinema em casa', 120);",
        "INSERT INTO tarefa_padrao (id_bloco_padrao, id_tarefa_tipo, detalhes, tempo) VALUES (2, 23, 'Jantar fora', 90);",
        "INSERT INTO tarefa_padrao (id_bloco_padrao, id_tarefa_tipo, detalhes, tempo) VALUES (2, 15, 'Tempo livre com a esposa', 90);",
        "INSERT INTO tarefa_padrao (id_bloco_padrao, id_tarefa_tipo, detalhes, tempo) VALUES (2, 17, 'Preparação para dormir', 60);",
        "INSERT INTO tarefa_padrao (id_bloco_padrao, id_tarefa_tipo, detalhes, tempo) VALUES (3, 1, 'Dormir', 540);",
        "INSERT INTO tarefa_padrao (id_bloco_padrao, id_tarefa_tipo, detalhes, tempo) VALUES (3, 24, 'Café da manhã tardio', 60);",
        "INSERT INTO tarefa_padrao (id_bloco_padrao, id_tarefa_tipo, detalhes, tempo) VALUES (3, 25, 'Visita à família ou amigos', 240);",
        "INSERT INTO tarefa_padrao (id_bloco_padrao, id_tarefa_tipo, detalhes, tempo) VALUES (3, 26, 'Churrasco em família', 240);",
        "INSERT INTO tarefa_padrao (id_bloco_padrao, id_tarefa_tipo, detalhes, tempo) VALUES (3, 27, 'Preparativos para a semana', 120);",
        "INSERT INTO tarefa_padrao (id_bloco_padrao, id_tarefa_tipo, detalhes, tempo) VALUES (3, 28, 'Hora do conto', 60);",
        "INSERT INTO tarefa_padrao (id_bloco_padrao, id_tarefa_tipo, detalhes, tempo) VALUES (3, 13, 'Jantar com a família', 60);",
        "INSERT INTO tarefa_padrao (id_bloco_padrao, id_tarefa_tipo, detalhes, tempo) VALUES (3, 17, 'Preparação para dormir', 60);",
        "INSERT INTO tarefa_padrao (id_bloco_padrao, id_tarefa_tipo, detalhes, tempo) VALUES (3, 15, 'Tempo livre com a esposa', 30);"
        ]
    
    # Executando os comandos
    try:
        for command in insert_commands:
            print("------------------- NOVO ---------------------------------------------------")
            print(command)
            cursor.execute(command)            
        conn.commit()
        print("Dados inseridos com sucesso.")
    except sqlite3.Error as e:
        print(f"Ocorreu um erro ao inserir dados: {e}")
    finally:
        conn.close()

if __name__ == '__main__':

    db_name = "db.sqlite4"

    db_path = os.path.join(os.getcwd(), "database")
    print(db_path)
    db_path = os.path.join(db_path, db_name)

    insert_data_into_tarefa_tipo(db_path)
