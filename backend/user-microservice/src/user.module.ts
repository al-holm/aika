import { Module } from '@nestjs/common';
import { UserService } from './domain/user.service';
import { FileUserRepository } from './adapters/orm/file-user.repository';
import { UserController } from './adapters/http/user.controller';


@Module({
    imports: [],
    providers: [UserService, { provide: 'UserRepository', useClass: FileUserRepository}],
    controllers: [UserController],
    exports: [UserService],
})
export class UserModule {}
