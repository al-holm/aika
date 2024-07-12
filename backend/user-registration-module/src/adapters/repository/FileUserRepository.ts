import * as fs from 'fs';
import * as path from 'path';
import { Injectable } from '@nestjs/common';
import { UserRepository } from '../../core/domain/UserRepository';
import { User } from '../../core/domain/User';

@Injectable()
export class FileUserRepository implements UserRepository {
    private readonly filePath = path.resolve(__dirname, 'users.json');

    constructor() {
        if (!fs.existsSync(this.filePath)) {
            fs.writeFileSync(this.filePath, JSON.stringify([]));
        }
    }

    private readFromFile(): User[] {
        const fileData = fs.readFileSync(this.filePath, 'utf8');
        return JSON.parse(fileData).map((user: any) => new User(
            user.id,
            user.email,
            user.password,
            user.role,
            new Date(user.createdAt),
            new Date(user.updatedAt)
        ));
    }

    private writeToFile(users: User[]): void {
        fs.writeFileSync(this.filePath, JSON.stringify(users, null, 2));
    }

    async findAll(): Promise<User[]> {
        return this.readFromFile();
    }

    async findOne(id: number): Promise<User | null> {
        const users = this.readFromFile();
        const user = users.find(user => user.id === id);
        return user || null;
    }

    async create(user: User): Promise<void> {
        const users = this.readFromFile();
        users.push(user);
        this.writeToFile(users);
    }

    async update(id: number, updatedUser: User): Promise<void> {
        const users = this.readFromFile();
        const userIndex = users.findIndex(user => user.id === id);
        if (userIndex !== -1) {
            users[userIndex] = updatedUser;
            this.writeToFile(users);
        }
    }

    async remove(id: number): Promise<void> {
        let users = this.readFromFile();
        users = users.filter(user => user.id !== id);
        this.writeToFile(users);
    }
}
