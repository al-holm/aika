import { User } from "src/domain/entities/user.entity";


export interface IUserRepository {
    create(user: User): Promise<void>;
    findAll(): Promise<User[]>;
    findOne(id: number): Promise<User | null>;
    update(id: number, user: User): Promise<void>;
    remove(id: number): Promise<void>;
}
