
import React, { useState } from "react";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from "recharts";

export default function KnapsackAGApp() {
  const [capacidade, setCapacidade] = useState(50);
  const [pesos, setPesos] = useState("10,20,30,5,8,12,6");
  const [valores, setValores] = useState("60,100,120,30,40,50,45");
  const [resultados, setResultados] = useState(null);
  const [graficoData, setGraficoData] = useState([]);
  const [geracoes, setGeracoes] = useState(100);
  const [populacao, setPopulacao] = useState(100);
  const [mutacao, setMutacao] = useState(0.01);

  const simularAG = () => {
    const pesosArray = pesos.split(",").map(Number);
    const valoresArray = valores.split(",").map(Number);
    const historico = [];
    const mediaFitness = [];

    const fitness = (ind) => {
      const peso = ind.reduce((acc, val, i) => acc + (val ? pesosArray[i] : 0), 0);
      const valor = ind.reduce((acc, val, i) => acc + (val ? valoresArray[i] : 0), 0);
      return peso > capacidade ? 0 : valor;
    };

    const criarPop = (tam, n) =>
      Array.from({ length: tam }, () => Array.from({ length: n }, () => (Math.random() < 0.5 ? 1 : 0)));

    const crossover = (p1, p2) => {
      const pt = Math.floor(Math.random() * (p1.length - 1)) + 1;
      return [p1.slice(0, pt).concat(p2.slice(pt)), p2.slice(0, pt).concat(p1.slice(pt))];
    };

    const mutacao = (ind, taxa) => ind.map((g) => (Math.random() < taxa ? 1 - g : g));

    let pop = criarPop(populacao, pesosArray.length);
    for (let g = 0; g < geracoes; g++) {
      pop.sort((a, b) => fitness(b) - fitness(a));
      historico.push(fitness(pop[0]));
      const media = pop.reduce((acc, ind) => acc + fitness(ind), 0) / pop.length;
      mediaFitness.push(media);
      const novaPop = pop.slice(0, 50);
      while (novaPop.length < 100) {
        const [p1, p2] = [novaPop[Math.floor(Math.random() * 50)], novaPop[Math.floor(Math.random() * 50)]];
        let [f1, f2] = crossover(p1, p2);
        novaPop.push(mutacao(f1, mutacao));
        novaPop.push(mutacao(f2, mutacao));
      }
      pop = novaPop;
    }

    const best = pop.reduce((a, b) => (fitness(a) > fitness(b) ? a : b));
    const itens = best.map((v, i) => (v ? i : null)).filter((v) => v !== null);
    setResultados({ valor: fitness(best), itens });
    setGraficoData(historico.map((v, i) => ({ geracao: i + 1, valor: v, media: mediaFitness[i] })));
  };

  return (
    <div style={{ maxWidth: 800, margin: '0 auto', padding: 20 }}>
      <h2>Algoritmo Genético - Problema da Mochila</h2>
<div style={{ marginBottom: 10 }}>
<label>Gerações: </label>
<input type="range" min="10" max="500" value={geracoes} onChange={(e) => setGeracoes(Number(e.target.value))} /> {geracoes}
</div>
<div style={{ marginBottom: 10 }}>
<label>Tamanho da População: </label>
<input type="range" min="10" max="300" value={populacao} onChange={(e) => setPopulacao(Number(e.target.value))} /> {populacao}
</div>
<div style={{ marginBottom: 10 }}>
<label>Taxa de Mutação: </label>
<input type="range" min="0.001" max="0.2" step="0.001" value={mutacao} onChange={(e) => setMutacao(Number(e.target.value))} /> {mutacao}
</div>
      <div style={{ marginBottom: 10 }}>
        <label>Capacidade da Mochila: </label>
        <input type="number" value={capacidade} onChange={(e) => setCapacidade(parseInt(e.target.value))} />
      </div>
      <div style={{ marginBottom: 10 }}>
        <label>Pesos dos Itens (vírgula): </label>
        <input value={pesos} onChange={(e) => setPesos(e.target.value)} />
      </div>
      <div style={{ marginBottom: 10 }}>
        <label>Valores dos Itens (vírgula): </label>
        <input value={valores} onChange={(e) => setValores(e.target.value)} />
      </div>
      <button onClick={simularAG} style={{ padding: '6px 12px', marginBottom: 20 }}>Executar AG</button>

      {resultados && (
        <div style={{ marginBottom: 20 }}>
          <p><strong>Valor Máximo:</strong> {resultados.valor}</p>
          <p><strong>Itens Selecionados:</strong> {resultados.itens.join(", ")}</p>
        </div>
      )}

      {graficoData.length > 0 && (
        <div>
          <h4>Evolução do Valor Máximo</h4>
          <LineChart width={600} height={300} data={graficoData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="geracao" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Line type="monotone" dataKey="valor" stroke="#8884d8" dot={false} />
<Line type="monotone" dataKey="media" stroke="#82ca9d" dot={false} />
          </LineChart>
        </div>
      )}
    </div>
  );
}
