import { UserRole } from './UserRole';

export class User {
    constructor(
        public readonly id: number,
        public email: string,
        public password: string,
        public role: UserRole = UserRole.USER,
        public readonly createdAt: Date = new Date(),
        public updatedAt: Date = new Date(),
    ) {}
}
