import { Test, TestingModule } from '@nestjs/testing';
import { LessonService } from '../src/lesson/lesson.service';
import { readLessonsFromFile } from '../src/util/json.util';
import { Lesson } from '../src/interfaces/lesson.interface';

// Mocking the readLessonsFromFile function
jest.mock('../src/util/json.util', () => ({
  readLessonsFromFile: jest.fn(),
}));
describe('LessonService', () => {
  let service: LessonService;
  const mockLessons: Lesson[] = [
    {
      id: 1,
      name: "Introduction to English",
      grammar: "Basic sentence structures",
      reading: "Read a short story about daily routines",
      listening: "Listen to a conversation about hobbies",
      completed: [true, false, false],
      score: [90, 0, 0],
    },
    {
      id: 2,
      name: "Advanced Grammar",
      grammar: "Complex sentences and clauses",
      reading: "Read an article on climate change",
      listening: "Listen to a news report",
      completed: [true, true, false],
      score: [85, 78, 0],
    },
  ];

  beforeEach(async () => {
    (readLessonsFromFile as jest.Mock).mockResolvedValue(mockLessons);

    const module: TestingModule = await Test.createTestingModule({
      providers: [LessonService],
    }).compile();

    service = module.get<LessonService>(LessonService);
  });

  it('should be defined', () => {
    expect(service).toBeDefined();
  });

  it('should load lessons on initialization', async () => {
    //@ts-ignore
    await service.loadLessons();
    expect(service['lessons']).toEqual(mockLessons);
  });

  it('should return the next uncompleted lesson', async () => {
    //@ts-ignore
    const nextLesson = await service.getNextUncompletedLesson();
    expect(nextLesson).toEqual({
      type: 'Reading',
      topic: 'Read a short story about daily routines',
    });
  });

  it('should construct the correct request in getNextLesson', async () => {
    const consoleSpy = jest.spyOn(console, 'log');
    await service.getNextLesson();
    expect(consoleSpy).toHaveBeenCalledWith('[Reading][Read a short story about daily routines][None][1][1][1]');
  });

  it('should handle processUserAnswers correctly', async () => {
    const result = await service.processUserAnswers({} as any);
    expect(result).toBe(true);
  });

  it('should handle completed curriculum', async () => {
    // Mock all lessons as completed
    const completedLessons = mockLessons.map(lesson => ({
      ...lesson,
      completed: [true, true, true],
    }));
    (readLessonsFromFile as jest.Mock).mockResolvedValue(completedLessons);
    //@ts-ignore
    await service.loadLessons();
    //@ts-ignore
    const nextLesson = await service.getNextUncompletedLesson();
    expect(nextLesson).toEqual({ type: 'Grammar', topic: 'Konkunktiv II' });
  });

  it('should throw an error for unsupported lesson type in getNextTopic', () => {
    const invalidType = 'InvalidType';
    expect(() => service['getNextTopic'](invalidType, mockLessons[0])).toThrowError('This lesson type is not implemented.');
  });
});