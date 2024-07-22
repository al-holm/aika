import { IsEmail, IsNotEmpty, IsString, MinLength } from 'class-validator';

export class CreateUserDto {
    @IsNotEmpty()
    @IsString()
    username: string;

    @IsNotEmpty()
    @IsString()
    @MinLength(3)
    password: string;

    constructor(email: string, password: string) {
        this.username = email;
        this.password = password;
    }
}