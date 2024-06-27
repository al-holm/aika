import { Controller, Get, Post, Body } from '@nestjs/common';
import { LessonService } from './lesson.service';
import { ApiTags, ApiOperation} from '@nestjs/swagger';
import { TaskDto } from './dto/task.dto';
@Controller('lesson')
@ApiTags('CurriculumAPI')
export class LessonController {
  constructor(private readonly lessonsService: LessonService) {}

  @Get('next')
  @ApiOperation({ summary: 'Returns next lesson according to the curriculum' })
  async getNextLesson(): Promise<JSON>{
    return this.lessonsService.getNextLesson();
  }

  @Get('tasks')
  @ApiOperation({ summary: 'Gets tasks for the current lesson according to the curriculum' })
  async getTasks(): Promise<JSON>{
    return this.lessonsService.getTasks();
  }

  @Post('process_answers')
  @ApiOperation({ summary: 'Process user answers and updates progress.' })
  async processAnswers(@Body() tasks: TaskDto[]) {
    console.log('processing user answers...')
    await this.lessonsService.processUserAnswers(tasks);
  }
}