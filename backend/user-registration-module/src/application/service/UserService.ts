import { Injectable, Inject } from '@nestjs/common';
import { User } from '../../core/domain/User';
import { CreateUserDto } from '../dto/CreateUserDto';
import { UpdateUserDto } from '../dto/UpdateUserDto';
import { UserRepository } from '../../core/domain/UserRepository';
import { UserRole } from '../../core/domain/UserRole';
import * as bcrypt from 'bcrypt';

@Injectable()
export class UserService {
    constructor(
        @Inject('UserRepository') private readonly userRepository: UserRepository,
    ) {}

    async create(createUserDto: CreateUserDto): Promise<User> {
        const users = await this.userRepository.findAll();
        const salt = await bcrypt.genSalt();
        const hashedPassword = await bcrypt.hash(createUserDto.password, salt);
        const newUser = new User(
            users.length ? users[users.length - 1].id + 1 : 1,
            createUserDto.email,
            hashedPassword,
            UserRole.USER,
            new Date(),
            new Date()
        );
        await this.userRepository.create(newUser);
        return newUser;
    }

    async findOne(id: number): Promise<User | null> {
        return this.userRepository.findOne(id);
    }

    async findOneByEmail(email: string): Promise<User | null> {
        const users = await this.userRepository.findAll();
        return users.find(user => user.email === email) || null;
    }

    async remove(id: number): Promise<void> {
        await this.userRepository.remove(id);
    }

    async findAll(): Promise<User[]> {
        return this.userRepository.findAll();
    }

    async update(id: number, updateUserDto: UpdateUserDto): Promise<User | null> {
        const user = await this.findOne(id);
        if (!user) {
            return null;
        }
        const updatedUser = { ...user, ...updateUserDto, updatedAt: new Date() };
        await this.userRepository.update(id, updatedUser);
        return updatedUser;
    }
}
