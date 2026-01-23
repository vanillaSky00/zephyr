import React from 'react';

export default function DiaryList({ entries, onAdd }) {
  return (
    <div className="max-w-4xl mx-auto p-10">
      <div className="flex justify-between items-center mb-10 border-b-4 border-[#5d4037] pb-4">
        <h1 className="text-3xl font-bold uppercase">My Memories</h1>
        <button onClick={onAdd} className="bg-[#5d4037] text-white px-6 py-2 border-2 border-white">+ New Entry</button>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {entries.map(entry => (
          <div key={entry.id} className="bg-white border-4 border-[#5d4037] p-4 shadow-[6px_6px_0px_0px_#5d4037]">
            <div className="flex items-center gap-3 mb-2">
              <span className="text-2xl">{entry.moodData.icon}</span>
              <span className="font-bold text-lg">{entry.moodData.name}</span>
              <span className="ml-auto text-sm text-[#8d6e63]">{entry.date}</span>
            </div>
            <p className="line-clamp-3 text-[#5d4037]">{entry.content}</p>
            <div className="mt-3 pt-3 border-t border-dashed border-[#d7ccc8] text-xs italic text-[#8d6e63]">
              "{entry.moodData.quote}"
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}