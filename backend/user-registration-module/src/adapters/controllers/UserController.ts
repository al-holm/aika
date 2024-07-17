import { Body, Controller, Delete, Get, NotFoundException, Param, Post, Put, UseGuards, Request } from '@nestjs/common';
import { UserService } from '../../application/service/UserService';
import { CreateUserDto } from '../../application/dto/CreateUserDto';
import { UpdateUserDto } from '../../application/dto/UpdateUserDto';
import { UserResponseDto } from '../../application/dto/UserResponseDto';
import { JwtAuthGuard } from '../../configuration/auth/jwt-auth.guard';
import { RolesGuard } from '../../configuration/auth/roles.guard';
import { Roles } from '../../configuration/auth/roles.decorator';
import { UserRole } from '../../core/domain/UserRole';
import { Request as ExpressRequest } from 'express';
import { UserRequest } from '../../core/domain/UserRequest.interface';

@Controller('users')
export class UserController {
    constructor(private readonly userService: UserService) {}

    @Post()
    async create(@Body() createUserDto: CreateUserDto): Promise<UserResponseDto> {
        const user = await this.userService.create(createUserDto);
        return UserResponseDto.fromEntity(user);
    }

    @UseGuards(JwtAuthGuard, RolesGuard)
    @Roles(UserRole.ADMIN)
    @Get()
    async findAll(): Promise<UserResponseDto[]> {
        const users = await this.userService.findAll();
        return users.map(user => UserResponseDto.fromEntity(user));
    }

    @UseGuards(JwtAuthGuard)
    @Get(':id')
    async findOne(@Param('id') id: string, @Request() req: ExpressRequest & { user: UserRequest }): Promise<UserResponseDto> {
        const userId = parseInt(id, 10);
        const user = await this.userService.findOne(userId);
        if (!user || (user.id !== req.user.userId && req.user.role !== UserRole.ADMIN)) {
            throw new NotFoundException(`User with id ${id} not found or unauthorized`);
        }
        return UserResponseDto.fromEntity(user);
    }

    @UseGuards(JwtAuthGuard)
    @Delete(':id')
    async remove(@Param('id') id: string, @Request() req: ExpressRequest & { user: UserRequest }): Promise<void> {
        const userId = parseInt(id, 10);
        const user = await this.userService.findOne(userId);
        if (!user || (user.id !== req.user.userId && req.user.role !== UserRole.ADMIN)) {
            throw new NotFoundException(`User with id ${id} not found or unauthorized`);
        }
        return this.userService.remove(userId);
    }

    @UseGuards(JwtAuthGuard)
    @Put(':id')
    async update(@Param('id') id: string, @Body() updateUserDto: UpdateUserDto, @Request() req: ExpressRequest & { user: UserRequest }): Promise<UserResponseDto> {
        const userId = parseInt(id, 10);
        const user = await this.userService.findOne(userId);
        if (!user || (user.id !== req.user.userId && req.user.role !== UserRole.ADMIN)) {
            throw new NotFoundException(`User with id ${id} not found or unauthorized`);
        }
        const updatedUser = await this.userService.update(userId, updateUserDto);
        if (!updatedUser) {
            throw new NotFoundException(`User with id ${id} not found`);
        }
        return UserResponseDto.fromEntity(updatedUser);
    }
}
