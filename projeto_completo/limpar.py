import sqlite3


def vincular_e_limpar():
    conn = sqlite3.connect("sistema.db")
    cursor = conn.cursor()

    # 1. Mapeia as colunas da tabela 'processos' para achar o campo do advogado
    cursor.execute("PRAGMA table_info(processos)")
    colunas_processos = [col[1].lower() for col in cursor.fetchall()]

    # Identifica como a coluna foi escrita (advogado, advogado_id, nome_advogado, etc.)
    coluna_adv_processo = None
    for col in colunas_processos:
        if "advogado" in col:
            coluna_adv_processo = col
            break

    if not coluna_adv_processo:
        print(
            "Erro: Não foi possível encontrar a coluna de advogado na tabela 'processos'."
        )
        conn.close()
        return

    # 2. Atualiza TODOS os processos para o advogado 'Teste2'
    print(
        f"Atualizando todos os processos usando a coluna '{coluna_adv_processo}' para 'Teste2'..."
    )
    cursor.execute(f"UPDATE processos SET {coluna_adv_processo} = 'Teste2'")
    conn.commit()
    print("-> Todos os processos foram vinculados ao 'Teste2' com sucesso!")

    # 3. Ativa as chaves estrangeiras e roda a remoção interativa
    cursor.execute("PRAGMA foreign_keys = ON")

    while True:
        cursor.execute("SELECT rowid, Advogado FROM advogados")
        usuarios = cursor.fetchall()

        if not usuarios:
            print("\nNão há mais advogados cadastrados no banco.")
            break

        print("\n--- LISTA DE ADVOGADOS ---")
        for user in usuarios:
            print(f"[{user[0]}] - {user[1]}")

        print("[0] - Sair do programa")

        escolha = input(
            "\nDigite o número (ID) do advogado que deseja APAGAR (ex: o do 'Ja'): "
        )

        if escolha == "0":
            print("Saindo...")
            break

        try:
            id_deletar = int(escolha)
            mapa_usuarios = {u[0]: u[1] for u in usuarios}

            if id_deletar in mapa_usuarios:
                nome_advogado = mapa_usuarios[id_deletar]

                if nome_advogado == "Teste2":
                    print(
                        "⚠️ Você não deve apagar o 'Teste2', pois ele agora cuida de todos os processos!"
                    )
                    continue

                cursor.execute("DELETE FROM advogados WHERE rowid = ?", (id_deletar,))
                conn.commit()
                print(f"-> Advogado '{nome_advogado}' foi apagado com sucesso!")
            else:
                print("ID inválido! Escolha um número da lista.")
        except ValueError:
            print("Por favor, digite apenas números.")

    conn.close()


if __name__ == "__main__":
    vincular_e_limpar()
