import React from 'react';
import { useHealth } from '../lib/useHealth';
import ModelSelector from './ModelSelector';

/**
 * Header component displaying the app title, model selector, language toggle
 * (placeholder), and health status chip.
 */
export default function Header() {
  const online = useHealth();
  // Placeholder model and language state; would be lifted up in a real app.
  const [model, setModel] = React.useState('gpt-3.5-turbo');
  const [lang, setLang] = React.useState('en');
  return (
    <header className="flex items-center justify-between p-4 bg-zinc-900 border-b border-zinc-800">
      <div className="flex items-center gap-4">
        <h1 className="text-xl font-semibold">GuardPilot</h1>
        {/* Health chip */}
        <span
          className={`px-2 py-1 text-xs rounded-full ${
            online ? 'bg-green-600' : 'bg-red-600'
          }`}
        >
          {online ? 'Online' : 'Offline'}
        </span>
      </div>
      <div className="flex items-center gap-4">
        <ModelSelector model={model} onChange={setModel} />
        <select
          value={lang}
          onChange={(e) => setLang(e.target.value)}
          className="bg-zinc-800 text-zinc-100 p-2 rounded"
        >
          <option value="en">EN</option>
          <option value="pl">PL</option>
        </select>
      </div>
    </header>
  );
}
