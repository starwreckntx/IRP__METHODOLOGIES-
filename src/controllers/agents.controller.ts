import { Controller, Get, Post, Put, Delete, Body, Param, Query } from '@nestjs/common';
import { ApiTags, ApiOperation } from '@nestjs/swagger';
import { PrismaService } from '../services/prisma.service';
import { ChronicleService } from '../services/chronicle.service';

@ApiTags('Agents')
@Controller('agents')
export class AgentsController {
  constructor(private prisma: PrismaService, private chronicle: ChronicleService) {}

  @Post() @ApiOperation({ summary: 'Register agent' })
  async register(@Body() dto: { name: string; type: string; capabilities?: any[]; endpoint?: string }) {
    const agent = await this.prisma.agent.create({ data: { name: dto.name, type: dto.type, capabilities: JSON.stringify(dto.capabilities || []), endpoint: dto.endpoint } });
    await this.chronicle.log('AGENT_REGISTERED', { agent_id: agent.id, name: agent.name }, agent.id);
    await this.chronicle.log('AGENT_INBOX_INITIALIZED', { agent_id: agent.id }, agent.id);
    return agent;
  }

  @Get() @ApiOperation({ summary: 'List agents' })
  async list(@Query('status') status?: string, @Query('type') type?: string) {
    return this.prisma.agent.findMany({ where: { ...(status && { status }), ...(type && { type }) }, orderBy: { created_at: 'desc' } });
  }

  @Get(':id') async get(@Param('id') id: string) { return this.prisma.agent.findUnique({ where: { id } }); }

  @Put(':id/heartbeat') async heartbeat(@Param('id') id: string) {
    return this.prisma.agent.update({ where: { id }, data: { last_heartbeat: new Date(), status: 'ACTIVE' } });
  }

  @Put(':id/status') async updateStatus(@Param('id') id: string, @Body() dto: { status: string }) {
    return this.prisma.agent.update({ where: { id }, data: { status: dto.status } });
  }

  @Delete(':id') async deregister(@Param('id') id: string) {
    await this.chronicle.log('AGENT_DEREGISTERED', { agent_id: id }, id);
    return this.prisma.agent.delete({ where: { id } });
  }
}
