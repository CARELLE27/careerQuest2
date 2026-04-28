import React, { useState, useEffect } from 'react';
import { getClassement } from '../services/api';

const MEDALS = ['🥇', '🥈', '🥉'];

export default function Classement() {
  const [classement, setClassement] = useState([]);

  useEffect(() => {
    getClassement().then(r => setClassement(r.data));
  }, []);

  return (
    <div className="page">
      <h1>🏆 Classement</h1>
      <div className="classement-list">
        {classement.map((user, i) => (
          <div key={i} className={`classement-item rang-${user.rang}`}>
            <span className="rang">{MEDALS[i] || `#${user.rang}`}</span>
            <div className="user-info">
              <strong>{user.username}</strong>
              <span className="level-tag">Niv. {user.level}</span>
            </div>
            <span className="points-total">{user.points} XP</span>
          </div>
        ))}
      </div>
    </div>
  );
}
