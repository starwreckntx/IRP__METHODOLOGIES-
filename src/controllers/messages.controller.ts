import { Controller, Get, Post, Put, Body, Param, Query } from '@nestjs/common';
import { ApiTags, ApiOperation } from '@nestjs/swagger';
import { MessagingService } from '../services/messaging.service';

@ApiTags('Messages')
@Controller('messages')
export class MessagesController {
  constructor(private messaging: MessagingService) {}

  @Post()
  @ApiOperation({ summary: 'Send a message (direct or broadcast)' })
  async send(@Body() dto: {
    sender_id: string;
    recipient_ids?: string[];
    subject?: string;
    body: string;
    priority?: 'LOW' | 'NORMAL' | 'HIGH' | 'CRITICAL';
    thread_id?: string;
    metadata?: any;
  }) {
    return this.messaging.sendMessage({
      sender_id: dto.sender_id,
      recipient_ids: dto.recipient_ids || [],
      subject: dto.subject,
      body: dto.body,
      priority: dto.priority || 'NORMAL',
      thread_id: dto.thread_id,
      metadata: dto.metadata,
    });
  }

  @Get('inbox/:agentId')
  @ApiOperation({ summary: 'Get agent inbox' })
  async inbox(
    @Param('agentId') agentId: string,
    @Query('status') status?: string,
    @Query('priority') priority?: string,
    @Query('since') since?: string,
  ) {
    return this.messaging.getInbox(agentId, { status, priority, since });
  }

  @Get('inbox/:agentId/count')
  @ApiOperation({ summary: 'Get unread message count' })
  async unreadCount(@Param('agentId') agentId: string) {
    const count = await this.messaging.getUnreadCount(agentId);
    return { agent_id: agentId, unread_count: count };
  }

  @Get('thread/:threadId')
  @ApiOperation({ summary: 'Get message thread' })
  async thread(@Param('threadId') threadId: string) {
    return this.messaging.getThread(threadId);
  }

  @Get(':id')
  @ApiOperation({ summary: 'Get message by ID' })
  async get(@Param('id') id: string) {
    return this.messaging.getMessage(id);
  }

  @Put(':id/delivered/:agentId')
  @ApiOperation({ summary: 'Mark message as delivered' })
  async markDelivered(@Param('id') id: string, @Param('agentId') agentId: string) {
    await this.messaging.markDelivered(id, agentId);
    return { status: 'delivered' };
  }

  @Put(':id/read/:agentId')
  @ApiOperation({ summary: 'Mark message as read' })
  async markRead(@Param('id') id: string, @Param('agentId') agentId: string) {
    await this.messaging.markRead(id, agentId);
    return { status: 'read' };
  }

  @Post('notify')
  @ApiOperation({ summary: 'Receive push notification from remote node' })
  async notify(@Body() data: {
    message_id: string;
    sender_id: string;
    subject?: string;
    body: string;
    priority: string;
    is_broadcast: boolean;
    crtp_hash: string;
    created_at: string;
  }) {
    // Log the inbound push for chronicle
    return { status: 'received', message_id: data.message_id, node: require('os').hostname() };
  }
}
