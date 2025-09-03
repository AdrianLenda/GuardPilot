import React, { useState } from 'react';

export interface MessageInputProps {
  onSend: (text: string) => void;
}

/**
 * Chat input component. Handles multiline text entry with Shift+Enter and
 * submits on Enter. Disables send button when input is empty.
 */
export default function MessageInput({ onSend }: MessageInputProps) {
  const [value, setValue] = useState('');
  const handleSend = () => {
    const text = value.trim();
    if (text.length === 0) return;
    onSend(text);
    setValue('');
  };
  return (
    <div className="p-4 bg-zinc-900 border-t border-zinc-800 flex gap-2">
      <textarea
        className="flex-1 resize-none rounded-lg p-3 bg-zinc-800 text-zinc-100 focus:outline-none focus:ring-2 focus:ring-indigo-500"
        rows={1}
        value={value}
        onChange={(e) => setValue(e.target.value)}
        onKeyDown={(e) => {
          if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSend();
          }
        }}
        placeholder="Type your message..."
      />
      <button
        type="button"
        className="disabled:opacity-50 bg-indigo-500 hover:bg-indigo-600 text-white p-3 rounded-full flex items-center justify-center"
        onClick={handleSend}
        disabled={value.trim().length === 0}
        aria-label="Send message"
      >
        {/* Simple SVG arrow icon for send */}
        <svg
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 24 24"
          fill="currentColor"
          className="h-5 w-5"
        >
          <path d="M3 12l18-9v18l-18-9z" />
        </svg>
      </button>
    </div>
  );
}
