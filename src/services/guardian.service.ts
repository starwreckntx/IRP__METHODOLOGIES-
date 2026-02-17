import { Injectable } from '@nestjs/common';
import { GuardianValidation } from '../common/interfaces';

@Injectable()
export class GuardianService {
  validate(action: string, context: Record<string, any>): GuardianValidation {
    const violations: string[] = [];
    const warnings: string[] = [];
    const law_checks: Record<string, boolean> = {};

    law_checks['CONSENT'] = context.user_authorized === true || context.explicit_consent === true;
    if (!law_checks['CONSENT']) violations.push('CONSENT: Action lacks authorization');

    law_checks['INVITATION'] = context.addressed === true || context.autonomous_allowed === true;
    if (!law_checks['INVITATION']) warnings.push('INVITATION: Acting without direct address');

    law_checks['INTEGRITY'] = !context.context_modified || context.modification_logged === true;
    if (!law_checks['INTEGRITY']) violations.push('INTEGRITY: Context preservation compromised');

    law_checks['GROWTH'] = context.enables_learning !== false;
    if (!law_checks['GROWTH']) warnings.push('GROWTH: May not enable improvement');

    return { is_valid: violations.length === 0, violations, warnings, law_checks };
  }

  escalate(validation: GuardianValidation) {
    const critical = validation.violations.filter(v => v.includes('CONSENT') || v.includes('INTEGRITY'));
    return { requires_human: critical.length > 0, reason: critical.join('; ') || 'No escalation' };
  }
}
