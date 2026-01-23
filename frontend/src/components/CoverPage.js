import React from 'react';
export default function CoverPage({ onEnter }) {
  return (
    <div className="flex h-screen items-center justify-center bg-[#8d6e63]">
      <div className="border-8 border-[#5d4037] p-10 bg-[#6d4c41] shadow-[16px_16px_0px_0px_rgba(0,0,0,0.3)] text-center">
        <h1 className="text-4xl text-white font-bold mb-6">PIXEL DIARY</h1>
        <div className="text-8xl my-10 animate-bounce">📔</div>
        <button onClick={onEnter} className="bg-white text-[#5d4037] px-8 py-4 border-4 border-[#5d4037] hover:bg-[#efe5fd] font-bold text-2xl transition-all active:scale-95">
          [ OPEN BOOK ]
        </button>
      </div>
    </div>
  );
}