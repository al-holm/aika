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
export class ChatService {
  /**
   * Processes a German chat message DTO and echoes back a formatted string.
   * @param {Message} userMessage - The German chat message DTO to process.
   * @returns {Promise<String>} A promise that resolves to a string containing the echoed message.
   */
  async processMessage (userMessage: Message, type: String): Promise<Message> {
    
    const botMessage = new Message();
    botMessage.userId= userMessage.userId;
    botMessage.messageId= uuidv4();
    botMessage.role = UserRole.Bot;
    botMessage.timestamp = new Date();
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
      const response: AxiosResponse = await client.post('/get_answer', data, config);
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
    async get_lesson(): Promise<JSON> 
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
   async get_tasks(): Promise<JSON> 
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

  async processAnswers(task_message: JSON){
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
}