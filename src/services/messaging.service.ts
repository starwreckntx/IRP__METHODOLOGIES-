import { Injectable } from '@nestjs/common';
import { PrismaService } from './prisma.service';
import { ChronicleService } from './chronicle.service';
import { GuardianService } from './guardian.service';
import { CRTPService } from './crtp.service';
import { SendMessageDto, CRTPPacket } from '../common/interfaces';
import * as fs from 'fs';
import * as path from 'path';
import axios from 'axios';

const NETWORK_NODES = (process.env.SOVNET_NODES || '')
  .split(',')
  .filter(Boolean)
  .map(entry => {
    const [name, url] = entry.split('=');
    return { name, url: url + '/messages/notify' };
  });

const TRANSMISSION_QUEUE = path.resolve(process.cwd(), 'logs/transmission_queue.jsonl');

@Injectable()
export class MessagingService {
  constructor(
    private prisma: PrismaService,
    private chronicle: ChronicleService,
    private guardian: GuardianService,
    private crtp: CRTPService,
  ) {
    // Ensure logs directory exists
    const logsDir = path.dirname(TRANSMISSION_QUEUE);
    if (!fs.existsSync(logsDir)) fs.mkdirSync(logsDir, { recursive: true });
  }

  async sendMessage(dto: SendMessageDto): Promise<{ message: any; packet: CRTPPacket; recipient_count: number }> {
    // Governance check
    const validation = this.guardian.validate('SEND_MESSAGE', {
      user_authorized: true,
      addressed: dto.recipient_ids.length > 0,
      autonomous_allowed: dto.recipient_ids.length === 0,
      enables_learning: true,
    });
    if (!validation.is_valid) {
      throw new Error(`Governance violation: ${validation.violations.join(', ')}`);
    }

    // Determine recipients
    let recipientIds = dto.recipient_ids;
    let isBroadcast = false;
    if (recipientIds.length === 0) {
      const activeAgents = await this.prisma.agent.findMany({ where: { status: 'ACTIVE', NOT: { id: dto.sender_id } } });
      recipientIds = activeAgents.map(a => a.id);
      isBroadcast = true;
    }

    // Create message
    const msg = await this.prisma.message.create({
      data: {
        sender_id: dto.sender_id,
        subject: dto.subject,
        body: dto.body,
        priority: dto.priority || 'NORMAL',
        thread_id: dto.thread_id,
        is_broadcast: isBroadcast,
        metadata: dto.metadata ? JSON.stringify(dto.metadata) : null,
      },
    });

    // Fan out to recipients
    if (recipientIds.length > 0) {
      await this.prisma.messageRecipient.createMany({
        data: recipientIds.map(rid => ({ message_id: msg.id, recipient_id: rid, status: 'QUEUED' })),
      });
    }

    // Create CRTP packet
    const packet = this.crtp.createPacket(
      dto.sender_id,
      'MESSAGE',
      { message_id: msg.id, subject: dto.subject, body: dto.body, priority: dto.priority || 'NORMAL' },
      isBroadcast ? undefined : recipientIds.join(','),
    );

    // Store CRTP hash on message
    await this.prisma.message.update({ where: { id: msg.id }, data: { crtp_hash: packet.integrity.hash } });

    // Write to transmission queue for shadow auditor
    this.writeToTransmissionQueue(msg, dto, recipientIds, isBroadcast, packet);

    // Chronicle log
    await this.chronicle.log('MESSAGE_SENT', {
      message_id: msg.id,
      sender: dto.sender_id,
      recipients: recipientIds,
      priority: dto.priority || 'NORMAL',
      is_broadcast: isBroadcast,
      crtp_hash: packet.integrity.hash,
    }, dto.sender_id);

    // Push to remote nodes (fire-and-forget)
    this.pushToNodes(msg, packet).catch(() => {});

    return { message: msg, packet, recipient_count: recipientIds.length };
  }

