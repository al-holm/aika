import { IsString, IsDateString } from 'class-validator';
import { ApiProperty } from '@nestjs/swagger';

export enum UserRole {
  Bot = 'bot',
  User = 'user'
}


/**
 * Object class for representing messages & enforces type safety for properties
 * @class Message
 */
export class Message {
  @ApiProperty({
    example: 'Hi! How are you?',
    required: true
 })
  @IsString()
  text: string;
  
  @ApiProperty({
    example: 'bot|user',
    required: true
 })
  role: UserRole;

  @ApiProperty({
    example: 'german',
    required: true
 })
  @IsString()
  chatID: string;
}


/**
 * Data Transfer Object class for representing messages & enforces type safety for properties
 * @class GermanChatMessageDto
 */
export class AgentMessageDTO {
  @IsString()
  text: string;
}
