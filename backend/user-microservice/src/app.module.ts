import { Module } from '@nestjs/common';
import { UserService } from './domain/user.service';
import { FileUserRepository } from './adapters/orm/file-user.repository';
import { UserModule } from './user.module';
import { AuthModule } from './auth.module';
import { UserController } from './adapters/http/user.controller';

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

