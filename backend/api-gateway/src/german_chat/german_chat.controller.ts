import { Controller, Post, Body } from '@nestjs/common';
import { GermanChatService } from './german_chat.service';
import { Message } from './models/message.dto';
import { ApiTags, ApiResponse, ApiExtraModels, getSchemaPath } from '@nestjs/swagger';

/**
 * Controller class for handling POST requests for processing messages in a
German chat application.
 * @class GermanChatController
 */
@ApiTags('API-Gateway')
@Controller('german-chat')
export class GermanChatController {
  constructor(private readonly germanChatService: GermanChatService) {}

  @ApiExtraModels(Message)
  @ApiResponse({
     status: 201,
     schema: {
       $ref: getSchemaPath(Message),
     },
   })
  @Post('message') // changed to post, cause get requests typically don't include a body
  async getAnswer( @Body() userMessage: Message, ): 
    Promise<{ message: Message }> {
    const message = await this.germanChatService.processMessage(userMessage);
    return { message };
  }
}
