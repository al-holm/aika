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
    example: '26b713d6-de95-4df6-9227-36ba07869a4e',
    required: true
 })

  @IsString()
  userId: string;

  @ApiProperty({
    example: '35d47560-dcff-4767-9903-16e8096d055a',
    required: true
 })
  @IsString()
  messageId: string;

  @ApiProperty({
    example: 'bot|user',
    required: true
 })
  role: UserRole;

  @ApiProperty({
    example: '2024-05-23 11:54:37',
    required: true
 })
  @IsDateString()
  timestamp: Date;

  @ApiProperty({
    example: 'Hi! How are you?',
    required: true
 })
  @IsString()
  text: string;
}


/**
 * Data Transfer Object class for representing messages & enforces type safety for properties
 * @class GermanChatMessageDto
 */
export class AgentMessageDTO {
  @IsString()
  text: string;
}
