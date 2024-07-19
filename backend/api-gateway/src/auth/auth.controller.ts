import { Controller, Post, Get, Body } from '@nestjs/common';
import { ApiTags, ApiResponse, ApiExtraModels, getSchemaPath, ApiOperation} from '@nestjs/swagger';
import { Credentials } from './models/credentials';
import { AuthService } from './auth.service';

/**
 * Controller class for handling POST requests for processing messages in a
German chat application.
 * @class GermanChatController
 */
@ApiTags('AuthAPI')
@Controller('auth')
export class ChatController {
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
