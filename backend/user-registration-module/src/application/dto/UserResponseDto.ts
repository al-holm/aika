import { UserRole } from '../../core/domain/UserRole';
import { User } from '../../core/domain/User';

export class UserResponseDto {
    id: number;
    email: string;
    role: UserRole;
    createdAt: Date;
    updatedAt: Date;

    constructor(id: number, email: string, role: UserRole, createdAt: Date, updatedAt: Date) {
        this.id = id;
        this.email = email;
        this.role = role;
        this.createdAt = createdAt;
        this.updatedAt = updatedAt;
    }

    static fromEntity(user: User): UserResponseDto {
        return new UserResponseDto(user.id, user.email, user.role, user.createdAt, user.updatedAt);
    }
}
