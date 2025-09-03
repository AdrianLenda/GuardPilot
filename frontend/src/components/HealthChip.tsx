import React from 'react';
import { useHealth } from '../lib/useHealth';

/**
 * HealthChip component. Displays backend online/offline status and updates
 * periodically via the useHealth hook. Styles the badge accordingly.
 */
export default function HealthChip() {
  const online = useHealth();
  const color = online ? 'bg-green-600' : 'bg-red-600';
  const label = online ? 'Online' : 'Offline';
  return (
    <span className={`px-2 py-1 text-xs rounded-full ${color}`}>{label}</span>
  );
}
