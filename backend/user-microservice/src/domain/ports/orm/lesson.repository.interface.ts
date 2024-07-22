import { Lesson } from "src/domain/entities/lesson.entity";

export interface ILessonRepository {
    findOne(userID: number): Promise<Lesson[]>;
    update(userID: number, topic: string, value: boolean): Promise<void>;
}
