import { Controller, Post, Body, Request, UseGuards } from '@nestjs/common';
import { LocalAuthGuard } from './guards/local-auth.guard';
import { Request as ExpressRequest } from 'express';
import { AuthService } from './../../domain/auth.service';
import { CreateUserDto } from '../../domain/dto/create-user.dto';

@Controller('auth')
export class AuthController {
    constructor(
        private readonly authService: AuthService,
    ) {}

    @Post('register')
    async register(@Body() createUserDto: CreateUserDto) {
        console.log('reg');
        console.log(createUserDto.username);
        return this.authService.register(createUserDto);
    }

    @UseGuards(LocalAuthGuard)
    @Post('login')
    async login(@Request() req: ExpressRequest) {
        console.log('log in');
        console.log(req);
        return this.authService.login(req.user);
    }
}
