import { Controller, Get, Post, Body } from '@nestjs/common';
import { LessonService } from './lesson.service';
import { ApiTags} from '@nestjs/swagger';
import { TaskDto } from './dto/task.dto';
@Controller('lesson')
@ApiTags('Curriculum')
export class LessonController {
  constructor(private readonly lessonsService: LessonService) {}

  @Get('next')
  async getNextLesson(): Promise<JSON>{
    return this.lessonsService.getNextLesson();
  }

  @Post('process_answers')
  async processAnswers(@Body() tasks: TaskDto[]) {
    console.log('processing user answers...')
    await this.lessonsService.processUserAnswers(tasks);
  }
}