/* eslint-disable @typescript-eslint/no-unused-vars */
import { Injectable } from '@nestjs/common';
import { Message, UserRole } from './models/message.dto';
import { v4 as uuidv4 } from 'uuid';
import axios, { AxiosResponse, AxiosRequestConfig, RawAxiosRequestHeaders } from 'axios';
import { ApiTags } from '@nestjs/swagger';
/**
 * Service class for processing German chat messages.
 * @class GermanChatService
 */
@ApiTags('API-Gateway')
@Injectable()
export class GermanChatService {
  /**
   * Processes a German chat message DTO and echoes back a formatted string.
   * @param {Message} userMessage - The German chat message DTO to process.
   * @returns {Promise<String>} A promise that resolves to a string containing the echoed message.
   */
  async processMessage(
    userMessage: Message,
  ): Promise<Message> {
    const botMessage = new Message();
    botMessage.userId= userMessage.userId;
    botMessage.messageId= uuidv4();
    botMessage.role = UserRole.Bot;
    botMessage.timestamp = new Date();
    //answerMessageDTO.message_text = await this.get_answer(messageDTO.message_text); // await the get_answer call
    botMessage.text = userMessage.text;
    await new Promise(r => setTimeout(r, 2000));
    return Promise.resolve(botMessage);
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