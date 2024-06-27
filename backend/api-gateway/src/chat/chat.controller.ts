import { Controller, Post, Get, Body } from '@nestjs/common';
import { ChatService } from './chat.service';
import { Message } from './models/message.dto';
import { ApiTags, ApiResponse, ApiExtraModels, getSchemaPath, ApiOperation} from '@nestjs/swagger';

/**
 * Controller class for handling POST requests for processing messages in a
German chat application.
 * @class GermanChatController
 */
@ApiTags('ChatAPI')
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
  @ApiOperation({
    summary: 'Gets users answer and returns bot answer in the german chat',
  })
  async getAnswerGerman( @Body() userMessage: Message, ): 
    Promise<{ message: Message }> {
    console.log('german');
    const message = await this.germanChatService.processMessage(userMessage, "language");
    return { message };
  }

  @Post('law')
  @ApiOperation({
    summary: 'Gets users answer and returns bot answer in the las & life chat',
  })
  async getAnswerLawLife( @Body() userMessage: Message, ): 
    Promise<{ message: Message }> {
    console.log('law');
    const message = await this.germanChatService.processMessage(userMessage, "law-life");
    return { message };
  }

  @Post('submit_answers')
  @ApiOperation({
    summary: 'takes users answers to the exercises & process them',
  })
  async getCompletedTasks( @Body() taskJSON: JSON) {
    console.log('answers submitted');
    await this.germanChatService.processAnswers(taskJSON);
  }

  @Get('lesson')
  @ApiOperation({
    summary: 'return next lesson in german chat',
  })
  async getLesson():
    Promise<JSON> {
    console.log('lesson');
    const lesson = await this.germanChatService.getLesson();
    return lesson;
  }

  @Get('tasks')
  @ApiOperation({
    summary: 'return tasks for the current lesson in german chat',
  })
  async getTasks():
    Promise<JSON> {
    console.log('tasks');
    const tasks = await this.germanChatService.getTasks();
    return tasks;
  }
}
