import React from 'react';

export interface ErrorBannerProps {
  message: string;
  onClose?: () => void;
}

/**
 * Displays a dismissable error banner at the top of the chat window. Used to
 * surface API errors to the user. Automatically disappears after a timeout
 * if no onClose is provided.
 */
export default function ErrorBanner({ message, onClose }: ErrorBannerProps) {
  return (
    <div className="bg-red-700 text-white p-3 rounded-md flex items-center justify-between mb-2">
      <span>{message}</span>
      {onClose && (
        <button
          type="button"
          className="ml-4 text-white hover:text-red-300"
          onClick={onClose}
          aria-label="Dismiss error"
        >
          ✕
        </button>
      )}
    </div>
  );
}
