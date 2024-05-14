import { IsString, IsDateString } from 'class-validator';


/**
 * Data Transfer Object class for representing messages & enforces type safety for properties
 * @class GermanChatMessageDto
 */
export class GermanChatMessageDto {
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
