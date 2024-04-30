import { Controller, Get, Body } from '@nestjs/common';
import { Interface } from 'readline';
import { AnswerGermanChat } from 'src/dto/answer-german-chat.dto';

@Controller('german-chat')
export class GermanChatController {
    @Get()
    getAnswer(@Body() request: AnswerGermanChat) : { answer_text: string; }{
        /**
         * Handle a user message reply request 
         * Parameters:
         * request: AnswerGermanChat - the body of the request
         * Returns:
         * Object with only one parameter: answer_text: string
         */
        return { answer_text: `User ${request.user_id} has sent the message ${request.question_text} on ${request.time_stamp}`}
    }
}
