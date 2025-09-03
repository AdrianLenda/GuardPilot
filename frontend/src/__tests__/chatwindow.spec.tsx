import { render, fireEvent, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import ChatWindow from '../components/ChatWindow';

describe('ChatWindow', () => {
  it('renders input and appends messages on send', () => {
    render(<ChatWindow />);
    const textarea = screen.getByPlaceholderText(/Type your message/i);
    fireEvent.change(textarea, { target: { value: 'hello' } });
    fireEvent.keyDown(textarea, { key: 'Enter', code: 'Enter' });
    // After sending, expect at least one occurrence of the text.
    expect(screen.getAllByText(/hello/).length).toBeGreaterThan(0);
  });
});
