/* eslint-disable @typescript-eslint/no-unused-vars */
import { Injectable } from '@nestjs/common';
import axios, { AxiosResponse, AxiosRequestConfig, RawAxiosRequestHeaders } from 'axios';
import { ApiTags } from '@nestjs/swagger';
import { Credentials } from './models/credentials';
/**
 * Service class for processing German chat messages.
 * @class GermanChatService
 */
@ApiTags('AuthAPI')
@Injectable()
export class AuthService {
  async validateCredentials(credentials: Credentials): Promise<string> {
    const client = axios.create({
      baseURL: 'http://127.0.0.1:3501/',
    });

    const config: AxiosRequestConfig = {
      headers: {
        'Accept': 'application/json',
      } as RawAxiosRequestHeaders,
    };
    var pattern;
    if (credentials.isSignUp) {
      pattern = 'register';
    } else {
      pattern = 'login';
    }

    try {
      const data = { 'username': credentials.username, 'password': credentials.password};
      const response: AxiosResponse = await client.post('/auth/' + pattern, data, config);
      return response.data['token'];
    } catch (err) {
      console.log(err);
      return err;
    }
  }
}