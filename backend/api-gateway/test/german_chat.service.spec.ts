import { Test, TestingModule } from '@nestjs/testing';
import { Message } from '../src/chat/models/message.dto';
import { ChatService } from '../src/chat/chat.service';

/**
 * Test suite for the GermanChatService class.
 */
describe('GermanChatService', () => {
  let service: ChatService;

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
    it('should return a formatted echo of the input message', async () => {
      const mockDto = new Message();
      mockDto.userId= '12345';
      mockDto.text = 'Hallo! Wie geht’s?';
      const result = await service.processMessage(mockDto);
      expect(result).toBeDefined();
      expect(result.userId).toEqual(mockDto.userId);
      expect(result.messageId).toBeDefined(); // Ensure a UUID is generated
      expect(result.role).toEqual('bot');
      expect(result.text).toContain('Hallo! Wie geht’s?');
      expect(result.timestamp).toBeInstanceOf(Date);
    });
  });
});
