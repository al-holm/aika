import { Test, TestingModule } from '@nestjs/testing';
import { GermanChatService } from './german_chat.service';
import { GermanChatMessageDto } from './dto/german-chat-question.dto';
import { GermanChatController } from './german_chat.controller';

/**
 * Test suite for the GermanChatController class.
 */
describe('GermanChatController', () => {
  let controller: GermanChatController;
  let mockGermanChatService: Partial<GermanChatService>;

  beforeEach(async () => {
    // Create a mock service
    mockGermanChatService = {
      processMessage: jest.fn((dto) =>
        Promise.resolve({ ...dto, processed: true }),
      ),
    };

    // Create a module with GermanChatController and the mock service
    const module: TestingModule = await Test.createTestingModule({
      controllers: [GermanChatController],
      providers: [
        {
          provide: GermanChatService,
          useValue: mockGermanChatService,
        },
      ],
    }).compile();

    controller = module.get<GermanChatController>(GermanChatController);
  });

  it('should be defined', () => {
    expect(controller).toBeDefined();
  });

  /**
   * Describes a test suite for the POST /message endpoint.
   * It tests whether the endpoint returns the processed message correctly.
   * @returns None
   */
  describe('POST /message', () => {
    it('should return the processed message', async () => {
      const messageDto = new GermanChatMessageDto();
      messageDto.message_text = 'Hello';
      messageDto.user_id = '123';

      const response = await controller.getAnswer(messageDto);

      expect(mockGermanChatService.processMessage).toHaveBeenCalledWith(
        messageDto,
      );
      expect(response).toEqual({ message: { ...messageDto, processed: true } });
    });
  });
});