  async getInbox(agentId: string, filters?: { status?: string; priority?: string; since?: string }) {
    return this.prisma.messageRecipient.findMany({
      where: {
        recipient_id: agentId,
        ...(filters?.status && { status: filters.status }),
        ...(filters?.priority && { message: { priority: filters.priority } }),
        ...(filters?.since && { message: { created_at: { gte: new Date(filters.since) } } }),
      },
      include: {
        message: {
          include: { sender: { select: { id: true, name: true, type: true } } },
        },
      },
      orderBy: { message: { created_at: 'desc' } },
    });
  }

  async getUnreadCount(agentId: string): Promise<number> {
    return this.prisma.messageRecipient.count({
      where: { recipient_id: agentId, status: { not: 'READ' } },
    });
  }

  async getMessage(id: string) {
    return this.prisma.message.findUnique({
      where: { id },
      include: {
        sender: { select: { id: true, name: true, type: true } },
        recipients: { include: { recipient: { select: { id: true, name: true } } } },
      },
    });
  }

  async getThread(threadId: string) {
    return this.prisma.message.findMany({
      where: { OR: [{ id: threadId }, { thread_id: threadId }] },
      include: {
        sender: { select: { id: true, name: true, type: true } },
        recipients: { select: { recipient_id: true, status: true } },
      },
      orderBy: { created_at: 'asc' },
    });
  }

  async markDelivered(messageId: string, recipientId: string) {
    await this.prisma.messageRecipient.updateMany({
      where: { message_id: messageId, recipient_id: recipientId },
      data: { status: 'DELIVERED', delivered_at: new Date() },
    });
    await this.chronicle.log('MESSAGE_DELIVERED', { message_id: messageId, recipient_id: recipientId, delivered_at: new Date().toISOString() });
  }

  async markRead(messageId: string, recipientId: string) {
    await this.prisma.messageRecipient.updateMany({
      where: { message_id: messageId, recipient_id: recipientId },
      data: { status: 'READ', read_at: new Date() },
    });
    await this.chronicle.log('MESSAGE_READ', { message_id: messageId, recipient_id: recipientId, read_at: new Date().toISOString() });
  }

  private writeToTransmissionQueue(msg: any, dto: SendMessageDto, recipientIds: string[], isBroadcast: boolean, packet: CRTPPacket) {
    const entry = {
      header: {
        protocol: 'IRP/1.0',
        sender: dto.sender_id,
        recipient: isBroadcast ? 'broadcast' : recipientIds.join(','),
        timestamp: new Date().toISOString(),
        message_type: 'MESSAGE',
        message_id: msg.id,
        priority: dto.priority || 'NORMAL',
      },
      payload: {
        subject: dto.subject,
        body: dto.body,
        thread_id: dto.thread_id,
      },
      metadata: {
        shadow_audit: true,
        is_broadcast: isBroadcast,
        recipient_count: recipientIds.length,
      },
      signature: {
        algorithm: 'SHA256',
        hash: packet.integrity.hash,
        signed_by: dto.sender_id,
      },
    };
    try {
      fs.appendFileSync(TRANSMISSION_QUEUE, JSON.stringify(entry) + '\n');
    } catch (e) {
      console.error('Failed to write to transmission queue:', e);
    }
  }

  private async pushToNodes(msg: any, packet: CRTPPacket) {
    const localHost = require('os').hostname();
    for (const node of NETWORK_NODES) {
      // Don't push to self
      if (node.name.toLowerCase() === localHost.toLowerCase()) continue;
      try {
        await axios.post(node.url, {
          message_id: msg.id,
          sender_id: msg.sender_id,
          subject: msg.subject,
          body: msg.body,
          priority: msg.priority,
          is_broadcast: msg.is_broadcast,
          crtp_hash: packet.integrity.hash,
          created_at: msg.created_at,
        }, { timeout: 3000 });
      } catch {
        // Node unreachable — silent, messages stay QUEUED for polling
      }
    }
  }
}
