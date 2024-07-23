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
@ApiTags('ChatAPI')
@Injectable()
export class ChatService {
  /**
   * Processes a German chat message DTO and echoes back a formatted string.
   * @param {Message} userMessage - The German chat message DTO to process.
   * @returns {Promise<String>} A promise that resolves to a string containing the echoed message.
   */
  async processMessage (userMessage: Message, type: String, token: string): Promise<Message> {
    const client = axios.create({
      baseURL: 'http://127.0.0.1:3501/user/',
    });
    const config: AxiosRequestConfig = {
      headers: {
        'Accept': 'application/json', 'Authorization': `Bearer ${token}`
      } as RawAxiosRequestHeaders,
    };
    await client.put('put-message', JSON.stringify(userMessage), config);
    const botMessage = new Message();
    botMessage.role = UserRole.Bot;
    console.log(type);
    switch(type) {
      case "language": {
        botMessage.text = await this.get_answer(userMessage.text);
        break;
      }
      case "law-life": {
        botMessage.text = await this.get_answer_law_life(userMessage.text);
        break;
      }
      default: {
        botMessage.text = "Something's gone wrong"
        console.log("processMessage: unexpected type")
      }
    }
    await client.put('put-message', JSON.stringify(botMessage), config);
    return Promise.resolve(botMessage);
  }

  /**
   * Makes a POST request to get an answer for the given question.
   * @returns {Promise<string>} The answer from the API or error if an error occurs.
   */
  async get_answer(question : string): Promise<string> {
    const client = axios.create({
      baseURL: 'http://127.0.0.1:5000',
    });

    const config: AxiosRequestConfig = {
      headers: {
        'Accept': 'application/json',
      } as RawAxiosRequestHeaders,
    };

    try {
      const data = { 'question': question };
      const response: AxiosResponse = await client.post('/get_answer_german', data, config);
      return response.data['answer'];
    } catch (err) {
      console.log(err);
      return err;
    }
  }

    /**
   * Makes a POST request to get an answer for the given question to the topic law and life.
   * @returns {Promise<string>} The answer from the API or error if an error occurs.
   */
    async get_answer_law_life(question : string): Promise<string> 
    {
      
      const client = axios.create({baseURL: 'http://127.0.0.1:5000',});
  
      const config: AxiosRequestConfig = {
        headers: {
          'Accept': 'application/json',
        } as RawAxiosRequestHeaders,
      };
  
      try {
        const data = { 'question': question };
        const response: AxiosResponse = await client.post('/get_answer_law_life', data, config);
        return response.data['answer'];
      } catch (err) {
        console.log(err);
        return err;
      }
    }

    /**
   * Makes a POST request to get an answer for the given question to the topic law and life.
   * @returns {Promise<JSON>} The answer from the API or error if an error occurs.
   */
    async getLesson(token: string): Promise<JSON> 
    {
      
      const client = axios.create({baseURL: 'http://127.0.0.1:3543/lesson',});
  
      const config: AxiosRequestConfig = {
        headers: {
          'Accept': 'application/json',
        } as RawAxiosRequestHeaders,
      };
  
      try {
        const response: AxiosResponse = await client.get('/next', config);
        return response.data;
      } catch (err) {
        console.log(err);
        return err;
      }
  }

   /**
   * Makes a POST request to get an answer for the given question to the topic law and life.
   * @returns {Promise<JSON>} The answer from the API or error if an error occurs.
   */
   async getTasks(): Promise<JSON> 
   {
     
     const client = axios.create({baseURL: 'http://127.0.0.1:3543/lesson',});
 
     const config: AxiosRequestConfig = {
       headers: {
         'Accept': 'application/json',
       } as RawAxiosRequestHeaders,
     };
 
     try {
       const response: AxiosResponse = await client.get('/tasks', config);
       return response.data;
     } catch (err) {
       console.log(err);
       return err;
     }
 }

  async processAnswers(task_message: JSON, token: string){
    const client = axios.create({baseURL: 'http://127.0.0.1:3543/lesson',});
    const config: AxiosRequestConfig = {
      headers: {
        'Accept': 'application/json',
      } as RawAxiosRequestHeaders,
    };
      try {
        await client.post('/process_answers', task_message, config);
    } catch (err) {
      console.log(err);
    }
  }

  async getChatHistory(chatID: string, token: string) {
    const client = axios.create({
      baseURL: 'http://127.0.0.1:3501/user/',
    });
    const config: AxiosRequestConfig = {
      headers: {
        'Accept': 'application/json', 'Authorization': `Bearer ${token}`
      } as RawAxiosRequestHeaders,
    };
    return (await client.get(`:${chatID}`, config)).data.messages;
  }
}