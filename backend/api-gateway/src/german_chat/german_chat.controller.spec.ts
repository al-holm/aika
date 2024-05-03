import { Test, TestingModule } from '@nestjs/testing';
import { GermanChatController } from './german_chat.controller';

describe('GermanChatController', () => {
  let controller: GermanChatController;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      controllers: [GermanChatController],
    }).compile();

    controller = module.get<GermanChatController>(GermanChatController);
  });

  it('should be defined', () => {
    expect(controller).toBeDefined();
  });
});
