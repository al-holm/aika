import { ApiTags} from '@nestjs/swagger';
import { Injectable, NotImplementedException } from "@nestjs/common";
import { Lesson, LessonType } from "src/interfaces/lesson.interface";
import { readLessonsFromFile, writeLessonsToFile } from "src/util/json.util";
import { Task } from '../interfaces/task.interface';
import { TaskDto } from './dto/task.dto';
import axios, { AxiosRequestConfig, AxiosResponse, RawAxiosRequestHeaders } from 'axios';
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

    async getNextLesson() : Promise<JSON> {
        let lesson_d = await this.getNextUncompletedLesson();
        let request = `[${lesson_d['type']}][${lesson_d['topic']}][None][2][1][1]`;
        console.log(`Sending request to the agent:${request}`)
        const client = axios.create({baseURL: 'http://127.0.0.1:5000',});
        const config: AxiosRequestConfig = {
        headers: {
            'Accept': 'application/json',
        } as RawAxiosRequestHeaders,
        };
        try {
            const data = { 'question': request};
            const response: AxiosResponse = await client.post('/get_lesson', data, config);
            response.data.id = lesson_d['id'];
            response.data.lessonType = lesson_d['type'];
            return response.data;
        } catch (err) {
            console.log(err);
            return err;
        }
    }

    private async getNextUncompletedLesson(): Promise<{type: string, topic: string, id: number}> {
        for(let i = 0; i < this.lessons.length; i++) {
            var lesson = this.lessons[i];
            var uncompletedInd = lesson.completed.findIndex((el)=>!el);
            if (uncompletedInd != -1) {
                var type = Object.values(LessonType)[uncompletedInd];
                var topic = this.getNextTopic(type, lesson);
                return {type:type, topic:topic, id: lesson.id}
            } else {
                return {type: 'Grammar', topic: 'Konkunktiv II', id: -1}; // if the curriculum is completed, dummy value for now
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

    async processUserAnswers(tasks: TaskDto[]) {
        var task = tasks[0];
        var lesson = this.lessons.find((el) => el.id == task.id);
        const lesson_type = task.lessonType.toLowerCase();
        const index: number = Object.keys(LessonType).indexOf(lesson_type); 
        lesson.completed[index] = true;
        await writeLessonsToFile(this.lessons);
        console.log('Answers processed')
    }
}