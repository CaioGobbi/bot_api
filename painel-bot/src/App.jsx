import { useEffect, useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [mensagens, setMensagens] = useState([]);

  useEffect(() => {
    const fetchMensagens = async () => {
      try {
        const response = await axios.get('http://localhost:8000/api/whatsapp/api/whatsapp/mensagens', {
          headers: {
            Authorization: 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJjYWlvZ29iYmkwMkBnbWFpbC5jb20iLCJleHAiOjE3NTQ0Mzg5MDB9.1Id7WVmlsiCggxBADBhL_uYWZxSJH3thGpbSZ-NmNbw' // troque pelo seu token real
          }
        });
        setMensagens(response.data);
      } catch (error) {
        console.error('Erro ao buscar mensagens:', error);
      }
    };

    fetchMensagens();
  }, []);

  return (
    <div className="App">
      <h1>📩 Mensagens Recebidas</h1>
      <table>
        <thead>
          <tr>
            <th>Telefone</th>
            <th>Mensagem</th>
            <th>Data</th>
          </tr>
        </thead>
        <tbody>
          {mensagens.map((msg) => (
            <tr key={msg.id}>
              <td>{msg.telefone}</td>
              <td>{msg.mensagem}</td>
              <td>{new Date(msg.criado_em).toLocaleString()}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default App;
