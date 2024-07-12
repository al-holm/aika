// src/configuration/AppModule.ts
import { Module } from '@nestjs/common';
import { UserController } from '../adapters/controllers/UserController';
import { UserService } from '../application/service/UserService';
import { FileUserRepository } from '../adapters/repository/FileUserRepository';
import { UserRepository } from '../core/domain/UserRepository';
import {AuthModule} from "./auth/auth.module";
import {UserModule} from "../application/service/user.module";

@Module({
    imports: [UserModule, AuthModule],
    controllers: [UserController],
    providers: [
        UserService,
        {
            provide: 'UserRepository',
            useClass: FileUserRepository,
        },
    ],
})
export class AppModule {}
