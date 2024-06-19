import { ApiTags} from '@nestjs/swagger';
import { Injectable, NotImplementedException } from "@nestjs/common";
import { Lesson, LessonType } from "src/interfaces/lesson.interface";
import { readLessonsFromFile, writeLessonsToFile } from "src/util/json.util";
import { Task } from '../interfaces/task.interface';
import { TaskDto } from './dto/task.dto';
@ApiTags('Curriculum')
@Injectable()
export class LessonService {
    private lessons: Lesson[] = [];

    constructor() {
        this.loadLessons()
    }

    private async loadLessons() {
        this.lessons = await readLessonsFromFile();
    }

    async getNextLesson() : Promise<boolean> {
        let lesson_d = await this.getNextUncompletedLesson();
        let request = `[${lesson_d['type']}][${lesson_d['topic']}][None][1][1][1]`;
        console.log(request);
        return true;
    }

    private async getNextUncompletedLesson(): Promise<{type: string, topic: string}> {
        for(let i = 0; i < this.lessons.length; i++) {
            var lesson = this.lessons[i];
            var uncompletedInd = lesson.completed.findIndex((el)=>!el);
            if (uncompletedInd != -1) {
                var type = Object.values(LessonType)[uncompletedInd];
                console.log(type);
                var topic = this.getNextTopic(type, lesson);
                return {type:type, topic:topic}
            } else {
                return {type: 'Grammar', topic: 'Konkunktiv II'}; // if the curriculum is completed, dummy value for now
            }
        }
    }

    private getNextTopic(type: string, lesson:Lesson) : string {
        if (type=='Grammar') {
            return lesson.grammar;
        } else if (type=='Reading') {
            return lesson.reading;
        } else if (type=='Listening') {
            return lesson.listening;
        } else {
            throw new NotImplementedException('This lesson type is not implemented.');
        }
    }

    async processUserAnswers(task: TaskDto) : Promise<boolean> {
        var lesson = this.lessons.find((el) => el.id == task.id);
        const lesson_type = task.lesson_type.toLowerCase();
        const index: number = Object.keys(LessonType).indexOf(lesson_type); 
        lesson.completed[index] = true;
        await writeLessonsToFile(this.lessons);
        return true;
    }
}