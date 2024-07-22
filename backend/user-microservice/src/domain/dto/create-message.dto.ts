import { IsBoolean, IsEmail, IsNotEmpty, IsOptional, IsString, MinLength } from 'class-validator';

export class CreateMessageDto {
    @IsString()
    text: string;

    @IsString()
    role: string;

    @IsString()
    chatID: string;
}
