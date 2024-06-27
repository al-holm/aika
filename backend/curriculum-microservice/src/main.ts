import { NestFactory } from '@nestjs/core';
import { AppModule } from './app.module';
import { SwaggerModule, DocumentBuilder } from '@nestjs/swagger';
async function bootstrap() {
  const app = await NestFactory.create(AppModule);
  const options = new DocumentBuilder()
    .setTitle('CurriculumAPI')
    .setDescription('Nest JS')
    .setVersion('1.0')
    .addServer('http://localhost:3543/', 'Local environment')
    .addTag('CurriculumAPI')
    .build();
  const document = SwaggerModule.createDocument(app, options);
  SwaggerModule.setup('api-docs', app, document);
  await app.listen(process.env.PORT || 3543);
}
bootstrap();
