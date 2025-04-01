from flask import Flask, request, jsonify
import pandas as pd
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  

df_operadoras = pd.read_csv('operadoras_ativas.csv', encoding='utf-8', delimiter=';')

@app.route('/api/buscar', methods=['GET'])
def buscar_operadoras():
    termo = request.args.get('q', '')
    
    if not termo:
        return jsonify([])
    
    resultados = df_operadoras[
        df_operadoras['razao_social'].str.contains(termo, case=False, na=False) |
        df_operadoras['nome_fantasia'].str.contains(termo, case=False, na=False)
    ].head(50).to_dict(orient='records')
    
    return jsonify(resultados)

if __name__ == '__main__':
    app.run(debug=True, port=5000)