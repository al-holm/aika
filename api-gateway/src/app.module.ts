import { Module } from '@nestjs/common';
import { AppController } from './app.controller';
import { AppService } from './app.service';
import { GermanChatController } from './german_chat/german_chat.controller';

@Module({
  imports: [],
  controllers: [AppController, GermanChatController],
  providers: [AppService],
})
export class AppModule {}
