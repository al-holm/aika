/* eslint-disable @typescript-eslint/no-unused-vars */
import { Injectable } from '@nestjs/common';
import { GermanChatMessageDto } from './dto/german-chat-question.dto';
import { v4 as uuidv4 } from 'uuid';
import axios, { AxiosResponse, AxiosRequestConfig, RawAxiosRequestHeaders } from 'axios';

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
    //answerMessageDTO.message_text = await this.get_answer(messageDTO.message_text); // await the get_answer call
    answerMessageDTO.message_text = messageDTO.message_text;
    await new Promise(r => setTimeout(r, 2000));
    return Promise.resolve(answerMessageDTO);
  }

  /**
   * Makes a POST request to get an answer for the given question.
   * @returns {Promise<string>} The answer from the API or error if an error occurs.
   */
  async get_answer(question : string): Promise<string> {
    const client = axios.create({
      baseURL: 'http://localhost:5000',
    });

    const config: AxiosRequestConfig = {
      headers: {
        'Accept': 'application/json',
      } as RawAxiosRequestHeaders,
    };

    try {
      const data = { 'question': question };
      const response: AxiosResponse = await client.post('/get_answer', data, config);
      console.log(response.status);
      console.log(response.data);
      return response.data['answer'];
    } catch (err) {
      console.log(err);
      return err;
    }
  }
}