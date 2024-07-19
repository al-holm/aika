import { Test, TestingModule } from '@nestjs/testing';
import { UserService } from '../src/domain/user.service';
import { UserRole } from '../src/common/enums/user-role.enum';
import { CreateUserDto } from '../src/domain/dto/create-user.dto';
import { UpdateUserDto } from '../src/domain/dto/update-user.dto';
import { UserController } from '../src/adapters/http/user.controller';

describe('UserController', () => {
    let controller: UserController;
    let service: UserService;

    const mockUserService = {
        create: jest.fn(dto => {
            return {
                id: Date.now(),
                username: dto.username,
                password: dto.password,
                role: UserRole.USER,
                createdAt: new Date(),
                updatedAt: new Date(),
            };
        }),
        findAll: jest.fn(() => [
            {
                id: 1,
                username: 'test1@example.com',
                role: UserRole.USER,
                createdAt: new Date(),
                updatedAt: new Date(),
            },
        ]),
        findOne: jest.fn(id => ({
            id,
            username: 'test@example.com',
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
        const dto: CreateUserDto = { username: 'test@example.com', password: 'password' };
        expect(await controller.create(dto)).toEqual({
            id: expect.any(Number),
            username: dto.username,
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
                username: 'test1@example.com',
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
            username: 'test@example.com',
            role: UserRole.USER,
            createdAt: expect.any(Date),
            updatedAt: expect.any(Date),
        });
        expect(service.findOne).toHaveBeenCalledWith(1);
    });

    it('should update a user', async () => {
        const dto: UpdateUserDto = { username: 'updated@example.com' };
        const req = { user: { userId: 1, role: UserRole.USER } };
        expect(await controller.update('1', dto, req as any)).toEqual({
            id: 1,
            username: dto.username,
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
