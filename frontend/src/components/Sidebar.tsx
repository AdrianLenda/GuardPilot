import React from 'react';

/**
 * Sidebar component for chat controls and settings. Currently minimal; would
 * include new/clear chat buttons and configuration controls. Visible on
 * medium+ screens; hidden on small screens via Tailwind CSS.
 */
export default function Sidebar() {
  return (
    <aside className="hidden md:block md:w-64 bg-zinc-800 border-r border-zinc-700 p-4 overflow-y-auto">
      <div className="flex flex-col gap-2">
        <button className="w-full py-2 px-3 rounded bg-zinc-700 text-zinc-100 hover:bg-zinc-600">
          New Chat
        </button>
        <button className="w-full py-2 px-3 rounded bg-zinc-700 text-zinc-100 hover:bg-zinc-600">
          Clear Chat
        </button>
        <div className="pt-4">
          <h2 className="text-sm uppercase font-semibold text-zinc-400 mb-2">Settings</h2>
          <div className="flex flex-col gap-3">
            <label className="flex flex-col text-sm text-zinc-300">
              Max Tokens
              <input type="number" min={1} max={4096} defaultValue={1024} className="mt-1 p-1 rounded bg-zinc-700 text-zinc-100" />
            </label>
            <label className="flex flex-col text-sm text-zinc-300">
              History Length
              <input type="number" min={1} max={50} defaultValue={10} className="mt-1 p-1 rounded bg-zinc-700 text-zinc-100" />
            </label>
          </div>
        </div>
      </div>
    </aside>
  );
}
