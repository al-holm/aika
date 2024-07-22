import { Message } from "src/domain/entities/message.entity";


export interface IMessageRepository {
    create(message: Message): Promise<void>;
    findAll(): Promise<Message[]>;
}
