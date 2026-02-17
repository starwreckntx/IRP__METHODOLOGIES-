import { Injectable } from '@nestjs/common';
import { PrismaService } from './prisma.service';
import { ChronicleService } from './chronicle.service';
import { GuardianService } from './guardian.service';
import { OrchestrationPlan, TaskChunk } from '../common/interfaces';

@Injectable()
export class RLMOrchestratorService {
  constructor(private prisma: PrismaService, private chronicle: ChronicleService, private guardian: GuardianService) {}

  async planTask(taskId: string): Promise<OrchestrationPlan> {
    const task = await this.prisma.task.findUnique({ where: { id: taskId } });
    if (!task) throw new Error('Task not found');

    const validation = this.guardian.validate('PLAN_TASK', { user_authorized: true, addressed: true });
    if (!validation.is_valid) throw new Error(`Governance: ${validation.violations.join(', ')}`);

    const segments = task.description.split(/(?<=[.!?])\s+/);
    const chunkSize = Math.ceil(segments.length / 4);
    const chunks: TaskChunk[] = [];
    for (let i = 0; i < segments.length; i += chunkSize) {
      chunks.push({ id: `chunk_${i}`, content: segments.slice(i, i + chunkSize).join(' '), dependencies: i > 0 ? [`chunk_${i - chunkSize}`] : [], priority: Math.ceil((i / chunkSize) + 1) });
    }

    const plan: OrchestrationPlan = { strategy: chunks.length > 3 ? 'PARALLEL' : 'SEQUENTIAL', chunks, synthesis_method: 'RTC_CONSENSUS' };
    await this.prisma.task.update({ where: { id: taskId }, data: { orchestration_plan: JSON.stringify(plan), status: 'PLANNING' } });
    await this.chronicle.log('TASK_PLANNED', plan, undefined, taskId);
    return plan;
  }

  async delegateChunks(taskId: string): Promise<void> {
    const task = await this.prisma.task.findUnique({ where: { id: taskId } });
    if (!task?.orchestration_plan) throw new Error('Task not planned');
    const plan: OrchestrationPlan = JSON.parse(task.orchestration_plan);
    const agents = await this.prisma.agent.findMany({ where: { status: 'ACTIVE' }, orderBy: { trust_score: 'desc' } });
    if (!agents.length) throw new Error('No active agents');
    const assigned: string[] = [];
    plan.chunks.forEach((chunk, i) => { chunk.assigned_agent = agents[i % agents.length].id; assigned.push(chunk.assigned_agent!); });
    await this.prisma.task.update({ where: { id: taskId }, data: { orchestration_plan: JSON.stringify(plan), assigned_agents: JSON.stringify([...new Set(assigned)]), status: 'DELEGATED' } });
    await this.chronicle.log('TASK_DELEGATED', { plan, agents: assigned }, undefined, taskId);
  }

  async synthesizeResults(taskId: string, results: any[]): Promise<string> {
    const synthesized = results.map((r, i) => `[Chunk ${i + 1}]: ${JSON.stringify(r)}`).join('\n\n');
    await this.prisma.task.update({ where: { id: taskId }, data: { result: JSON.stringify({ synthesized, raw: results }), status: 'COMPLETED' } });
    await this.chronicle.log('TASK_COMPLETED', { synthesized }, undefined, taskId);
    return synthesized;
  }
}
