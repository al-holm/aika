import { Controller, Post, Body } from '@nestjs/common';
import { GermanChatMessageDto } from 'src/german_chat/dto/german-chat-question.dto';
import { GermanChatService } from './german_chat.service';

@Controller('german-chat')
export class GermanChatController {
  constructor(private readonly germanChatService: GermanChatService) {}

  @Post('message') // changed to post, cause get requests typically don't include a body
  async getAnswer(
    @Body() messageDTO: GermanChatMessageDto,
  ): Promise<{ message: GermanChatMessageDto }> {
    const message = await this.germanChatService.processMessage(messageDTO);
    return { message };
  }
}
