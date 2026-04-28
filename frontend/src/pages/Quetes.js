import React, { useState, useEffect } from 'react';
import { getMesQuetes, completerQuete } from '../services/api';

export default function Quetes() {
  const [quetes, setQuetes] = useState([]);
  const [message, setMessage] = useState('');

  useEffect(() => {
    getMesQuetes().then(r => setQuetes(r.data));
  }, []);

  const handleCompleter = async (quete_id) => {
    try {
      const res = await completerQuete(quete_id);
      setMessage(res.data.message);
      // Rafraîchir la liste
      getMesQuetes().then(r => setQuetes(r.data));
      setTimeout(() => setMessage(''), 3000);
    } catch (err) {
      setMessage('Quête déjà complétée ou erreur');
    }
  };

  const todo = quetes.filter(q => !q.completee);
  const done = quetes.filter(q => q.completee);

  return (
    <div className="page">
      <h1>⚔️ Mes Quêtes</h1>
      {message && <div className="toast">{message}</div>}

      <h2>📋 À compléter ({todo.length})</h2>
      <div className="quetes-list">
        {todo.map(uq => (
          <div key={uq.id} className="quete-item">
            <span className="quete-icone">{uq.quete.icone}</span>
            <div className="quete-info">
              <strong>{uq.quete.titre}</strong>
              <p>{uq.quete.description}</p>
            </div>
            <div className="quete-right">
              <span className="points-badge">+{uq.quete.points} XP</span>
              <button
                className="btn-complete"
                onClick={() => handleCompleter(uq.quete.id)}
              >
                Compléter ✅
              </button>
            </div>
          </div>
        ))}
      </div>

      <h2>✅ Complétées ({done.length})</h2>
      <div className="quetes-list">
        {done.map(uq => (
          <div key={uq.id} className="quete-item done">
            <span className="quete-icone">{uq.quete.icone}</span>
            <div className="quete-info">
              <strong>{uq.quete.titre}</strong>
              <p className="date">
                {new Date(uq.date_completion).toLocaleDateString('fr-FR')}
              </p>
            </div>
            <span className="points-badge earned">+{uq.quete.points} XP ✓</span>
          </div>
        ))}
      </div>
    </div>
  );
}
