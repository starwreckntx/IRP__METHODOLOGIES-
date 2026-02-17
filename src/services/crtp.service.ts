import { Injectable } from '@nestjs/common';
import { CRTPPacket, CRTPHeader, CRTPPayload, CRTPIntegrity } from '../common/interfaces';
import * as crypto from 'crypto';

@Injectable()
export class CRTPService {
  createPacket(source_agent: string, packet_type: CRTPHeader['packet_type'], content: any, target_agent?: string, session_id?: string, previous_hash?: string): CRTPPacket {
    const header: CRTPHeader = { version: '1.0', timestamp: new Date().toISOString(), source_agent, target_agent, packet_type, session_id };
    const payload: CRTPPayload = { content, context: {}, governance_flags: [] };
    const hash = crypto.createHash('sha256').update(JSON.stringify({ header, payload }) + (previous_hash || '')).digest('hex');
    const integrity: CRTPIntegrity = { hash, previous_hash };
    return { header, payload, integrity };
  }

  validatePacket(packet: CRTPPacket): boolean {
    const expected = crypto.createHash('sha256').update(JSON.stringify({ header: packet.header, payload: packet.payload }) + (packet.integrity.previous_hash || '')).digest('hex');
    return packet.integrity.hash === expected;
  }

  toXML(packet: CRTPPacket): string {
    return `<?xml version="1.0"?><crtp_packet version="${packet.header.version}"><header><timestamp>${packet.header.timestamp}</timestamp><source>${packet.header.source_agent}</source><type>${packet.header.packet_type}</type></header><payload><![CDATA[${JSON.stringify(packet.payload.content)}]]></payload><integrity><hash>${packet.integrity.hash}</hash></integrity></crtp_packet>`;
  }
}
