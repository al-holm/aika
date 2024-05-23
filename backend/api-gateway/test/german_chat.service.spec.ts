import { Test, TestingModule } from '@nestjs/testing';
import { Message } from '../src/german_chat/models/message.dto';
import { GermanChatService } from './../src/german_chat/german_chat.service';

/**
 * Test suite for the GermanChatService class.
 */
describe('GermanChatService', () => {
  let service: GermanChatService;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [GermanChatService],
    }).compile();

    service = module.get(GermanChatService);
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
