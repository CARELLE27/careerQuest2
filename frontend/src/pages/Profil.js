import React, { useState, useEffect } from 'react';
import { getProfil, updateProfil, getMesCompetences, getCompetences, ajouterCompetence, connectGithub } from '../services/api';

export default function Profil() {
  const [user, setUser] = useState(null);
  const [competences, setCompetences] = useState([]);
  const [mesCompetences, setMesCompetences] = useState([]);
  const [githubUsername, setGithubUsername] = useState('');
  const [githubRepos, setGithubRepos] = useState([]);
  const [message, setMessage] = useState('');

  useEffect(() => {
    getProfil().then(r => { setUser(r.data); setGithubUsername(r.data.github_username || ''); });
    getCompetences().then(r => setCompetences(r.data));
    getMesCompetences().then(r => setMesCompetences(r.data));
  }, []);

  const handleAjouterComp = async (id) => {
    try {
      await ajouterCompetence(id);
      getMesCompetences().then(r => setMesCompetences(r.data));
      getProfil().then(r => setUser(r.data));
      setMessage('+20 XP ! Compétence ajoutée 🎉');
      setTimeout(() => setMessage(''), 2000);
    } catch {}
  };

  const handleGithub = async (e) => {
    e.preventDefault();
    try {
      const res = await connectGithub(githubUsername);
      setGithubRepos(res.data.repos);
      setMessage(res.data.message);
      getProfil().then(r => setUser(r.data));
      setTimeout(() => setMessage(''), 3000);
    } catch {
      setMessage('Impossible de charger GitHub');
    }
  };

  if (!user) return <div className="loading">Chargement...</div>;

  const mesCompIds = mesCompetences.map(mc => mc.competence.id);

  return (
    <div className="page">
      <h1>👤 Mon Profil</h1>
      {message && <div className="toast">{message}</div>}

      <div className="profil-header">
        <div className="profil-info">
          <h2>{user.username}</h2>
          <p>Niveau {user.level} • {user.points} XP</p>
        </div>
      </div>

      {/* Compétences */}
      <section className="section">
        <h2>🧠 Mes Compétences</h2>
        <div className="competences-grid">
          {competences.map(c => (
            <div
              key={c.id}
              className={`comp-badge ${mesCompIds.includes(c.id) ? 'owned' : ''}`}
              onClick={() => !mesCompIds.includes(c.id) && handleAjouterComp(c.id)}
            >
              {c.nom}
              {mesCompIds.includes(c.id) ? ' ✓' : ' +'}
            </div>
          ))}
        </div>
      </section>

      {/* GitHub */}
      <section className="section">
        <h2>🐙 Connecter GitHub</h2>
        <form onSubmit={handleGithub} className="github-form">
          <input
            type="text"
            placeholder="Votre pseudo GitHub"
            value={githubUsername}
            onChange={(e) => setGithubUsername(e.target.value)}
          />
          <button type="submit" className="btn-primary">Connecter</button>
        </form>
        {githubRepos.length > 0 && (
          <div className="repos-list">
            {githubRepos.map((repo, i) => (
              <div key={i} className="repo-item">
                <span>📁 {repo.name}</span>
                <span>⭐ {repo.stargazers_count}</span>
              </div>
            ))}
          </div>
        )}
      </section>
    </div>
  );
}
