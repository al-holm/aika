import { Injectable, Inject } from '@nestjs/common';
import * as bcrypt from 'bcrypt';
import { CreateUserDto } from './dto/create-user.dto';
import { IUserRepository } from './ports/orm/user.repository.interface';
import { UserRole } from '../common/enums/user-role.enum';
import { UpdateUserDto } from './dto/update-user.dto';
import { User } from './entities/user.entity';
import { IUserService } from './ports/http/user.service.interface';
import { IMessageRepository } from './ports/orm/message.repository.interface';
import { ILessonRepository } from './ports/orm/lesson.repository.interface';
import { ChatType } from 'src/common/enums/chat-type.enum';
import { Message } from './entities/message.entity';
import { MessageRole } from 'src/common/enums/message-role.enum';
import { CreateMessageDto } from './dto/create-message.dto';

@Injectable()
export class UserService implements IUserService{
    constructor(
        @Inject('UserRepository') private readonly userRepository: IUserRepository,
        @Inject('MessageRepository') private readonly messageRepository: IMessageRepository,
        @Inject('LessonRepository') private readonly lessonRepository: ILessonRepository,
    ) {}

    async createUser(createUserDto: CreateUserDto): Promise<User> {
        const users = await this.userRepository.findAll();
        const salt = await bcrypt.genSalt();
        const hashedPassword = await bcrypt.hash(createUserDto.password, salt);
        const newUser = new User(
            users.length ? users[users.length - 1].id + 1 : 1,
            createUserDto.username,
            hashedPassword,
            UserRole.USER,
            new Date(),
            new Date()
        );
        await this.userRepository.create(newUser);
        return newUser;
    }

    async getUserbyID(id: number): Promise<User | null> {
        return this.userRepository.findOne(id);
    }

    async getUserByUsername(username: string): Promise<User | null> {
        const users = await this.userRepository.findAll();
        return users.find(user => user.username === username) || null;
    }

    async getAllUsers(): Promise<User[]> {
        return this.userRepository.findAll();
    }

    async getLastBotMessage(userID: number): Promise<Message | null> {
        const messages = await this.messageRepository.findAll();
        const filteredMessages = messages.filter(
            message => message.chatID == ChatType.GERMAN && message.userID == userID && message.role == MessageRole.BOT
        );
        filteredMessages.sort((a, b) => b.createdAt.getTime() - a.createdAt.getTime());
        return filteredMessages.length > 0 ? filteredMessages[0] : null;
    }

    async getMessageHistory(userID: number, chatID: ChatType): Promise<Message[] | null> {
        const messages = await this.messageRepository.findAll();
        return messages.filter(
            message => message.chatID == chatID && message.userID == userID
        );
    }

    async addMessage(userID: number, message: CreateMessageDto) {
        const messages = await this.messageRepository.findAll();
        const newMessage = new Message(
            messages.length ? messages[messages.length - 1].id + 1 : 1,
            userID, message.text, 
            this.getMessageRole(message.role), this.getChatType(message.chatID), new Date()
        );
        await this.messageRepository.create(newMessage);
    }

    private getChatType(chatTypeStr: string): ChatType | null {
        switch (chatTypeStr) {
            case 'german':
                return ChatType.GERMAN;
            case 'law':
                return ChatType.LAW;
            default:
                return null;
        }
    }

    private getMessageRole(roleStr: string): MessageRole| null {
        switch (roleStr) {
            case 'user':
                return MessageRole.USER;
            case 'bot':
                return MessageRole.BOT;
            default:
                return null;
        }
    }

    getNextLesson(userID: number): Promise<string>;
    updateLesson(userID: number, updateLessonDto: UpdateLessonDto);
}
