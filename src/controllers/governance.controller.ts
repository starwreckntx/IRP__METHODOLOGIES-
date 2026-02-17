import { Controller, Post, Body } from '@nestjs/common';
import { ApiTags, ApiOperation } from '@nestjs/swagger';
import { GuardianService } from '../services/guardian.service';
import { MirrorRTCService } from '../services/mirror-rtc.service';
import { CRTPService } from '../services/crtp.service';

@ApiTags('Governance')
@Controller('governance')
export class GovernanceController {
  constructor(private guardian: GuardianService, private rtc: MirrorRTCService, private crtp: CRTPService) {}

  @Post('validate') @ApiOperation({ summary: 'Validate against Codex Laws' })
  async validate(@Body() dto: { action: string; context: Record<string, any> }) { return this.guardian.validate(dto.action, dto.context); }

  @Post('rtc/synthesize') @ApiOperation({ summary: 'RTC synthesis' })
  async rtcSynthesize(@Body() dto: { input: string; context?: Record<string, any> }) { return this.rtc.synthesize(dto.input, dto.context); }

  @Post('crtp/create') @ApiOperation({ summary: 'Create CRTP packet' })
  async createPacket(@Body() dto: { source_agent: string; packet_type: 'HANDSHAKE' | 'TASK' | 'RESULT' | 'GOVERNANCE' | 'HEARTBEAT'; content: any; target_agent?: string; session_id?: string }) {
    const packet = this.crtp.createPacket(dto.source_agent, dto.packet_type, dto.content, dto.target_agent, dto.session_id);
    return { packet, xml: this.crtp.toXML(packet) };
  }

  @Post('crtp/validate') async validatePacket(@Body() packet: any) { return { valid: this.crtp.validatePacket(packet) }; }
}
