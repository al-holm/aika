import { Module } from '@nestjs/common';
import { AppController } from './app.controller';
import { AppService } from './app.service';
import { GermanChatModule } from './german_chat/german-chat.module';

@Module({
  imports: [GermanChatModule],
  controllers: [AppController],
  providers: [AppService],
})
export class AppModule {}
