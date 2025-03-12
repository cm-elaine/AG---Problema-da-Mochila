
# AG para problema da Mochila - Frontend React (Versão com Valor Máximo, Média e Sliders de Parâmetros)

Este projeto implementa uma interface web interativa para o algoritmo genético do problema da mochila.

O gráfico mostra:
- **Linha Azul:** Valor Máximo da População em cada geração.
- **Linha Verde:** Média de Fitness da População em cada geração.

Além disso, a interface inclui **sliders interativos** para ajuste dos seguintes parâmetros:
- ✅ Número de Gerações
- ✅ Tamanho da População
- ✅ Taxa de Mutação

---

## ✅ Tecnologias Usadas
- React + Vite + TypeScript
- Recharts para visualização do gráfico de evolução
- HTML/CSS nativo (sem UI frameworks externos)

---

## ▶ Como Executar

1. **Abra a pasta no VS Code**
2. **Abra o terminal e instale as dependências:**
```bash
npm install
```

3. **Execute o projeto:**
```bash
npm run dev
```

4. **Acesse no navegador:**
```
http://localhost:5173 ou conforme o servidor apresentado em seu terminal.
```

---

## 📂 Estrutura
```
src/
├── App.tsx          // Componente principal (interface com inputs, sliders e gráfico)
├── main.tsx         // Ponto de entrada do React
index.html
vite.config.js
package.json
```

---
