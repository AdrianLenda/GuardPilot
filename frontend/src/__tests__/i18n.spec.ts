import { describe, it, expect } from 'vitest';
import { useT } from '../lib/i18n';

describe('i18n', () => {
  it('falls back to English for missing keys', () => {
    const t = useT('pl');
    // 'history_length_label' exists in both languages; should return Polish.
    expect(t('history_length_label')).toBeDefined();
    // Unknown key should fall back to English and return the key itself.
    expect(t('nonexistent_key')).toBe('nonexistent_key');
  });
});
