import { Injectable } from '@nestjs/common';
import { PrismaService } from './prisma.service';
import * as crypto from 'crypto';

@Injectable()
export class ChronicleService {
  constructor(private prisma: PrismaService) {}

  async log(entry_type: string, content: any, agent_id?: string, task_id?: string) {
    const lastEntry = await this.prisma.chronicle.findFirst({ orderBy: { created_at: 'desc' } });
    const contentStr = JSON.stringify(content);
    const hash = crypto.createHash('sha256').update(contentStr + (lastEntry?.hash || 'GENESIS')).digest('hex');
    return this.prisma.chronicle.create({
      data: { entry_type, content: contentStr, hash, previous_hash: lastEntry?.hash || null, agent_id, task_id }
    });
  }

  async verify(id: string): Promise<boolean> {
    const entry = await this.prisma.chronicle.findUnique({ where: { id } });
    if (!entry) return false;
    const expectedHash = crypto.createHash('sha256').update(entry.content + (entry.previous_hash || 'GENESIS')).digest('hex');
    return entry.hash === expectedHash;
  }
}
