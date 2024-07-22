import { CreateUserDto } from "src/domain/dto/create-user.dto";
import { Message } from "src/domain/entities/message.entity";
import { User } from "src/domain/entities/user.entity";
import { UpdateLessonDto } from '../../dto/update-lesson.dto';
import { ChatType } from "src/common/enums/chat-type.enum";
import { CreateMessageDto } from "src/domain/dto/create-message.dto";

export interface IUserService {
    createUser(createUserDto: CreateUserDto): Promise<User>;
    getUserbyID(id: number): Promise<User | null>;
    getUserByUsername(username: string): Promise<User | null>;
    getAllUsers(): Promise<User[]>;

    getLastBotMessage(userID: number): Promise<Message | null>;
    getMessageHistory(userID: number, chatID: ChatType): Promise<Message[] | null>;
    addMessage(userID: number, message: CreateMessageDto);

    getNextLesson(userID: number): Promise<string>;
    updateLesson(userID: number, updateLessonDto: UpdateLessonDto);
}
