import { Body, Controller, Delete, Get, NotFoundException, Param, Post, Put, UseGuards, Request } from '@nestjs/common';
import { Request as ExpressRequest } from 'express';
import { JwtAuthGuard } from './guards/jwt-auth.guard';
import { UserRequest } from '../../common/user-request.interface';
import { UserService } from './../../domain/user.service';
import { Message } from 'src/domain/entities/message.entity';
import { CreateMessageDto } from 'src/domain/dto/create-message.dto';
import { UpdateLessonDto } from 'src/domain/dto/update-lesson.dto';



@Controller('user')
export class UserController {
    constructor(private readonly userService: UserService) {}

    @UseGuards(JwtAuthGuard)
    @Get('last-message')
    async getLastBotMessage( @Request() req: ExpressRequest & { user: UserRequest }): Promise<{'last-message': Message }> {
        const message: Message = await this.userService.getLastBotMessage(req.user.userId);
        return {'last-message': message};;
    }

    @UseGuards(JwtAuthGuard)
    @Get(':chat-id')
    async getMessageHistory(@Param('chat-id') chatID: string, @Request() req: ExpressRequest & { user: UserRequest }): 
    Promise<{'messages': Message[]}> {
        const messages = await this.userService.getMessageHistory(req.user.userID, chatID);
        return {'messages': messages};
    }

    @UseGuards(JwtAuthGuard)
    @Put('put-message')
    async putMessage(@Body() createMessageDto: CreateMessageDto, @Request() req: ExpressRequest & { user: UserRequest }): 
    Promise<void> {
        await this.userService.addMessage(req.user.userID, createMessageDto);
    }

    @UseGuards(JwtAuthGuard)
    @Get('next-topic')
    async getNextTopic(@Request() req: ExpressRequest & { user: UserRequest }): Promise<{'next-topic': string}> {
        const topic = await this.userService.getNextLesson(req.user.userID);
        return {'next-topic': topic};
    }

    @UseGuards(JwtAuthGuard)
    @Post('update-progress')
    async updateProgress(@Body() updateLessonDto: UpdateLessonDto, @Request() req: ExpressRequest & { user: UserRequest }): 
    Promise<void> {
        await this.userService.updateLesson(req.user.userID, updateLessonDto);
    }
}
