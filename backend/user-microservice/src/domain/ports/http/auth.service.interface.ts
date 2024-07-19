import { CreateUserDto } from "src/domain/dto/create-user.dto";


export interface IAuthService {
    validateUser(username: string, pass: string): Promise<any>;
    login(user: any);
    register(createUserDto: CreateUserDto);
}
