from flask import Flask, request, jsonify
import pandas as pd
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # Habilita CORS para todas as rotas

def carregar_dados_operadoras():
    """
    Carrega os dados das operadoras de saúde com tratamento robusto para diferentes formatos de arquivo
    """
    try:
        # Caminho absoluto do arquivo
        base_dir = os.path.dirname(os.path.abspath(__file__))
        csv_path = os.path.join(base_dir, 'operadoras_ativas.csv')
        
        print(f"Tentando carregar arquivo em: {csv_path}")
        
        # Tenta diferentes encodings comuns em arquivos da ANS
        encodings = ['utf-8', 'latin1', 'iso-8859-1', 'cp1252']
        
        for encoding in encodings:
            try:
                # Carrega apenas os primeiros registros para teste
                df = pd.read_csv(csv_path, sep=';', encoding=encoding, nrows=5)
                
                # Verifica se encontrou colunas relevantes
                colunas_encontradas = df.columns.str.lower().tolist()
                colunas_necessarias = ['razão social', 'razao_social', 'nome fantasia', 'nome_fantasia', 'registro']
                
                if any(col in ' '.join(colunas_encontradas) for col in colunas_necessarias):
                    # Carrega o arquivo completo
                    df = pd.read_csv(csv_path, sep=';', encoding=encoding)
                    
                    # Padroniza nomes de colunas
                    df.columns = df.columns.str.strip().str.lower()
                    
                    # Mapeamento de colunas alternativas
                    nome_colunas = {
                        'razao_social': ['razão social', 'razaosocial', 'nome_operadora'],
                        'nome_fantasia': ['nome fantasia', 'nomefantasia', 'fantasia'],
                        'registro_ans': ['registro ans', 'registro', 'cd_operadora']
                    }
                    
                    # Renomeia colunas para padrão
                    for padrao, alternativas in nome_colunas.items():
                        for alt in alternativas:
                            if alt in df.columns:
                                df = df.rename(columns={alt: padrao})
                                break
                    
                    print("Colunas disponíveis:", df.columns.tolist())
                    return df
                
            except UnicodeDecodeError:
                continue
            except Exception as e:
                print(f"Tentativa com encoding {encoding} falhou: {str(e)}")
                continue
        
        raise Exception("Não foi possível identificar o formato correto do arquivo CSV")
    
    except Exception as e:
        print(f"Erro ao carregar arquivo: {str(e)}")
        return None

# Carrega os dados ao iniciar
df_operadoras = carregar_dados_operadoras()

@app.route('/api/buscar', methods=['GET'])
def buscar_operadoras():
    """
    Endpoint para busca de operadoras por termo
    """
    try:
        if df_operadoras is None:
            return jsonify({"error": "Dados não disponíveis"}), 503
            
        termo = request.args.get('q', '').strip()
        
        if not termo or len(termo) < 2:
            return jsonify({"error": "Forneça um termo de busca com pelo menos 2 caracteres"}), 400
        
        # Verifica quais colunas estão disponíveis para busca
        colunas_busca = []
        if 'razao_social' in df_operadoras.columns:
            colunas_busca.append('razao_social')
        if 'nome_fantasia' in df_operadoras.columns:
            colunas_busca.append('nome_fantasia')
        
        if not colunas_busca:
            return jsonify({"error": "Nenhuma coluna disponível para busca"}), 500
        
        # Filtra os resultados
        mask = pd.Series(False, index=df_operadoras.index)
        for col in colunas_busca:
            mask = mask | df_operadoras[col].str.contains(termo, case=False, na=False)
        
        resultados = df_operadoras[mask].head(50)
        
        # Remove valores NaN e converte para dict
        resultados = resultados.where(pd.notnull(resultados), None).to_dict('records')
        
        return jsonify(resultados)
    
    except Exception as e:
        return jsonify({"error": f"Erro na busca: {str(e)}"}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """
    Endpoint para verificação do status da API
    """
    status = {
        "status": "OK" if df_operadoras is not None else "ERROR",
        "operadoras_carregadas": len(df_operadoras) if df_operadoras is not None else 0,
        "colunas_disponiveis": list(df_operadoras.columns) if df_operadoras is not None else []
    }
    return jsonify(status)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)