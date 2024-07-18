import { Module } from '@nestjs/common';
import { JwtModule } from '@nestjs/jwt';
import { PassportModule } from '@nestjs/passport';
import { UserModule } from './user.module';
import { AuthService } from './domain/auth.service';
import { JwtStrategy } from './adapters/http/strategies/jwt.strategy';
import { LocalStrategy } from './adapters/http/strategies/local.strategy';
import { AuthController } from './adapters/http/auth.controller';


@Module({
    imports: [
        PassportModule,
        UserModule,
        JwtModule.register({
            secret: 'your_secret_key', // замените на более безопасный секретный ключ
            signOptions: { expiresIn: '1h' },
        }),
    ],
    providers: [AuthService, JwtStrategy, LocalStrategy],
    controllers: [AuthController],
    exports: [AuthService],
})
export class AuthModule {}
