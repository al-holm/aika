import { IsEnum, IsNumber, IsString, IsArray, IsBoolean, ValidateNested, ArrayNotEmpty, IsOptional } from 'class-validator';
import { TaskType } from 'src/interfaces/task.interface';

export class TaskDto {
  @IsEnum(TaskType)
  type: TaskType;

  @IsNumber()
  id: number;

  @IsString()
  lesson_type: string;

  @IsString()
  question: string;

  @IsArray()
  @ArrayNotEmpty()
  @IsArray({ each: true })
  options: string[][];

  @IsArray()
  @ArrayNotEmpty()
  @IsArray({ each: true })
  userAnswers: string[][];

  @IsArray()
  @ArrayNotEmpty()
  @IsString({ each: true })
  solutions: string[];
}