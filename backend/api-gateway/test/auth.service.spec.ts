import { Test, TestingModule } from '@nestjs/testing';
import { Message } from '../src/chat/models/message.dto';
import { ChatService } from '../src/chat/chat.service';
import { setupServer } from 'msw/node';
import { http } from 'msw';
import { json } from 'express';
import { AuthService } from 'src/auth/auth.service';
import { Credentials } from 'src/auth/models/credentials';
export const server = setupServer(
  http.post('http://127.0.0.1:3501/auth/login', () => {
    return new Response(JSON.stringify({access_token: 'login123' }), {
      headers: {
        'Content-Type': 'application/json',
      },
    })
  }),
  http.post('http://127.0.0.1:3501/auth/register', () => {
    return new Response(JSON.stringify({access_token: 'register123' }), {
      headers: {
        'Content-Type': 'application/json',
      },
    })
  }),
)


describe('AuthService', () => {
  let service: AuthService;

  beforeAll(() => {
    server.listen()
  })  

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [AuthService],
    }).compile();

    service = module.get(AuthService);
  });

  it('should be defined', () => {
    expect(service).toBeDefined();
  });


  describe('login', () => {
    it('should return a scess tokem', async () => {
      const credentials = new Credentials();
      credentials.username = 'sss';
      credentials.password = '111';
      credentials.isSignUp = false;

      const result = await service.validateCredentials(credentials);
      expect(result).toBeDefined();
      expect(result).toEqual('login123');
    });

    describe('register', () => {
      it('should access token', async () => {
        const credentials = new Credentials();
        credentials.username = 'sss';
        credentials.password = '111';
        credentials.isSignUp = true;
  
        const result = await service.validateCredentials(credentials);
        expect(result).toBeDefined();
        expect(result).toEqual('register123');
      });
});
});
});
