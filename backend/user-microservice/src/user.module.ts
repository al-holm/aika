import { Module } from '@nestjs/common';
import { UserService } from './domain/user.service';
import { FileUserRepository } from './adapters/orm/file-user.repository';
import { UserController } from './adapters/http/user.controller';
import { FileMessagesRepository } from './adapters/orm/file-messages.repository';
import { FileLessonRepository } from './adapters/orm/file-lesson.repository';


@Module({
    imports: [],
    providers: [UserService, 
        { provide: 'UserRepository', useClass: FileUserRepository },
        { provide: 'MessageRepository', useClass: FileMessagesRepository },
        { provide: 'LessonRepository', useClass: FileLessonRepository },
    ],
    controllers: [UserController],
    exports: [UserService],
})
export class UserModule {}
