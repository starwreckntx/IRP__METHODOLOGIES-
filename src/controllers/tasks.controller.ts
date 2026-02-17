import { Controller, Get, Post, Body, Param } from '@nestjs/common';
import { ApiTags, ApiOperation } from '@nestjs/swagger';
import { PrismaService } from '../services/prisma.service';
import { RLMOrchestratorService } from '../services/rlm-orchestrator.service';

@ApiTags('Tasks')
@Controller('tasks')
export class TasksController {
  constructor(private prisma: PrismaService, private rlm: RLMOrchestratorService) {}

  @Post() @ApiOperation({ summary: 'Create task' })
  async create(@Body() dto: { title: string; description: string; creator_id: string; priority?: number; context?: any; requirements?: any; governance_config?: any }) {
    return this.prisma.task.create({ data: { title: dto.title, description: dto.description, creator_id: dto.creator_id, priority: dto.priority || 5, context: dto.context ? JSON.stringify(dto.context) : null, requirements: dto.requirements ? JSON.stringify(dto.requirements) : null, governance_config: dto.governance_config ? JSON.stringify(dto.governance_config) : null } });
  }

  @Get() async list() { return this.prisma.task.findMany({ include: { creator: true }, orderBy: { created_at: 'desc' } }); }
  @Get(':id') async get(@Param('id') id: string) { return this.prisma.task.findUnique({ where: { id }, include: { creator: true, chronicles: true } }); }
  @Post(':id/plan') async plan(@Param('id') id: string) { return this.rlm.planTask(id); }
  @Post(':id/delegate') async delegate(@Param('id') id: string) { await this.rlm.delegateChunks(id); return { status: 'delegated', task_id: id }; }
  @Post(':id/synthesize') async synthesize(@Param('id') id: string, @Body() dto: { results: any[] }) { return this.rlm.synthesizeResults(id, dto.results); }
}
