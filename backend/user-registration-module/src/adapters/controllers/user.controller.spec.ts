import { Test, TestingModule } from '@nestjs/testing';
import { UserService } from '../../application/service/UserService';
import { CreateUserDto } from '../../application/dto/CreateUserDto';
import { UpdateUserDto } from '../../application/dto/UpdateUserDto';
import { UserResponseDto } from '../../application/dto/UserResponseDto';
import { JwtAuthGuard } from '../../configuration/auth/jwt-auth.guard';
import { RolesGuard } from '../../configuration/auth/roles.guard';
import { UserRole } from '../../core/domain/UserRole';
import {UserController} from "./UserController";

describe('UserController', () => {
    let controller: UserController;
    let service: UserService;

    const mockUserService = {
        create: jest.fn(dto => {
            return {
                id: Date.now(),
                email: dto.email,
                password: dto.password,
                role: UserRole.USER,
                createdAt: new Date(),
                updatedAt: new Date(),
            };
        }),
        findAll: jest.fn(() => [
            {
                id: 1,
                email: 'test1@example.com',
                role: UserRole.USER,
                createdAt: new Date(),
                updatedAt: new Date(),
            },
        ]),
        findOne: jest.fn(id => ({
            id,
            email: 'test@example.com',
            role: UserRole.USER,
            createdAt: new Date(),
            updatedAt: new Date(),
        })),
        update: jest.fn((id, dto) => ({
            id,
            ...dto,
            role: UserRole.USER,
            updatedAt: new Date(),
        })),
        remove: jest.fn(id => {}),
    };

    beforeEach(async () => {
        const module: TestingModule = await Test.createTestingModule({
            controllers: [UserController],
            providers: [
                {
                    provide: UserService,
                    useValue: mockUserService,
                },
            ],
        }).compile();

        controller = module.get<UserController>(UserController);
        service = module.get<UserService>(UserService);
    });

    it('should be defined', () => {
        expect(controller).toBeDefined();
    });

    it('should create a user', async () => {
        const dto: CreateUserDto = { email: 'test@example.com', password: 'password' };
        expect(await controller.create(dto)).toEqual({
            id: expect.any(Number),
            email: dto.email,
            role: UserRole.USER,
            createdAt: expect.any(Date),
            updatedAt: expect.any(Date),
        });
        expect(service.create).toHaveBeenCalledWith(dto);
    });

    it('should find all users', async () => {
        expect(await controller.findAll()).toEqual([
            {
                id: 1,
                email: 'test1@example.com',
                role: UserRole.USER,
                createdAt: expect.any(Date),
                updatedAt: expect.any(Date),
            },
        ]);
        expect(service.findAll).toHaveBeenCalled();
    });

    it('should find one user by id', async () => {
        const req = { user: { userId: 1, role: UserRole.USER } };
        expect(await controller.findOne('1', req as any)).toEqual({
            id: 1,
            email: 'test@example.com',
            role: UserRole.USER,
            createdAt: expect.any(Date),
            updatedAt: expect.any(Date),
        });
        expect(service.findOne).toHaveBeenCalledWith(1);
    });

    it('should update a user', async () => {
        const dto: UpdateUserDto = { email: 'updated@example.com' };
        const req = { user: { userId: 1, role: UserRole.USER } };
        expect(await controller.update('1', dto, req as any)).toEqual({
            id: 1,
            email: dto.email,
            role: UserRole.USER,
            updatedAt: expect.any(Date),
        });
        expect(service.update).toHaveBeenCalledWith(1, dto);
    });

    it('should remove a user', async () => {
        const req = { user: { userId: 1, role: UserRole.USER } };
        await controller.remove('1', req as any);
        expect(service.remove).toHaveBeenCalledWith(1);
    });
});
