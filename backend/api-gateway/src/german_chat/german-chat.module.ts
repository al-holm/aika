import { Module } from '@nestjs/common';
import { GermanChatController } from './german_chat.controller';
import { GermanChatService } from './german_chat.service';

@Module({
  controllers: [GermanChatController],
  providers: [GermanChatService],
})
export class GermanChatModule {}
