import React, { useState } from 'react';
import MessageBubble from './MessageBubble';
import MessageInput from './MessageInput';
import type { Message } from '../lib/types';

/**
 * Main chat window component. Maintains local message state and renders
 * incoming and outgoing messages. In a complete implementation, this
 * component would interact with the backend via API helpers.
 */
export default function ChatWindow() {
  const [messages, setMessages] = useState<Message[]>([]);

  const appendMessage = (role: 'user' | 'assistant', content: string) => {
    setMessages((prev) => [...prev, { role, content, timestamp: Date.now() }]);
  };

  const handleSend = (text: string) => {
    // Append the user's message immediately
    appendMessage('user', text);
    // Simulate assistant reply placeholder; in real app call the proxy API
    appendMessage('assistant', '...');
  };

  return (
    <section
      className="flex flex-col flex-1 overflow-hidden"
      aria-label="Conversation"
      role="log"
      aria-live="polite"
    >
      {/* Message list */}
      <div className="flex-1 overflow-y-auto p-4 space-y-2">
        {messages.map((msg, idx) => (
          <MessageBubble
            key={idx}
            role={msg.role}
            content={msg.content}
            timestamp={msg.timestamp}
          />
        ))}
      </div>
      {/* Input */}
      <MessageInput onSend={handleSend} />
    </section>
  );
}
