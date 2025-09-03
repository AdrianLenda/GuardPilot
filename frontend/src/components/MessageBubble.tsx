import React from 'react';
import type { Role } from '../lib/types';

export interface MessageBubbleProps {
  role: Role;
  content: string;
  timestamp?: number;
}

/**
 * A single chat message bubble. Aligns left or right based on role and
 * displays a timestamp when provided. Future work: render markdown,
 * highlight code blocks, and provide copy buttons.
 */
export default function MessageBubble({ role, content, timestamp }: MessageBubbleProps) {
  const isUser = role === 'user';
  const align = isUser ? 'justify-end' : 'justify-start';
  const bubbleClasses = isUser
    ? 'bg-gradient-to-r from-indigo-500 to-sky-500 text-white'
    : 'bg-zinc-800 text-zinc-100';
  return (
    <div className={`flex ${align}`}>
      <div className={`${bubbleClasses} px-4 py-3 rounded-2xl shadow-lg max-w-68ch`}> 
        <div>{content}</div>
        {timestamp && (
          <div className="text-xs text-zinc-400 mt-1 text-right">
            {new Date(timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
          </div>
        )}
      </div>
    </div>
  );
}
