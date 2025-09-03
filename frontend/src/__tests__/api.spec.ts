import { describe, it, expect } from 'vitest';
import { postProxy, getHealth } from '../lib/api';

describe('api helpers', () => {
  it('exposes postProxy function', () => {
    expect(typeof postProxy).toBe('function');
  });
  it('exposes getHealth function', () => {
    expect(typeof getHealth).toBe('function');
  });
});
