import { ChatType } from "src/common/enums/chat-type.enum";
import { MessageRole } from "src/common/enums/message-role.enum";

export class Message {
    constructor(
        public readonly id: number,
        public userID: number,
        public text: string,
        public role: MessageRole,
        public chatID: ChatType,
        public readonly createdAt: Date = new Date(),
    ) {}
}