import { Test, TestingModule } from '@nestjs/testing';
import { AuthController } from './auth.controller';
import { AuthService } from './auth.service';
import { UserService } from '../../application/service/UserService';
import { CreateUserDto } from '../../application/dto/CreateUserDto';

describe('AuthController', () => {
    let controller: AuthController;
    let authService: AuthService;
    let userService: UserService;

    const mockAuthService = {
        register: jest.fn(dto => {
            return {
                access_token: 'test_token',
            };
        }),
        login: jest.fn(user => {
            return {
                access_token: 'test_token',
            };
        }),
    };

    const mockUserService = {
        create: jest.fn(dto => {
            return {
                id: Date.now(),
                ...dto,
                createdAt: new Date(),
                updatedAt: new Date(),
            };
        }),
    };

    beforeEach(async () => {
        const module: TestingModule = await Test.createTestingModule({
            controllers: [AuthController],
            providers: [
                {
                    provide: AuthService,
                    useValue: mockAuthService,
                },
                {
                    provide: UserService,
                    useValue: mockUserService,
                },
            ],
        }).compile();

        controller = module.get<AuthController>(AuthController);
        authService = module.get<AuthService>(AuthService);
        userService = module.get<UserService>(UserService);
    });

    it('should be defined', () => {
        expect(controller).toBeDefined();
    });

    it('should register a user and return a token', async () => {
        const dto: CreateUserDto = { email: 'test@example.com', password: 'password' };
        expect(await controller.register(dto)).toEqual({
            access_token: 'test_token',
        });
        expect(authService.register).toHaveBeenCalledWith(dto);
    });

    it('should login a user and return a token', async () => {
        const req = { user: { userId: 1, email: 'test@example.com', role: 'USER' } };
        expect(await controller.login(req as any)).toEqual({
            access_token: 'test_token',
        });
        expect(authService.login).toHaveBeenCalledWith(req.user);
    });
});
