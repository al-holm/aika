
import { UserRole } from "src/common/enums/user-role.enum";
import { User } from "../entities/user.entity";


export class UserResponseDto {
    id: number;
    username: string;
    role: UserRole;
    createdAt: Date;
    updatedAt: Date;

    constructor(id: number, email: string, role: UserRole, createdAt: Date, updatedAt: Date) {
        this.id = id;
        this.username = email;
        this.role = role;
        this.createdAt = createdAt;
        this.updatedAt = updatedAt;
    }

    static fromEntity(user: User): UserResponseDto {
        return new UserResponseDto(user.id, user.username, user.role, user.createdAt, user.updatedAt);
    }
}
