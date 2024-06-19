import { Lesson } from '../interfaces/lesson.interface';
import { promises as fs } from 'fs';
import * as path from 'path';

const filePath = path.join(__dirname, '../../data/curriculum.json');

export const readLessonsFromFile = async (): Promise<Lesson[]> => {
  try {
    const data = await fs.readFile(filePath, 'utf-8');
    return JSON.parse(data);
  } catch (err) {
    if (err.code === 'ENOENT') {
      return [];
    }
    throw err;
  }
};

export const writeLessonsToFile = async (lessons: Lesson[]): Promise<void> => {
  await fs.writeFile(filePath, JSON.stringify(lessons, null, 2));
};