/* eslint-disable @typescript-eslint/no-unused-vars */
import { Injectable } from '@nestjs/common';
import { GermanChatMessageDto } from './dto/german-chat-question.dto';
import { v4 as uuidv4 } from 'uuid';
/**
 * Service class for processing German chat messages.
 * @class GermanChatService
 */
@Injectable()
export class GermanChatService {
  /**
   * Processes a German chat message DTO and echoes back a formatted string.
   * @param {GermanChatMessageDto} messageDTO - The German chat message DTO to process.
   * @returns {Promise<String>} A promise that resolves to a string containing the echoed message.
   */
  async processMessage(
    messageDTO: GermanChatMessageDto,
  ): Promise<GermanChatMessageDto> {
    const answerMessageDTO = new GermanChatMessageDto();
    answerMessageDTO.user_id = messageDTO.user_id;
    answerMessageDTO.message_id = uuidv4();
    answerMessageDTO.role = 'bot';
    answerMessageDTO.timestamp = new Date();
    answerMessageDTO.message_text = `Backend echoed from ${messageDTO.user_id}: ${messageDTO.message_text}`;

    return Promise.resolve(answerMessageDTO);
  }
}
