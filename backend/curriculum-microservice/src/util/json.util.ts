import { randomUUID } from 'crypto';
import { Lesson } from '../interfaces/lesson.interface';
import { promises as fs } from 'fs';
import * as path from 'path';

const filePathInit = path.join(__dirname, '../../data/curriculum.json');
const filePathSession = path.join(__dirname, '../../out/curriculum.json');
export const readLessonsFromFile = async (): Promise<Lesson[]> => {
  try {
    const data = await fs.readFile(filePathInit, 'utf-8');
    return JSON.parse(data);
  } catch (err) {
    if (err.code === 'ENOENT') {
      return [];
    }
    throw err;
  }
};

export const writeLessonsToFile = async (lessons: Lesson[]): Promise<void> => {
  await fs.writeFile(filePathSession, JSON.stringify(lessons, null, 2));
};