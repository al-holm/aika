import { Body, Controller, Delete, Get, NotFoundException, Param, Post, Put, UseGuards, Request } from '@nestjs/common';
import { Request as ExpressRequest } from 'express';
import { UserResponseDto } from '../../domain/dto/user-response.dto';
import { JwtAuthGuard } from './guards/jwt-auth.guard';
import { UserRole } from '../../common/enums/user-role.enum';
import { UserRequest } from '../../common/user-request.interface';
import { UpdateUserDto } from '../../domain/dto/update-user.dto';
import { UserService } from './../../domain/user.service';



@Controller('users')
export class UserController {
    constructor(private readonly userService: UserService) {}

    @UseGuards(JwtAuthGuard)
    @Get('last-message')
    async getLastBotMessage(): Promise<UserResponseDto[]> {
        const users = await this.userService.getAllUsers();
        return users.map(user => UserResponseDto.fromEntity(user));
    }

    @UseGuards(JwtAuthGuard)
    @Get()
    async getMessageHistory(@Param('id') id: string, @Request() req: ExpressRequest & { user: UserRequest }): Promise<UserResponseDto> {
        const userId = parseInt(id, 10);
        const user = await this.userService.getUserbyID(userId);
        if (!user || (user.id !== req.user.userId && req.user.role !== UserRole.ADMIN)) {
            throw new NotFoundException(`User with id ${id} not found or unauthorized`);
        }
        return UserResponseDto.fromEntity(user);
    }

    @UseGuards(JwtAuthGuard)
    @Put('put-message')
    async putMessage(@Param('id') id: string, @Body() updateUserDto: UpdateUserDto, @Request() req: ExpressRequest & { user: UserRequest }): Promise<UserResponseDto> {
        const userId = parseInt(id, 10);
        const user = await this.userService.getUserbyID(userId);
        if (!user || (user.id !== req.user.userId && req.user.role !== UserRole.ADMIN)) {
            throw new NotFoundException(`User with id ${id} not found or unauthorized`);
        }
        const updatedUser = await this.userService.update(userId, updateUserDto);
        if (!updatedUser) {
            throw new NotFoundException(`User with id ${id} not found`);
        }
        return UserResponseDto.fromEntity(updatedUser);
    }

    @UseGuards(JwtAuthGuard)
    @Get('next-topic')
    async getNextTopic(): Promise<UserResponseDto[]> {
        const users = await this.userService.getAllUsers();
        return users.map(user => UserResponseDto.fromEntity(user));
    }

    @UseGuards(JwtAuthGuard)
    @Post('update-progress')
    async updateProgress(): Promise<UserResponseDto[]> {
        const users = await this.userService.getAllUsers();
        return users.map(user => UserResponseDto.fromEntity(user));
    }
}
