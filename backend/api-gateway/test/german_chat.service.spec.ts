import { Test, TestingModule } from '@nestjs/testing';
import { Message } from '../src/chat/models/message.dto';
import { ChatService } from '../src/chat/chat.service';
import { setupServer } from 'msw/node';
import { http } from 'msw';
import { json } from 'express';
export const server = setupServer(
  http.post('http://127.0.0.1:5000/get_answer', () => {
    return new Response(JSON.stringify({answer: 'test msg' }), {
      headers: {
        'Content-Type': 'application/json',
      },
    })
  }),
  http.post('http://127.0.0.1:5000/get_answer_law_life', () => {
    return new Response(JSON.stringify({answer: 'test msg' }), {
      headers: {
        'Content-Type': 'application/json',
      },
    })
  }),

  http.post('http://127.0.0.1:3543/lesson/process_answers', () => {
    return new Response(JSON.stringify({answer: 'test msg' }), {
      headers: {
        'Content-Type': 'application/json',
      },
    })
  }),

  http.get('http://127.0.0.1:3543/lesson/next', () => {
    return new Response(JSON.stringify({answer: 'test msg' }), {
      headers: {
        'Content-Type': 'application/json',
      },
    })
  }),

  http.get('http://127.0.0.1:3543/lesson/tasks', () => {
    return new Response(JSON.stringify({answer: 'test msg' }), {
      headers: {
        'Content-Type': 'application/json',
      },
    })
  })
);

/**
 * Test suite for the GermanChatService class.
 */
describe('GermanChatService', () => {
  let service: ChatService;

  beforeAll(() => {
    server.listen()
  })  

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [ChatService],
    }).compile();

    service = module.get(ChatService);
  });

  it('should be defined', () => {
    expect(service).toBeDefined();
  });

  /**
   * Test case for the processMessage function.
   * It should return a formatted echo of the input message.
   * @returns None
   */
  describe('processMessage', () => {
    it('should return a response for german chat', async () => {
      const mockDto = new Message();
      mockDto.userId= '12345';
      const result = await service.processMessage(mockDto, 'language');
      expect(result).toBeDefined();
      expect(result.userId).toEqual(mockDto.userId);
      expect(result.messageId).toBeDefined(); // Ensure a UUID is generated
      expect(result.role).toEqual('bot');
      expect(result.text).toContain('test msg');
      expect(result.timestamp).toBeInstanceOf(Date);
    });

  it('should return a response for law chat', async () => {
    const mockDto = new Message();
    mockDto.userId= '12345';
    const result = await service.processMessage(mockDto, "law-life");
    expect(result).toBeDefined();
    expect(result.userId).toEqual(mockDto.userId);
    expect(result.messageId).toBeDefined(); // Ensure a UUID is generated
    expect(result.role).toEqual('bot');
    expect(result.text).toContain('test msg');
    expect(result.timestamp).toBeInstanceOf(Date);
  });

  it('should return a response for an invalid type', async () => {
    const mockDto = new Message();
    mockDto.userId= '12345';
    const result = await service.processMessage(mockDto, "abrakadabra");
    expect(result).toBeDefined();
    expect(result.userId).toEqual(mockDto.userId);
    expect(result.messageId).toBeDefined(); // Ensure a UUID is generated
    expect(result.role).toEqual('bot');
    expect(result.text).toContain("Something's gone wrong");
    expect(result.timestamp).toBeInstanceOf(Date);
  });
});
describe('getLesson', () => {
  it('should return a lesson', async () => {
    const result = await service.getLesson();
    expect(result).toBeDefined();
    var res =JSON.stringify(result);
    expect(JSON.parse(res).answer).toContain('test msg');
  });
});
describe('getTasks', () => {
  it('should return a task', async () => {
    const result = await service.getTasks();
    expect(result).toBeDefined();
    var res =JSON.stringify(result);
    expect(JSON.parse(res).answer).toContain('test msg');
  });
});
});
