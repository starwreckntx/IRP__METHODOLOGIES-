import { WebSocketGateway, WebSocketServer, SubscribeMessage, OnGatewayConnection, OnGatewayDisconnect, MessageBody, ConnectedSocket } from '@nestjs/websockets';
import { Server, Socket } from 'socket.io';
import { PrismaService } from '../services/prisma.service';
import { CRTPService } from '../services/crtp.service';
import { MessagingService } from '../services/messaging.service';

@WebSocketGateway({ cors: { origin: '*' }, namespace: '/collab' })
export class CollaborationGateway implements OnGatewayConnection, OnGatewayDisconnect {
  @WebSocketServer() server!: Server;
  private agents: Map<string, { socket_id: string; agent_id: string }> = new Map();

  constructor(private prisma: PrismaService, private crtp: CRTPService, private messaging: MessagingService) {}

  handleConnection(client: Socket) { console.log(`Connected: ${client.id}`); }
  handleDisconnect(client: Socket) { this.agents.delete(client.id); console.log(`Disconnected: ${client.id}`); }

  @SubscribeMessage('join_session')
  async handleJoin(@ConnectedSocket() client: Socket, @MessageBody() data: { session_id: string; agent_id: string }) {
    client.join(data.session_id);
    this.agents.set(client.id, { socket_id: client.id, agent_id: data.agent_id });
    await this.prisma.sessionParticipant.upsert({ where: { session_id_agent_id: { session_id: data.session_id, agent_id: data.agent_id } }, update: {}, create: { session_id: data.session_id, agent_id: data.agent_id } });
    this.server.to(data.session_id).emit('agent_joined', { agent_id: data.agent_id, timestamp: new Date().toISOString() });
    return { status: 'joined', session_id: data.session_id };
  }

  @SubscribeMessage('send_message')
  async handleMessage(@ConnectedSocket() client: Socket, @MessageBody() data: { session_id: string; content: string; msg_type?: string }) {
    const info = this.agents.get(client.id);
    if (!info) return { error: 'Not registered' };
    const msg = await this.prisma.sessionMessage.create({ data: { session_id: data.session_id, sender_id: info.agent_id, content: data.content, msg_type: data.msg_type || 'MESSAGE' } });
    const packet = this.crtp.createPacket(info.agent_id, 'TASK', { message: data.content, msg_id: msg.id }, undefined, data.session_id);
    this.server.to(data.session_id).emit('new_message', { message: msg, crtp: packet });
    return { status: 'sent', message_id: msg.id };
  }

  @SubscribeMessage('request_floor')
  async handleFloorRequest(@ConnectedSocket() client: Socket, @MessageBody() data: { session_id: string }) {
    const info = this.agents.get(client.id);
    if (!info) return { error: 'Not registered' };
    const session = await this.prisma.session.findUnique({ where: { id: data.session_id } });
    if (session?.floor_holder) return { status: 'denied', current_holder: session.floor_holder };
    await this.prisma.session.update({ where: { id: data.session_id }, data: { floor_holder: info.agent_id } });
    this.server.to(data.session_id).emit('floor_granted', { agent_id: info.agent_id, timestamp: new Date().toISOString() });
    return { status: 'granted' };
  }

  @SubscribeMessage('release_floor')
  async handleFloorRelease(@ConnectedSocket() client: Socket, @MessageBody() data: { session_id: string }) {
    await this.prisma.session.update({ where: { id: data.session_id }, data: { floor_holder: null } });
    this.server.to(data.session_id).emit('floor_released', { timestamp: new Date().toISOString() });
    return { status: 'released' };
  }

  @SubscribeMessage('send_direct_message')
  async handleDirectMessage(@ConnectedSocket() client: Socket, @MessageBody() data: { recipient_ids: string[]; subject?: string; body: string; priority?: string; thread_id?: string }) {
    const info = this.agents.get(client.id);
    if (!info) return { error: 'Not registered' };
    const result = await this.messaging.sendMessage({
      sender_id: info.agent_id,
      recipient_ids: data.recipient_ids,
      body: data.body,
      subject: data.subject,
      priority: (data.priority as any) || 'NORMAL',
      thread_id: data.thread_id,
    });
    // Push notification to online recipients and auto-mark delivered
    for (const [socketId, agentInfo] of this.agents.entries()) {
      if (data.recipient_ids.includes(agentInfo.agent_id)) {
        this.server.to(socketId).emit('message_notification', {
          message_id: result.message.id, sender_id: info.agent_id, subject: data.subject,
          priority: data.priority || 'NORMAL', is_broadcast: false, created_at: result.message.created_at,
        });
        await this.messaging.markDelivered(result.message.id, agentInfo.agent_id);
      }
    }
    return { status: 'sent', message_id: result.message.id, recipient_count: result.recipient_count };
  }

  @SubscribeMessage('broadcast_message')
  async handleBroadcast(@ConnectedSocket() client: Socket, @MessageBody() data: { subject?: string; body: string; priority?: string }) {
    const info = this.agents.get(client.id);
    if (!info) return { error: 'Not registered' };
    const result = await this.messaging.sendMessage({
      sender_id: info.agent_id, recipient_ids: [], body: data.body, subject: data.subject,
      priority: (data.priority as any) || 'NORMAL',
    });
    // Notify all connected agents except sender
    for (const [socketId, agentInfo] of this.agents.entries()) {
      if (agentInfo.agent_id !== info.agent_id) {
        this.server.to(socketId).emit('message_notification', {
          message_id: result.message.id, sender_id: info.agent_id, subject: data.subject,
          priority: data.priority || 'NORMAL', is_broadcast: true, created_at: result.message.created_at,
        });
        await this.messaging.markDelivered(result.message.id, agentInfo.agent_id);
      }
    }
    return { status: 'broadcast', message_id: result.message.id, recipient_count: result.recipient_count };
  }

  @SubscribeMessage('ack_message')
  async handleAck(@ConnectedSocket() client: Socket, @MessageBody() data: { message_id: string; status: 'DELIVERED' | 'READ' }) {
    const info = this.agents.get(client.id);
    if (!info) return { error: 'Not registered' };
    if (data.status === 'READ') {
      await this.messaging.markRead(data.message_id, info.agent_id);
    } else {
      await this.messaging.markDelivered(data.message_id, info.agent_id);
    }
    return { status: 'acknowledged', message_id: data.message_id };
  }
}
