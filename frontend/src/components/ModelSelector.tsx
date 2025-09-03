import React from 'react';

export interface ModelSelectorProps {
  model: string;
  onChange: (model: string) => void;
}

/**
 * Dropdown selector for choosing the LLM model. Accepts the current model
 * value and an onChange callback. Additional models can be added to the
 * options list as needed.
 */
export default function ModelSelector({ model, onChange }: ModelSelectorProps) {
  return (
    <select
      value={model}
      onChange={(e) => onChange(e.target.value)}
      className="bg-zinc-800 text-zinc-100 p-2 rounded"
      aria-label="Select model"
    >
      <option value="gpt-3.5-turbo">GPT-3.5 Turbo</option>
      <option value="gpt-4">GPT-4</option>
    </select>
  );
}
