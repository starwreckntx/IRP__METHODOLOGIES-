export interface CRTPHeader {
  version: string;
  timestamp: string;
  source_agent: string;
  target_agent?: string;
  packet_type: 'HANDSHAKE' | 'TASK' | 'RESULT' | 'GOVERNANCE' | 'HEARTBEAT' | 'MESSAGE';
  session_id?: string;
}

export interface CRTPPayload {
  content: any;
  context?: Record<string, any>;
  governance_flags?: string[];
}

export interface CRTPIntegrity {
  hash: string;
  signature?: string;
  previous_hash?: string;
}

export interface CRTPPacket {
  header: CRTPHeader;
  payload: CRTPPayload;
  integrity: CRTPIntegrity;
}

export interface GuardianValidation {
  is_valid: boolean;
  violations: string[];
  warnings: string[];
  law_checks: Record<string, boolean>;
}

export interface RTCSynthesis {
  consensus: string;
  perspectives: Record<string, string>;
  dissent: string[];
  confidence: number;
}

export interface OrchestrationPlan {
  strategy: 'PARALLEL' | 'SEQUENTIAL' | 'HYBRID';
  chunks: TaskChunk[];
  synthesis_method: string;
}

export interface TaskChunk {
  id: string;
  content: string;
  assigned_agent?: string;
  dependencies: string[];
  priority: number;
}

export interface SendMessageDto {
  sender_id: string;
  recipient_ids: string[];
  subject?: string;
  body: string;
  priority?: 'LOW' | 'NORMAL' | 'HIGH' | 'CRITICAL';
  thread_id?: string;
  metadata?: Record<string, any>;
}

export interface MessageDeliveryEvent {
  message_id: string;
  sender_id: string;
  sender_name?: string;
  subject?: string;
  body: string;
  priority: string;
  thread_id?: string;
  is_broadcast: boolean;
  created_at: string;
}
