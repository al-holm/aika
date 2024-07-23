import { CreateUserDto } from "src/domain/dto/create-user.dto";
import { UpdateUserDto } from "src/domain/dto/update-user.dto";
import { User } from "src/domain/entities/user.entity";

export interface IUserService {
    create(createUserDto: CreateUserDto): Promise<User>;
    findOne(id: number): Promise<User | null>;
    findOneByUsername(username: string): Promise<User | null>;
    remove(id: number): Promise<void>;
    findAll(): Promise<User[]>;
    update(id: number, updateUserDto: UpdateUserDto): Promise<User | null>;

}
