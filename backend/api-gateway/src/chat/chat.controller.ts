import { Controller, Post, Get, Body, Param, UseGuards, Req} from '@nestjs/common';
import { ChatService } from './chat.service';
import { Message } from './models/message.dto';
import { ApiTags, ApiResponse, ApiExtraModels, getSchemaPath, ApiOperation} from '@nestjs/swagger';
import { AuthGuard } from '@nestjs/passport';

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
  @UseGuards(AuthGuard('jwt'))
  @Post('german')
  @ApiOperation({
    summary: 'Gets users answer and returns bot answer in the german chat',
  })
  async getAnswerGerman( @Body() userMessage: Message, @Req() req: any): 
    Promise<{ message: Message }> {
    console.log('german');
    const token = req.headers['authorization'];
    const message = await this.germanChatService.processMessage(userMessage, "language", token);
    return { message };
  }

  @Post('law')
  @UseGuards(AuthGuard('jwt'))
  @ApiOperation({
    summary: 'Gets users answer and returns bot answer in the las & life chat',
  })
  async getAnswerLawLife( @Body() userMessage: Message, @Req() req: any): 
    Promise<{ message: Message }> {
    console.log('law');
    const token = req.headers['authorization'];
    const message = await this.germanChatService.processMessage(userMessage, "law-life", token);
    return { message };
  }

  @Post('submit_answers')
  @UseGuards(AuthGuard('jwt'))
  @ApiOperation({
    summary: 'takes users answers to the exercises & process them',
  })
  async getCompletedTasks( @Body() taskJSON: JSON, @Req() req: any) {
    console.log('answers submitted');
    const token = req.headers['authorization'];
    await this.germanChatService.processAnswers(taskJSON, token);
  }

  @Get('lesson')
  @UseGuards(AuthGuard('jwt'))
  @ApiOperation({
    summary: 'return next lesson in german chat',
  })
  async getLesson(@Req() req: any):
    Promise<JSON> {
    console.log('lesson');
    const token = req.headers['authorization'];
    const lesson = await this.germanChatService.getLesson(token);
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

  @Get('history:chat-id')
  @UseGuards(AuthGuard('jwt'))
  @ApiOperation({
    summary: 'return message history',
  })
  async getMessageHistory(@Param('chat-id') chatID: string, @Req() req: any):
  Promise<{messages: Message[] }> {
    console.log('maessage history');
    const token = req.headers['authorization'];
    const history = await this.germanChatService.getChatHistory(chatID, token);
    return {'messages' : history};
  }
}
