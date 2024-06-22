import { Test, TestingModule } from '@nestjs/testing';
import { TaskType } from 'src/interfaces/task.interface';
import { TaskDto } from 'src/lesson/dto/task.dto';
import { LessonController } from 'src/lesson/lesson.controller';
import { LessonService } from 'src/lesson/lesson.service';
describe('LessonController', () => {
  let controller: LessonController;
  let service: LessonService;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      controllers: [LessonController],
      providers: [
        {
          provide: LessonService,
          useValue: {
            getNextLesson: jest.fn(),
            processUserAnswers: jest.fn(),
          },
        },
      ],
    }).compile();

    controller = module.get<LessonController>(LessonController);
    service = module.get<LessonService>(LessonService);
  });

  it('should be defined', () => {
    expect(controller).toBeDefined();
  });

  describe('getNextLesson', () => {
    it('should return the next lesson', async () => {
      const mockLesson = { id: 1, type: 'Reading', topic: 'Mein Beruf' };
      jest.spyOn(service, 'getNextLesson').mockResolvedValue(mockLesson as any);

      const result = await controller.getNextLesson();

      expect(result).toEqual(mockLesson);
      expect(service.getNextLesson).toHaveBeenCalled();
    });
  });

  describe('processAnswers', () => {
    it('should call processUserAnswers with correct parameters', async () => {
      const tasks: TaskDto[] =  [{
        type: TaskType.single_choice,
        id: 1,
        lessonType: 'Reading',
        question: 'What is your name?',
        userAnswers: [['John']],
        solutions: ['John'],
      }];

      await controller.processAnswers(tasks);

      expect(service.processUserAnswers).toHaveBeenCalledWith(tasks);
      expect(service.processUserAnswers).toHaveBeenCalledTimes(1);
    });
  });
});