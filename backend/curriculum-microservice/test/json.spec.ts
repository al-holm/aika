import { promises as fs } from 'fs';
import * as path from 'path';
import { Lesson } from 'src/interfaces/lesson.interface';
import { readLessonsFromFile, writeLessonsToFile } from 'src/util/json.util';

jest.mock('fs', () => ({
    promises: {
      readFile: jest.fn(),
      writeFile: jest.fn(),
    },
  }));

describe('JSON Operations', () => {
  const filePathInit = path.join(__dirname, '../data/curriculum.json');
  const filePathSession = path.join(__dirname, '../out/curriculum.json');

  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe('readLessonsFromFile', () => {
    it('should read lessons from file and return them', async () => {
      const mockData = JSON.stringify([{ id: 1, name: 'Lesson 1' } as Lesson]);
      (fs.readFile as jest.Mock).mockResolvedValue(mockData);

      const result = await readLessonsFromFile();

      expect(result).toEqual([{ id: 1, name: 'Lesson 1' }]);
      expect(fs.readFile).toHaveBeenCalledWith(filePathInit, 'utf-8');
    })

    it('should return an empty array if the file does not exist', async () => {
        const error = new Error('File not found');
        (error as any).code = 'ENOENT';
        (fs.readFile as jest.Mock).mockRejectedValue(error);
  
        const result = await readLessonsFromFile();
  
        expect(result).toEqual([]);
      });
});

  describe('writeLessonsToFile', () => {
    it('should write lessons to file', async () => {
      const lessons: Lesson[] = [{ id: 1, name: 'Lesson 1' } as Lesson];
      const formattedLessons = JSON.stringify(lessons, null, 2);
      await writeLessonsToFile(lessons);

      expect(fs.writeFile).toHaveBeenCalledWith(
        filePathSession,formattedLessons
      );
    });
  })
});