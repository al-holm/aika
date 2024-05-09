import { IsString, IsDateString } from 'class-validator';
export class GermanChatMessageDto {
  /* The `@IsString()` decorator is used in TypeScript with the class-validator library to enforce
    that the `user_id` property of the `GermanChatMessageDto` class must be a string type. This helps ensure type safety and data integrity. */
  @IsString()
  user_id: string;

  @IsString()
  message_id: string;

  @IsString()
  role: string;

  @IsDateString()
  timestamp: Date;

  @IsString()
  message_text: string;
}
