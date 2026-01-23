import React, { useState } from 'react';

export default function DiaryEntry({ onSave, onCancel }) {
  const [text, setText] = useState('');

  return (
    <div className="flex items-center justify-center min-h-screen p-4">
      <div className="bg-[#fdf6e3] border-4 border-[#5d4037] p-8 w-full max-w-4xl flex gap-8 shadow-[12px_12px_0px_0px_#5d4037]">
        {/* 左頁：寫作區 */}
        <div className="flex-1 flex flex-col border-r-2 border-[#5d4037] pr-8 border-dashed">
          <h2 className="text-2xl font-bold underline mb-4">Dear Diary,</h2>
          <textarea 
            className="flex-1 bg-transparent border-none focus:ring-0 text-2xl leading-relaxed resize-none h-96"
            placeholder="Write your story here..."
            value={text}
            onChange={(e) => setText(e.target.value)}
          />
        </div>
        {/* 右頁：功能區 */}
        <div className="w-1/3 flex flex-col justify-between italic text-center">
          <div className="text-xl">"A cup of coffee shared with a diary is time well spent."</div>
          <div className="flex flex-col gap-4">
            <button onClick={() => onSave(text)} className="bg-[#5d4037] text-white py-3 border-4 border-white hover:invert">
              SAVE & ANALYZE
            </button>
            <button onClick={onCancel} className="text-[#8d6e63] underline">Cancel</button>
          </div>
        </div>
      </div>
    </div>
  );
}