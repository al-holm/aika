import { Module } from '@nestjs/common';
import { UserService } from './UserService';
import { UserController } from '../../adapters/controllers/UserController';
import { FileUserRepository } from '../../adapters/repository/FileUserRepository';

@Module({
    imports: [],
    providers: [UserService, { provide: 'UserRepository', useClass: FileUserRepository }],
    controllers: [UserController],
    exports: [UserService],
})
export class UserModule {}
