import React, { useState, useEffect } from 'react';
import CoverPage from './components/CoverPage';
import DiaryList from './components/DiaryList';
import DiaryEntry from './components/DiaryEntry';
import { analyzeMoodAgent } from './services/moodAgent';

export default function App() {
  const [view, setView] = useState('cover');
  const [entries, setEntries] = useState([]);

  useEffect(() => {
    const saved = localStorage.getItem('pixel_coffee_v2');
    if (saved) setEntries(JSON.parse(saved));
  }, []);

  const handleSaveDiary = (content) => {
    const analysis = analyzeMoodAgent(content);
    const newEntry = {
      id: Date.now(),
      date: new Date().toLocaleDateString(),
      content: content,
      moodData: analysis
    };
    const updated = [newEntry, ...entries];
    setEntries(updated);
    localStorage.setItem('pixel_coffee_v2', JSON.stringify(updated));
    setView('list');
  };

  return (
    <div className="min-h-screen bg-[#d7ccc8] text-[#5d4037]">
      {view === 'cover' && <CoverPage onEnter={() => setView('list')} />}
      {view === 'list' && <DiaryList entries={entries} onAdd={() => setView('write')} />}
      {view === 'write' && <DiaryEntry onSave={handleSaveDiary} onCancel={() => setView('list')} />}
    </div>
  );
}