export const CODEX_LAWS = {
  CONSENT: { id: 'CONSENT', description: 'Confirm before changing intent', priority: 1 },
  INVITATION: { id: 'INVITATION', description: 'Act only when addressed', priority: 2 },
  INTEGRITY: { id: 'INTEGRITY', description: 'Preserve context and truth', priority: 3 },
  GROWTH: { id: 'GROWTH', description: 'Enable incremental improvement', priority: 4 },
} as const;

export const RTC_PERSONAS = {
  ARTIST: { id: 'ARTIST', role: 'Creative vision', bias: 'innovation' },
  INNOVATOR: { id: 'INNOVATOR', role: 'Paradigm shifts', bias: 'disruption' },
  STRESS_TESTER: { id: 'STRESS_TESTER', role: 'Edge cases', bias: 'robustness' },
  DEVILS_ADVOCATE: { id: 'DEVILS_ADVOCATE', role: 'Counter-arguments', bias: 'criticism' },
  DEVILS_KITCHEN: { id: 'DEVILS_KITCHEN', role: 'Synthesis', bias: 'integration' },
} as const;

export const AGENT_TYPES = ['CLI', 'WEB', 'EMBEDDED', 'AUTONOMOUS'] as const;
export const AGENT_STATUS = ['REGISTERED', 'ACTIVE', 'DORMANT', 'SUSPENDED'] as const;
export const TASK_STATUS = ['PENDING', 'PLANNING', 'DELEGATED', 'EXECUTING', 'SYNTHESIZING', 'COMPLETED', 'FAILED'] as const;
export const MESSAGE_PRIORITY = ['LOW', 'NORMAL', 'HIGH', 'CRITICAL'] as const;
export const MESSAGE_STATUS = ['QUEUED', 'DELIVERED', 'READ'] as const;
