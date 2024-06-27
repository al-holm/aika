import { Controller, Post, Get, Body } from '@nestjs/common';
import { ChatService } from './chat.service';
import { Message } from './models/message.dto';
import { ApiTags, ApiResponse, ApiExtraModels, getSchemaPath } from '@nestjs/swagger';

/**
 * Controller class for handling POST requests for processing messages in a
German chat application.
 * @class GermanChatController
 */
@ApiTags('API-Gateway')
@Controller('chat')
export class ChatController {
  constructor(private readonly germanChatService: ChatService) {}

  @ApiExtraModels(Message)
  @ApiResponse({
     status: 201,
     schema: {
       $ref: getSchemaPath(Message),
     },
   })

  @Post('german')
  async getAnswer( @Body() userMessage: Message, ): 
    Promise<{ message: Message }> {
    console.log('german');
    const message = await this.germanChatService.processMessage(userMessage, "language");
    return { message };
  }

  @Post('law')
  async getAnswerLawLife( @Body() userMessage: Message, ): 
    Promise<{ message: Message }> {
    console.log('law');
    const message = await this.germanChatService.processMessage(userMessage, "law-life");
    return { message };
  }

  @Post('submit_answers')
  async getCompletedTasks( @Body() taskJSON: JSON) {
    console.log('answers submitted');
    await this.germanChatService.processAnswers(taskJSON);
  }

  @Get('lesson')
  async getLesson():
    Promise<JSON> {
    console.log('lesson');
    const lesson = await this.germanChatService.getLesson();
    return lesson;
  }

  @Get('tasks')
  async getTasks():
    Promise<JSON> {
    console.log('tasks');
    const tasks = await this.germanChatService.getTasks();
    return tasks;
  }
}
