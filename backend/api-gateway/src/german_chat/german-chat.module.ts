import { Module } from '@nestjs/common';
import { GermanChatController } from './german_chat.controller';

@Module({
    controllers: [GermanChatController]
})
export class GermanChatModule {}
