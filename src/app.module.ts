import { Module } from '@nestjs/common';
import { PrismaService } from './services/prisma.service';
import { ChronicleService } from './services/chronicle.service';
import { GuardianService } from './services/guardian.service';
import { MirrorRTCService } from './services/mirror-rtc.service';
import { CRTPService } from './services/crtp.service';
import { RLMOrchestratorService } from './services/rlm-orchestrator.service';
import { MessagingService } from './services/messaging.service';
import { AgentsController } from './controllers/agents.controller';
import { TasksController } from './controllers/tasks.controller';
import { GovernanceController } from './controllers/governance.controller';
import { MessagesController } from './controllers/messages.controller';
import { CollaborationGateway } from './gateways/collaboration.gateway';

@Module({
  controllers: [AgentsController, TasksController, GovernanceController, MessagesController],
  providers: [PrismaService, ChronicleService, GuardianService, MirrorRTCService, CRTPService, RLMOrchestratorService, MessagingService, CollaborationGateway],
})
export class AppModule {}
