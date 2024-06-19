import { Controller, Get, Post, Body } from '@nestjs/common';
import { LessonService } from './lesson.service';
import { ApiTags} from '@nestjs/swagger';
@Controller('lesson')
@ApiTags('Curriculum')
export class LessonController {
  constructor(private readonly lessonsService: LessonService) {}

  @Get('get_next_lesson')
  async getNextLesson(): Promise<boolean>{
    return this.lessonsService.getNextLesson();
  }

  @Post('process_answers')
  async processAnswers(@Body() TaskDto): Promise<boolean> {
    return this.lessonsService.processUserAnswers(TaskDto);
  }
}