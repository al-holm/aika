import { Body, Controller, Delete, Get, NotFoundException, Param, Post, Put, UseGuards, Request } from '@nestjs/common';
import { Request as ExpressRequest } from 'express';
import { UserResponseDto } from '../../domain/dto/user-response.dto';
import { JwtAuthGuard } from './guards/jwt-auth.guard';
import { RolesGuard } from './guards/roles.guard';
import { UserRole } from '../../common/enums/user-role.enum';
import { Roles } from './../../common/decorators/roles.decorator';
import { UserRequest } from '../../common/user-request.interface';
import { UpdateUserDto } from '../../domain/dto/update-user.dto';
import { CreateUserDto } from '../../domain/dto/create-user.dto';
import { UserService } from './../../domain/user.service';



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
