import { Test, TestingModule } from '@nestjs/testing';
import { GermanChatService } from './german_chat.service';
import { GermanChatMessageDto } from './dto/german-chat-question.dto';

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
      const mockDto = new GermanChatMessageDto();
      mockDto.user_id = '12345';
      mockDto.message_text = 'Hallo! Wie geht’s?';
      const result = await service.processMessage(mockDto);
      expect(result).toBeDefined();
      expect(result.user_id).toEqual(mockDto.user_id);
      expect(result.message_id).toBeDefined(); // Ensure a UUID is generated
      expect(result.role).toEqual('bot');
      expect(result.message_text).toContain('Hallo! Wie geht’s?');
      expect(result.timestamp).toBeInstanceOf(Date);
    });
  });
});
