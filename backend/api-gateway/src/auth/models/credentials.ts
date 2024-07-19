import { IsString, IsDateString, IsBoolean } from 'class-validator';
import { ApiProperty } from '@nestjs/swagger';


export class Credentials {
  @ApiProperty({
    example: 'karl_wuch',
    required: true
 })

  @IsString()
  username: string;

  @ApiProperty({
    example: '35d47560-dcff-4767-9903-16e8096d055a',
    required: true
 })
  @IsString()
  password: string;

  @ApiProperty({
    example: 'true',
    required: true
 })
  @IsBoolean()
  isSignUp: boolean;
}