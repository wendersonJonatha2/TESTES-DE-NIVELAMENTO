<template>
    <div class="container">
      <h1>Busca de Operadoras ANS</h1>
      <div class="search-box">
        <input 
          v-model="termoBusca" 
          @input="buscarOperadoras" 
          placeholder="Digite o nome da operadora..."
        />
      </div>
      
      <div v-if="resultados.length" class="results">
        <div v-for="op in resultados" :key="op.registro_ans" class="card">
          <h3>{{ op.nome_fantasia || op.razao_social }}</h3>
          <p><strong>Registro ANS:</strong> {{ op.registro_ans }}</p>
          <p><strong>CNPJ:</strong> {{ op.cnpj }}</p>
          <p><strong>UF:</strong> {{ op.uf }}</p>
        </div>
      </div>
      
      <div v-else-if="carregando" class="loading">Carregando...</div>
      <div v-else class="empty">Nenhum resultado encontrado</div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        termoBusca: '',
        resultados: [],
        carregando: false
      }
    },
    methods: {
      async buscarOperadoras() {
        if (this.termoBusca.length < 3) {
          this.resultados = [];
          return;
        }
        
        this.carregando = true;
        try {
          const response = await fetch(`http://localhost:5000/api/buscar?q=${this.termoBusca}`);
          this.resultados = await response.json();
        } catch (error) {
          console.error('Erro na busca:', error);
        } finally {
          this.carregando = false;
        }
      }
    }
  }
  </script>
  
  <style>
  .container {
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
  }
  .search-box {
    margin: 20px 0;
  }
  .search-box input {
    width: 100%;
    padding: 10px;
    font-size: 16px;
  }
  .results {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 15px;
  }
  .card {
    border: 1px solid #ddd;
    padding: 15px;
    border-radius: 5px;
  }
  .loading, .empty {
    text-align: center;
    padding: 20px;
    color: #666;
  }
  </style>