import * as fs from 'fs';
import * as path from 'path';
import { Injectable } from '@nestjs/common';
import { IUserRepository } from '../../domain/ports/orm/user.repository.interface';
import { IMessageRepository } from 'src/domain/ports/orm/message.repository.interface';
import { Message } from 'src/domain/entities/message.entity';

@Injectable()
export class FileMessagesRepository implements IMessageRepository {
    private readonly filePath = path.resolve(__dirname, 'messages.json');

    constructor() {
        if (!fs.existsSync(this.filePath)) {
            fs.writeFileSync(this.filePath, JSON.stringify([]));
        }
    }

    private readFromFile(): Message[] {
        const fileData = fs.readFileSync(this.filePath, 'utf8');
        return JSON.parse(fileData).map((message: any) => new Message(
            message.id, message.userID, message.text, message.role, message.chatID, message.createdAt 
        ));
    }

    private writeToFile(messages: Message[]): void {
        fs.writeFileSync(this.filePath, JSON.stringify(messages, null, 2));
    }

    async findAll(): Promise<Message[]> {
        return this.readFromFile();
    }

    async create(message: Message): Promise<void> {
        const messages = this.readFromFile();
        messages.push(message);
        this.writeToFile(messages);
    }
}
