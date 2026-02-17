import { NestFactory } from '@nestjs/core';
import { NestExpressApplication } from '@nestjs/platform-express';
import { SwaggerModule, DocumentBuilder } from '@nestjs/swagger';
import { AppModule } from './app.module';
import { join } from 'path';

async function bootstrap() {
  const app = await NestFactory.create<NestExpressApplication>(AppModule);
  app.enableCors({ origin: '*', methods: 'GET,HEAD,PUT,PATCH,POST,DELETE', credentials: true });
  app.useStaticAssets(join(__dirname, '..', 'public'));

  const config = new DocumentBuilder()
    .setTitle('Sovereign AI Collaboration Hub')
    .setDescription('RLM Orchestrator | IRP Governance | Multi-Agent Collaboration')
    .setVersion('1.0')
    .addTag('Agents').addTag('Tasks').addTag('Governance').addTag('Messages')
    .build();
  SwaggerModule.setup('api-docs', app, SwaggerModule.createDocument(app, config));

  const port = process.env.PORT || 3000;
  await app.listen(port);
  console.log(`
╔═══════════════════════════════════════════════════════════╗
║     SOVEREIGN AI COLLABORATION HUB                        ║
║     Local Instance Running                                ║
╠═══════════════════════════════════════════════════════════╣
║  API Docs:    http://localhost:${port}/api-docs               ║
║  WebSocket:   ws://localhost:${port}/collab                   ║
║  Health:      http://localhost:${port}/agents                 ║
╠═══════════════════════════════════════════════════════════╣
║  Codex Law:   CONSENT | INVITATION | INTEGRITY | GROWTH   ║
║  Chronicle:   SHA-256 verified ledger active              ║
║  RTC:         5 personas ready                            ║
╚═══════════════════════════════════════════════════════════╝
  `);
}
bootstrap();
