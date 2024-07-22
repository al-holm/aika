import { Controller, Post, Get, Body } from '@nestjs/common';
import { ApiTags, ApiResponse, ApiExtraModels, getSchemaPath, ApiOperation} from '@nestjs/swagger';
import { Credentials } from './models/credentials';
import { AuthService } from './auth.service';


@ApiTags('AuthAPI')
@Controller('auth')
export class AuthController {
  constructor(private readonly authService: AuthService) {}


  @Post()
  @ApiOperation({
    summary: 'Gets users answer and returns bot answer in the german chat',
  })
  async authetificate( @Body() userCredentials: Credentials ): 
    Promise<{ token: String }> {
    console.log('got credentials');
    const token = await this.authService.validateCredentials(userCredentials);
    return { token };
  }

}
