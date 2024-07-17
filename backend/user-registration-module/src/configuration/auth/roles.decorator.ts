import { SetMetadata } from '@nestjs/common';
import { UserRole } from '../../core/domain/UserRole';

export const Roles = (...roles: UserRole[]) => SetMetadata('roles', roles);
