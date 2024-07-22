import { IsBoolean, IsEmail, IsNotEmpty, IsOptional, IsString, MinLength } from 'class-validator';

export class UpdateLessonDto {

    @IsString()
    @MinLength(3)
    topic: string;

    @IsBoolean()
    value: boolean;
}
