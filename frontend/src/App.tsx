import React from 'react';
import Header from './components/Header';
import ChatWindow from './components/ChatWindow';
import Sidebar from './components/Sidebar';

/**
 * Top-level application component. Composes the sidebar, header and chat window
 * into a full-page chat interface. Styling is provided via Tailwind CSS.
 */
export default function App() {
  return (
    <div className="flex h-screen text-zinc-100 bg-zinc-900">
      {/* Sidebar is hidden on small screens; see Sidebar component for details */}
      <Sidebar />
      <div className="flex flex-col flex-1">
        <Header />
        <ChatWindow />
      </div>
    </div>
  );
}
