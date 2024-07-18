import { Controller, Post, Body, Request, UseGuards } from '@nestjs/common';
import { LocalAuthGuard } from './guards/local-auth.guard';
import { Request as ExpressRequest } from 'express';
import { AuthService } from './../../domain/auth.service';
import { CreateUserDto } from '../../domain/dto/create-user.dto';
import { UserService } from './../../domain/user.service';

@Controller('auth')
export class AuthController {
    constructor(
        private readonly authService: AuthService,
        private readonly userService: UserService,
    ) {}

    @Post('register')
    async register(@Body() createUserDto: CreateUserDto) {
        return this.authService.register(createUserDto);
    }

    @UseGuards(LocalAuthGuard)
    @Post('login')
    async login(@Request() req: ExpressRequest) {
        return this.authService.login(req.user);
    }
}
