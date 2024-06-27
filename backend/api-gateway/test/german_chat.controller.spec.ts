import { ChatController } from '../src/chat/chat.controller';
import { Message } from '../src/chat/models/message.dto';
import { ChatService } from '../src/chat/chat.service';
import { Test, TestingModule } from '@nestjs/testing';

/**
 * Test suite for the GermanChatController class.
 */
describe('GermanChatController', () => {
  let controller: ChatController;
  let mockGermanChatService: Partial<ChatService>;

  beforeEach(async () => {
    // Create a mock service
    mockGermanChatService = {
      processMessage: jest.fn((dto) =>
        Promise.resolve({ ...dto, processed: true }),
      ),
      getLesson : jest.fn(),
      getTasks : jest.fn()
    };

    // Create a module with GermanChatController and the mock service
    const module: TestingModule = await Test.createTestingModule({
      controllers: [ChatController],
      providers: [
        {
          provide: ChatService,
          useValue: mockGermanChatService,
        },
      ],
    }).compile();

    controller = module.get<ChatController>(ChatController);
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
      const messageDto = new Message();
      messageDto.text = 'Hello';
      messageDto.messageId = '123';

      const response = await controller.getAnswerGerman(messageDto);

      expect(mockGermanChatService.processMessage).toHaveBeenCalledWith(
        messageDto,  "language"
      );
      expect(response).toEqual({ message: { ...messageDto, processed: true } });
    });

  it('should return the processed message', async () => {
    const messageDto = new Message();
    messageDto.text = 'Hello';
    messageDto.messageId = '123';

    const response = await controller.getAnswerLawLife(messageDto);

    expect(mockGermanChatService.processMessage).toHaveBeenCalledWith(
      messageDto,  "law-life"
    );
    expect(response).toEqual({ message: { ...messageDto, processed: true } });
  });

  it('should return the lesson', async () => {
    const response = await controller.getLesson();

    expect(mockGermanChatService.getLesson).toHaveBeenCalled();
   });

   it('should return the tasls', async () => {
    const response = await controller.getTasks();

    expect(mockGermanChatService.getTasks).toHaveBeenCalled();
   });
});
});
